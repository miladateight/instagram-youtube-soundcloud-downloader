from __future__ import annotations

from aiogram import Bot
from aiogram.types import (
    FSInputFile,
    InputMediaPhoto,
    InputMediaVideo,
)

from .config import Settings
from .downloader import DownloadResult
from .i18n import t
from .utils import file_kind, human_size, truncate_caption


class TelegramSender:
    def __init__(self, bot: Bot, settings: Settings) -> None:
        self.bot = bot
        self.settings = settings

    async def send_result(self, chat_id: int, result: DownloadResult, language: str = "fa") -> None:
        valid_files = [item for item in result.files if item.size <= self.settings.max_upload_bytes]
        skipped = [item for item in result.files if item.size > self.settings.max_upload_bytes]

        if not valid_files:
            await self.bot.send_message(
                chat_id,
                t(language, "oversized_all", limit=self.settings.max_upload_mb),
            )
            return

        kinds = [file_kind(item.path) for item in valid_files]
        caption = truncate_caption(result.caption)

        if all(kind in {"photo", "video"} for kind in kinds) and len(valid_files) > 1:
            await self._send_media_groups(chat_id, valid_files, kinds, caption)
        else:
            await self._send_one_by_one(chat_id, valid_files, kinds, caption)

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

    async def _send_one_by_one(self, chat_id: int, files, kinds, caption: str | None) -> None:
        for index, (item, kind) in enumerate(zip(files, kinds)):
            item_caption = caption if index == 0 else None
            input_file = FSInputFile(item.path)
            if kind == "photo":
                await self.bot.send_photo(chat_id, input_file, caption=item_caption)
            elif kind == "video":
                await self.bot.send_video(chat_id, input_file, caption=item_caption)
            elif kind == "audio":
                await self.bot.send_audio(chat_id, input_file, caption=item_caption)
            else:
                await self.bot.send_document(chat_id, input_file, caption=item_caption)
