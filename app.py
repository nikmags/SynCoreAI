import streamlit as st
from utils.yt_comment_fetcher import get_comments
import openai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="YouTube Comment Summarizer", layout="centered")
st.title("🎥 YouTube Comment Summarizer")

video_url = st.text_input("Paste a YouTube Video URL")

if st.button("Summarize Comments") and video_url:
    with st.spinner("Fetching comments..."):
        comments = get_comments(video_url)

    if not comments:
        st.error("No comments found or invalid video URL.")
    else:
        with st.spinner("Summarizing with AI..."):
            prompt = "Summarize the following YouTube comments:\n" + "\n".join(comments)
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                summary = response['choices'][0]['message']['content']
                st.success("Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"Error calling OpenAI: {e}")
