import json

def handler(request, response):
    try:
        # 요청 데이터 받기
        body = request.get_json()
        appraisal_price = float(body.get('감정가', 0))
        expected_competition = float(body.get('예상경쟁률', 1.0))
        discount_rate = float(body.get('할인율', 10))  # 예: 10% 할인 기준

        # 계산식: 감정가에서 할인 → 경쟁률 따라 입찰가 가중
        base_bid = appraisal_price * (1 - discount_rate / 100)
        adjusted_bid = base_bid * (1 + expected_competition / 10)

        result = {
            "입찰가_제안": round(adjusted_bid, -2),
            "감정가": appraisal_price,
            "할인율": discount_rate,
            "예상경쟁률": expected_competition,
            "코멘트": "적정한 수준의 입찰가를 계산했습니다."
        }

        response.status_code = 200
        response.body = json.dumps(result)
        return response

    except Exception as e:
        response.status_code = 500
        response.body = json.dumps({"error": str(e)})
        return response
