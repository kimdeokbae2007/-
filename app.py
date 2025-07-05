from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import datetime

app = Flask(__name__)

@app.route("/meal", methods=["POST"])
def get_meal():
    try:
        # 날짜 포맷
        today = datetime.datetime.now()
        ymd = today.strftime("%Y%m%d")
        
        # NEIS API URL 구성
        url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?ATPT_OFCDC_SC_CODE=Q10&SD_SCHUL_CODE=8490083&MLSV_YMD={ymd}"

        # timeout 추가 (2초 초과 시 실패로 간주)
        response = requests.get(url, timeout=2)

        # BeautifulSoup으로 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        dish_list = soup.find_all('ddish_nm')

        if not dish_list:
            meal = "오늘은 급식 정보가 없습니다."
        else:
            menu = dish_list[0].get_text().replace('<br/>', '\n')
            meal = f"오늘의 급식입니다:\n{menu}"
    
    except Exception as e:
        # 오류 발생 시 기본 안내 메시지 반환
        meal = "⚠️ 급식 정보를 불러오는 데 실패했습니다.\n잠시 후 다시 시도해주세요."

    # JSON 형태로 카카오톡 챗봇 응답
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": meal
                }
            }]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
