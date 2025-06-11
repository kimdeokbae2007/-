from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import datetime

app = Flask(__name__)

@app.route("/meal", methods=["POST"])
def get_meal():
    today = datetime.datetime.now()
    ymd = today.strftime("%Y%m%d")
    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?ATPT_OFCDC_SC_CODE=B10&SD_SCHUL_CODE=7091428&MLSV_YMD={ymd}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dish_list = soup.find_all('ddish_nm')

    if not dish_list:
        meal = "오늘은 급식 정보가 없습니다."
    else:
        menu = dish_list[0].get_text().replace('<br/>', '\n')
        meal = f"오늘의 급식입니다:\n{menu}"

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