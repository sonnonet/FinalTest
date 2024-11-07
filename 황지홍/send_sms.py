from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
from dotenv import load_dotenv
import os

# 쿨에스엠에스 API를 이용한 SMS 서비스

load_dotenv()

SMS_API_KEY = os.environ.get('SMS_API_KEY')
SMS_API_SECRET = os.environ.get('SMS_API_SECRET')

params = dict()
params['type'] = 'sms'
params['to'] = '받는사람 번호 ' # 받는 사람 번호
params['from'] = '보내는 사람 번호' # 보내는 사람 번호
params['text'] = '보낼 내용' # 내용

cool = Message(SMS_API_KEY, SMS_API_SECRET)

response = cool.send(params)
print("성공 여부 : %s" % response['success_count'])
print("실패 여부 : %s" % response['error_count'])

if "error_list" in response:
    print("에러 정보 : %s" % response['error_list'])

