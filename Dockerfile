# Runtime image for the self-hosted Telegram downloader bot.
#
# Built and published from .github/workflows/release.yml to
# ghcr.io/miladateight/instagram-youtube-soundcloud-downloader.
FROM python:3.12-slim

# yt-dlp merges separate video and audio streams, extracts audio, and the song
# recogniser cuts a 15-second snippet — all of that shells out to ffmpeg, so
# the binary has to be in the image or the bot fails at the first download.
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg ca-certificates \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Dependencies before source: this layer is only rebuilt when a requirement
# changes, not on every edit to the bot.
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY downloader_bot ./downloader_bot

# Everything the bot writes goes under a single mount point, so the container
# can be replaced without losing the access list, the state or the logs.
ENV DOWNLOAD_DIR=/data/downloads \
    DATA_DIR=/data/state \
    LOG_DIR=/data/logs

RUN useradd --system --create-home --uid 10001 bot \
 && mkdir -p /data/downloads /data/state /data/logs \
 && chown -R bot:bot /data

USER bot
VOLUME ["/data"]

CMD ["python", "-m", "downloader_bot"]
