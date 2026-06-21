from __future__ import annotations

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
from .utils import file_kind, human_size, truncate_caption


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
        valid_files = [item for item in result.files if item.size <= self.settings.max_upload_bytes]
        skipped = [item for item in result.files if item.size > self.settings.max_upload_bytes]

        if not valid_files:
            await self.bot.send_message(
                chat_id,
                t(language, "oversized_all", limit=self.settings.max_upload_mb),
            )
            return

        valid_files = self._soundcloud_friendly_order(valid_files)
        kinds = [file_kind(item.path) for item in valid_files]
        caption, caption_markup = self._caption_preview(result.caption, language, caption_id)

        if all(kind in {"photo", "video"} for kind in kinds) and len(valid_files) > 1:
            await self._send_media_groups(chat_id, valid_files, kinds, caption)
            if caption_markup:
                await self.bot.send_message(
                    chat_id,
                    caption or result.title,
                    reply_markup=caption_markup,
                )
        else:
            await self._send_one_by_one(chat_id, valid_files, kinds, caption, caption_markup, result)

        if skipped:
            skipped_text = "\n".join(
                f"- {item.path.name} ({human_size(item.size)})" for item in skipped[:10]
            )
            await self.bot.send_message(
                chat_id,
                t(language, "skipped_files", files=skipped_text),
            )

    async def _send_media_groups(self, chat_id: int, files, kinds, caption: str | None) -> None:
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
                    media.append(InputMediaVideo(media=input_file, caption=item_caption))
            await self.bot.send_media_group(chat_id=chat_id, media=media)

    async def _send_one_by_one(
        self,
        chat_id: int,
        files,
        kinds,
        caption: str | None,
        caption_markup: InlineKeyboardMarkup | None,
        result: DownloadResult,
    ) -> None:
        for index, (item, kind) in enumerate(zip(files, kinds)):
            item_caption = caption if index == 0 else None
            reply_markup = caption_markup if index == 0 else None
            input_file = FSInputFile(item.path)
            if kind == "photo":
                await self.bot.send_photo(
                    chat_id,
                    input_file,
                    caption=item_caption,
                    reply_markup=reply_markup,
                )
            elif kind == "video":
                await self.bot.send_video(
                    chat_id,
                    input_file,
                    caption=item_caption,
                    reply_markup=reply_markup,
                )
            elif kind == "audio":
                await self.bot.send_audio(
                    chat_id,
                    input_file,
                    caption=item_caption,
                    title=result.title,
                    performer=result.uploader,
                    reply_markup=reply_markup,
                )
            else:
                await self.bot.send_document(
                    chat_id,
                    input_file,
                    caption=item_caption,
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
