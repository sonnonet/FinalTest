"""
쿨에스엠에스 API를 이용한 SMS 서비스
"""

from dotenv import load_dotenv
import auth
import requests
import os

load_dotenv() # .env 파일

SMS_API_KEY = os.environ.get("SMS_API_KEY")
SMS_API_SECRET = os.environ.get("SMS_API_SECRET")

# API에 메시지 전송 요청
def send(data):
    requests.post("https://api.coolsms.co.kr/messages/v4/send",
                  headers=auth.get_headers(SMS_API_KEY, SMS_API_SECRET),
                  json=data)

if __name__ == "__main__":
    params = dict()
    params["message"] = dict()
    params["message"]["to"] = "" # 받는 사람 번호
    params["message"]["from"] = "" # 보내는 사람 번호
    params["message"]["text"] = "test" # 내용
    
    send(params)
    