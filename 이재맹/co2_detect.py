import serial  # Zigbee 통신을 위한 serial 라이브러리
import time  # 시간 지연을 위한 time 라이브러리

# XBee Zigbee 모듈 설정
ser = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)  # 통신 안정화를 위해 2초 대기 (모듈 초기화 시간)

# CO₂ 농도 임계값 설정
CO2_THRESHOLD = 1000


def read_co2():
    """
    Zigbee 모듈을 통해 CO₂ 농도를 주기적으로 읽고 임계값 초과 시 경고 메시지 출력.
    """
    try:
        while True:  # 무한 루프를 돌며 CO₂ 농도 데이터를 계속 수신
            if ser.in_waiting > 0:  # 수신된 데이터가 있을 때만 읽음
                data = ser.read(ser.in_waiting)  # 수신된 모든 데이터를 읽음

                # CO₂ 농도 값 파싱
                co2_ppm = parse_co2_data(data)

                # 현재 CO₂ 농도 출력
                print(f"현재 CO₂ 농도: {co2_ppm} ppm")

                # CO₂ 농도가 임계값을 초과하면 경고 메시지 출력
                if co2_ppm > CO2_THRESHOLD:
                    print("경고: CO₂ 농도가 높습니다. 환기 필요!")
            time.sleep(1)  # 1초마다 CO₂ 농도 측정
    except KeyboardInterrupt:  # 프로그램을 중단할 때
        ser.close()  # 시리얼 포트를 닫아 통신 종료


def parse_co2_data(data):
    """
    수신된 데이터를 파싱하여 CO₂ 농도(ppm)를 반환하는 함수.
    """
    co2_ppm = int.from_bytes(data[3:5], byteorder='big')  # 'big'은 빅 엔디안 형식으로 변환
    return co2_ppm


# CO₂ 농도 측정 시작
# read_co2 함수는 Zigbee 통신으로 CO₂ 데이터를 수신하고 주기적으로 출력
read_co2()
