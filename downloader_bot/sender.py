from __future__ import annotations

import logging
from contextlib import suppress

from aiogram import Bot
from aiogram.types import (
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
)

from .config import Settings
from .downloader import DownloadResult
from .i18n import t
from .state import BotState
from .utils import file_kind, truncate_caption


class TelegramSender:
    def __init__(self, bot: Bot, settings: Settings, state: BotState | None = None) -> None:
        self.bot = bot
        self.settings = settings
        self.state = state

    async def send_result(
        self,
        chat_id: int,
        result: DownloadResult,
        language: str = "fa",
        caption_id: str | None = None,
    ) -> None:
        valid_files = list(result.files)

        if not valid_files:
            await self.bot.send_message(
                chat_id,
                t(language, "no_files_to_send"),
            )
            return

        valid_files = self._soundcloud_friendly_order(valid_files)
        kinds = [file_kind(item.path) for item in valid_files]
        caption, caption_markup = self._caption_preview(result.caption, language, caption_id)

        has_audio = "audio" in kinds
        has_photo = "photo" in kinds
        if has_audio and has_photo and not any(k == "video" for k in kinds):
            await self._send_soundcloud_bundle(
                chat_id, valid_files, kinds, caption, caption_markup, result, language
            )
            return

        if all(kind in {"photo", "video"} for kind in kinds) and len(valid_files) > 1:
            await self._send_media_groups(chat_id, valid_files, kinds, caption, language)
            if caption_markup:
                await self.bot.send_message(
                    chat_id,
                    caption or result.title,
                    reply_markup=caption_markup,
                )
        else:
            await self._send_one_by_one(chat_id, valid_files, kinds, caption, caption_markup, result, language)

    async def _send_soundcloud_bundle(
        self,
        chat_id: int,
        files,
        kinds,
        caption: str | None,
        caption_markup: InlineKeyboardMarkup | None,
        result: DownloadResult,
        language: str,
    ) -> None:
        photos = [item for item, kind in zip(files, kinds) if kind == "photo"]
        audios = [item for item, kind in zip(files, kinds) if kind == "audio"]

        for photo in photos:
            with suppress(Exception):
                await self.bot.send_photo(chat_id, FSInputFile(photo.path))

        for index, item in enumerate(audios):
            item_caption = caption if index == 0 else None
            reply_markup = caption_markup if index == 0 else None
            oversized = item.size > self.settings.max_upload_bytes
            if oversized:
                await self._send_as_document(chat_id, item, item_caption, reply_markup, language)
                continue
            sent = await self._try_send_audio(chat_id, item, item_caption, reply_markup, result)
            if not sent:
                await self._send_as_document(chat_id, item, item_caption, reply_markup, language)

    async def _send_media_groups(
        self,
        chat_id: int,
        files,
        kinds,
        caption: str | None,
        language: str,
    ) -> None:
        for chunk_start in range(0, len(files), 10):
            chunk = files[chunk_start : chunk_start + 10]
            chunk_kinds = kinds[chunk_start : chunk_start + 10]
            media = []
            for index, (item, kind) in enumerate(zip(chunk, chunk_kinds)):
                item_caption = caption if chunk_start == 0 and index == 0 else None
                input_file = FSInputFile(item.path)
                if kind == "photo":
                    media.append(InputMediaPhoto(media=input_file, caption=item_caption))
                else:
                    thumb = FSInputFile(item.thumbnail_path) if item.thumbnail_path and item.thumbnail_path.exists() else None
                    media.append(
                        InputMediaVideo(
                            media=input_file,
                            caption=item_caption,
                            width=item.width,
                            height=item.height,
                            duration=int(item.duration) if item.duration else None,
                            thumbnail=thumb,
                            supports_streaming=True,
                        )
                    )
            await self.bot.send_media_group(chat_id=chat_id, media=media)

    async def _send_one_by_one(
        self,
        chat_id: int,
        files,
        kinds,
        caption: str | None,
        caption_markup: InlineKeyboardMarkup | None,
        result: DownloadResult,
        language: str,
    ) -> None:
        for index, (item, kind) in enumerate(zip(files, kinds)):
            item_caption = caption if index == 0 else None
            reply_markup = caption_markup if index == 0 else None
            oversized = item.size > self.settings.max_upload_bytes

            if oversized:
                await self._send_as_document(chat_id, item, item_caption, reply_markup, language)
                continue

            sent = False
            if kind == "photo":
                sent = await self._try_send_photo(chat_id, item, item_caption, reply_markup)
            elif kind == "video":
                sent = await self._try_send_video(chat_id, item, item_caption, reply_markup, language)
            elif kind == "audio":
                sent = await self._try_send_audio(chat_id, item, item_caption, reply_markup, result)
            if not sent:
                await self._send_as_document(chat_id, item, item_caption, reply_markup, language)

    async def _try_send_photo(self, chat_id: int, item, caption, reply_markup) -> bool:
        try:
            await self.bot.send_photo(
                chat_id,
                FSInputFile(item.path),
                caption=caption,
                reply_markup=reply_markup,
            )
            return True
        except Exception as exc:
            logging.warning("send_photo failed, will fall back to document: %s", exc)
            return False

    async def _try_send_video(self, chat_id: int, item, caption, reply_markup, language: str) -> bool:
        try:
            thumb_file = (
                FSInputFile(item.thumbnail_path)
                if item.thumbnail_path and item.thumbnail_path.exists()
                else None
            )
            await self.bot.send_video(
                chat_id,
                FSInputFile(item.path),
                caption=caption,
                width=item.width,
                height=item.height,
                duration=int(item.duration) if item.duration else None,
                thumbnail=thumb_file,
                supports_streaming=True,
                reply_markup=reply_markup,
            )
            return True
        except Exception as exc:
            lowered = str(exc).lower()
            if any(tok in lowered for tok in ("too large", "larger than", "request entity", "file is too big")):
                return False
            logging.warning("send_video failed, will fall back to document: %s", exc)
            return False

    async def _try_send_audio(self, chat_id: int, item, caption, reply_markup, result: DownloadResult) -> bool:
        try:
            thumb_file = (
                FSInputFile(item.thumbnail_path)
                if item.thumbnail_path and item.thumbnail_path.exists()
                else None
            )
            await self.bot.send_audio(
                chat_id,
                FSInputFile(item.path),
                caption=caption,
                duration=int(item.duration) if item.duration else None,
                performer=result.uploader,
                title=result.title,
                thumbnail=thumb_file,
                reply_markup=reply_markup,
            )
            return True
        except Exception as exc:
            logging.warning("send_audio failed, will fall back to document: %s", exc)
            return False

    async def _send_as_document(self, chat_id: int, item, caption, reply_markup, language: str) -> None:
        with suppress(Exception):
            await self.bot.send_document(
                chat_id,
                FSInputFile(item.path),
                caption=caption,
                reply_markup=reply_markup,
            )

    def _caption_preview(
        self,
        caption: str | None,
        language: str,
        caption_id: str | None,
    ) -> tuple[str | None, InlineKeyboardMarkup | None]:
        if not caption:
            return None, None

        lines = [line.strip() for line in caption.strip().splitlines() if line.strip()]
        preview = "\n".join(lines[:3])
        preview = truncate_caption(preview, 350) or preview
        full_is_longer = preview.strip() != caption.strip()

        if not full_is_longer or not caption_id or not self.state:
            return truncate_caption(caption, 900), None

        self.state.save_caption(caption_id, caption)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=t(language, "full_caption_button"),
                        callback_data=f"caption:{caption_id}",
                    )
                ]
            ]
        )
        return preview, keyboard

    @staticmethod
    def _soundcloud_friendly_order(files):
        if not any(file_kind(item.path) == "audio" for item in files):
            return files
        priority = {"photo": 0, "audio": 1, "video": 2, "document": 3}
        return sorted(files, key=lambda item: priority.get(file_kind(item.path), 3))