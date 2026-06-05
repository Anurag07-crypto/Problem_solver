from googleapiclient.discovery import build
import os  
from dotenv import load_dotenv
import sys 
from pathlib import Path
from logger import get_logger

sys.path.insert(0, str(Path(__file__).parent.parent))
logger = get_logger(__name__)

def yt_search(query:str):
    
    load_dotenv()
    API_KEY = os.getenv("YOUTUBE_API_KEY")
    if not API_KEY:
        logger.critical("API key is not working")
        raise RuntimeError("API key not Found")
    youtube = build("youtube", "v3", developerKey=API_KEY)

# Search videos
    search_response = youtube.search().list(
    q=query,
    part="snippet",
    type="video",
    maxResults=20
).execute()

    video_ids = [item["id"]["videoId"]
             for item in search_response["items"]]

# Get statistics
    video_response = youtube.videos().list(
    part="snippet,statistics",
    id=",".join(video_ids)
).execute()

    videos = []

    for item in video_response["items"]:
        likes = int(item["statistics"].get("likeCount", 0))
        views = int(item["statistics"].get("viewCount", 0))

        video_id = item["id"]
        engagement_rate = (
        (likes / views) * 100
        if views > 0 else 0
    )

        videos.append({
        "title": item["snippet"]["title"],
        "likes": likes,
        "views": views,
        "engagement_rate": engagement_rate,
        "link": f"https://www.youtube.com/watch?v={video_id}"
    })

    videos.sort(
    key=lambda x: x["engagement_rate"],
    reverse=True
)

    # for rank, video in enumerate(videos, start=1):
    #     print(
    #     f"{rank}. {video['title']} "
    #     f"({video['engagement_rate']:.2f}%)"
    # )  # For next streamlit site
    #  print(video["link"])
    logger.info("Youtube videos info is ready")
    return videos

