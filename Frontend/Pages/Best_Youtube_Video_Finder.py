import sys 
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Tools.yt_video_finder import yt_search
import streamlit as st 

# Page configuration
st.set_page_config(
    page_title="YouTube Video Finder",
    page_icon="🎥",
    layout="wide"
)

# Custom CSS for video cards
st.markdown("""
    <style>
        .video-card {
            padding: 20px;
            border-radius: 10px;
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        .video-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-color: #1f77e6;
        }
        .video-rank {
            display: inline-block;
            background-color: #1f77e6;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
            margin-right: 10px;
        }
        .video-title {
            font-size: 1.1em;
            font-weight: bold;
            color: #1a1a1a;
            margin: 10px 0;
        }
        .video-stats {
            display: flex;
            gap: 20px;
            margin: 10px 0;
            flex-wrap: wrap;
        }
        .stat-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        .stat-value {
            color: #1f77e6;
            font-weight: bold;
            font-size: 1.1em;
        }
        .engagement-bar {
            width: 100%;
            height: 6px;
            background-color: #e0e0e0;
            border-radius: 3px;
            margin: 10px 0;
            overflow: hidden;
        }
        .engagement-fill {
            height: 100%;
            background: linear-gradient(90deg, #1f77e6, #00d4ff);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align: center; color: #1f77e6;">🎥 Best YouTube Video Finder</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">Find the best videos based on engagement rates</p>', unsafe_allow_html=True)
st.markdown('---')

col1, col2 = st.columns([0.85, 0.15])

with col1:
    user_query = st.text_input(
        "Search for videos...",
        placeholder="Enter your search query",
        label_visibility="collapsed"
    )

with col2:
    search_button = st.button("🔍 Search", use_container_width=True)

if user_query:
    try:
        with st.spinner("🔄 Searching YouTube..."):
            videos = yt_search(query=user_query)
        
        if videos:
            st.success(f"✅ Found {len(videos)} videos")
            st.markdown('---')
            
            for rank, video in enumerate(videos, start=1):
                video_link = video['link']
                video_title = video['title']
                engagement_rate = video['engagement_rate']
                views = video['views']
                likes = video['likes']
                
                # Create video card HTML
                card_html = f"""
                <div class="video-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <span class="video-rank">#{rank}</span>
                            <div class="video-title">{video_title}</div>
                        </div>
                        <div style="text-align: right;">
                            <div class="stat-value" style="font-size: 1.3em;">{engagement_rate:.2f}%</div>
                            <div class="stat-label">Engagement</div>
                        </div>
                    </div>
                    
                    <div class="engagement-bar">
                        <div class="engagement-fill" style="width: {min(engagement_rate * 10, 100)}%;"></div>
                    </div>
                    
                    <div class="video-stats">
                        <div class="stat-item">
                            <span class="stat-label">👁️ Views:</span>
                            <span class="stat-value">{views:,}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">👍 Likes:</span>
                            <span class="stat-value">{likes:,}</span>
                        </div>
                    </div>
                </div>
                """
                
                st.markdown(card_html, unsafe_allow_html=True)
                st.markdown(f'<a href="{video_link}" target="_blank" style="display: inline-block; padding: 8px 16px; background-color: #1f77e6; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">▶️ Watch on YouTube</a>', unsafe_allow_html=True)
                st.markdown('---')
        else:
            st.warning("No videos found. Try a different search.")
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Make sure your YOUTUBE_API_KEY is set in your .env file")