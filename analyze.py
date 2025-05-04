from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import openai
import os
from googleapiclient.discovery import build

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

@app.post("/api/analyze")
async def analyze(request: Request):
    data = await request.json()
    user_text = data.get("text", "")

    # GPT 프롬프트 생성
    prompt = f"""
    사용자가 보낸 부동산 등기 내용입니다:
    \"\"\"{user_text}\"\"\"
    이 내용을 보고 권리분석 요약을 해줘. 위험요소가 있다면 알려줘.
    """

    # GPT 호출
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "부동산 경매 전문가처럼 분석해줘."},
            {"role": "user", "content": prompt}
        ]
    )
    gpt_result = response.choices[0].message.content

    # 유튜브 검색 (예: "권리분석 강의")
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q="권리분석 강의",
        part="snippet",
        type="video",
        maxResults=1
    ).execute()

    video_title = search_response["items"][0]["snippet"]["title"]
    video_url = "https://www.youtube.com/watch?v=" + search_response["items"][0]["id"]["videoId"]

    return JSONResponse(content={
        "권리분석결과": gpt_result,
        "추천강의": {"제목": video_title, "링크": video_url}
    })
