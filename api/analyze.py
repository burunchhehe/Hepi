import openai
import os
import json
from googleapiclient.discovery import build

def handler(request, context):
    try:
        body = json.loads(request.body.decode("utf-8"))
        user_text = body.get("text", "")

        # API 키 불러오기
        openai.api_key = os.environ["OPENAI_API_KEY"]
        youtube_api_key = os.environ["YOUTUBE_API_KEY"]

        # GPT 프롬프트 구성
        prompt = f"""
        사용자가 보낸 부동산 등기 내용입니다:
        \"\"\"{user_text}\"\"\"
        이 내용을 보고 권리분석 요약을 해줘. 위험요소가 있다면 알려줘.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "부동산 경매 전문가처럼 분석해줘."},
                {"role": "user", "content": prompt}
            ]
        )
        gpt_result = response.choices[0].message["content"]

        # 유튜브 검색
        youtube = build("youtube", "v3", developerKey=youtube_api_key)
        search_response = youtube.search().list(
            q="권리분석 강의",
            part="snippet",
            type="video",
            maxResults=1
        ).execute()

        video_title = search_response["items"][0]["snippet"]["title"]
        video_url = "https://www.youtube.com/watch?v=" + search_response["items"][0]["id"]["videoId"]

        return {
            "statusCode": 200,
            "body": json.dumps({
                "권리분석결과": gpt_result,
                "추천강의": {
                    "제목": video_title,
                    "링크": video_url
                }
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
