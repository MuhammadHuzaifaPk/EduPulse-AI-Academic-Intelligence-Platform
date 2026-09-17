import re
from typing import Dict, Any, List
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from app.core.logger import logger
from app.core.exceptions import TranscriptExtractionError

class YouTubeService:
    """
    Extracts, cleans, and formats YouTube transcripts for AI summarization engines.
    """

    @staticmethod
    def extract_video_id(url_or_id: str) -> str:
        """
        Extracts 11-character YouTube video ID from various URL formats.
        Supports: Standard, Shortened (youtu.be), Embeds, and Raw IDs.
        """
        url_or_id = url_or_id.strip()
        
        # Regular expressions for YouTube URL patterns
        patterns = [
            r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:[&?\/].*)?$",
            r"youtu\.be\/([0-9A-Za-z_-]{11})",
            r"youtube\.com\/embed\/([0-9A-Za-z_-]{11})",
            r"^([0-9A-Za-z_-]{11})$"
        ]

        for pattern in patterns:
            match = re.search(pattern, url_or_id)
            if match:
                return match.group(1)

        raise TranscriptExtractionError(f"Invalid YouTube URL or Video ID format: '{url_or_id}'")

    async def get_transcript(self, video_url_or_id: str, languages: List[str] = ["en"]) -> Dict[str, Any]:
        """
        Fetches transcript entries from YouTube API and formats into plain text and timestamped segments.
        """
        video_id = self.extract_video_id(video_url_or_id)
        logger.info(f"Extracting transcript for YouTube Video ID: {video_id}")

        try:
            # Instantiate transcript list
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            
            full_text_chunks = []
            formatted_timestamps = []

            for entry in transcript_list:
                text_clean = entry["text"].replace("\n", " ").strip()
                start_time = int(entry["start"])
                
                # Format time string HH:MM:SS
                minutes, seconds = divmod(start_time, 60)
                hours, minutes = divmod(minutes, 60)
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours > 0 else f"{minutes:02d}:{seconds:02d}"

                full_text_chunks.append(text_clean)
                formatted_timestamps.append({
                    "time": time_str,
                    "seconds": start_time,
                    "text": text_clean
                })

            combined_text = " ".join(full_text_chunks)

            return {
                "video_id": video_id,
                "video_url": f"[https://www.youtube.com/watch?v=](https://www.youtube.com/watch?v=){video_id}",
                "transcript_text": combined_text,
                "word_count": len(combined_text.split()),
                "timestamps": formatted_timestamps
            }

        except TranscriptsDisabled:
            raise TranscriptExtractionError(f"Subtitles/Transcripts are disabled for video ID: {video_id}")
        except NoTranscriptFound:
            raise TranscriptExtractionError(f"No English transcript found for video ID: {video_id}")
        except Exception as err:
            logger.error(f"Error fetching YouTube transcript: {str(err)}")
            raise TranscriptExtractionError(f"Failed to fetch YouTube transcript: {str(err)}")

# Global Singleton Instance
youtube_service = YouTubeService()