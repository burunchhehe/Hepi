import os
import openai
from googleapiclient.discovery import build

# ✅ GPT 키 환경변수로부터 불러오기
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ GPT 질문 보내기
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "너는 경매 전문가야."},
        {"role": "user", "content": "전세사기 어떻게 피하죠?"}
    ]
)

# ✅ GPT 응답 출력
print(response.choices[0].message.content)

# ✅ 유튜브 API 키 환경변수에서 불러오기
API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)

# ✅ 유튜브 영상 검색 함수
def search_youtube(query, max_results=3):
    print("\n[유튜브 검색 결과]")
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id,snippet",
        maxResults=max_results
    ).execute()

    for item in search_response["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        print(f"{title}\nhttps://www.youtube.com/watch?v={video_id}\n")

# ✅ 함수 실행
search_youtube("전세사기")


import os
import requests

# ✅ 환경변수에서 불러오기!
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    response = requests.post(url, data=data)
    return response.json()

# ✅ 테스트 실행
if __name__ == "__main__":
    send_telegram_message("✅ Render 서버 실행 성공! 헤피 메시지 전송 테스트")
