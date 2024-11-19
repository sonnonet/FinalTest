import sys
import tos
import datetime
import pyttsx3

# CO2 임계값 설정 (ppm)
CO2_THRESHOLD = 1000

# pyttsx3 엔진 초기화
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # 말하는 속도 설정

class OscilloscopeMsg(tos.Packet):
    def __init__(self, packet=None):
        tos.Packet.__init__(self,
                            [('srcID', 'int', 2),
                             ('seqNo', 'int', 4),
                             ('type', 'int', 2),
                             ('Data0', 'int', 2),
                             ('Data1', 'int', 2),
                             ('Data2', 'int', 2),
                             ('Data3', 'int', 2),
                             ('Data4', 'int', 2),
                             ('Data5', 'int', 2),
                            ],
                            packet)

def play_warning_message():
    """음성 경고 메시지를 재생하는 함수"""
    engine.say("경고: CO2 농도가 임계값을 초과했습니다. 즉시 환기가 필요합니다.")
    engine.runAndWait()

if '-h' in sys.argv:
    print("Usage:", sys.argv[0], "serial@/dev/ttyUSB0:57600")
    sys.exit()

# AM 객체 생성
try:
    am = tos.AM()
    print("AM 객체가 생성되었습니다.")
except Exception as e:
    print("AM 객체 생성 오류:", e)
    sys.exit(1)

print("데이터 수신을 시작합니다...")

while True:
    try:
        p = am.read()
        if p:
            msg = OscilloscopeMsg(p.data)
            if msg.type == 1:  # CO2 데이터 타입인 경우
                CO2 = msg.Data0
                CO2 = 1.5 * CO2 / 4096 * 2 * 1000
                print(f"{datetime.datetime.now()} - ID: {msg.srcID}, seqNo: {msg.seqNo}, CO2: {CO2:.2f} ppm")

                # 임계값 초과 시 음성 경고 출력
                if CO2 > CO2_THRESHOLD:
                    print("경고: CO₂ 농도가 임계값을 초과했습니다! 즉시 환기가 필요합니다!")
                    play_warning_message()
    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")
        break
    except Exception as e:
        print(f"오류 발생: {e}")
        break
