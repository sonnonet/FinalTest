import serial  # Zigbee 통신을 위한 serial 라이브러리
import time  # 시간 지연을 위한 time 라이브러리
import pygame  # 오디오 재생을 위한 라이브러리

# XBee Zigbee 모듈 설정
# '/dev/ttyUSB0'은 라즈베리파이에 연결된 XBee Zigbee 모듈의 포트 이름입니다.
# baudrate는 XBee 모듈과의 통신 속도입니다. (9600은 기본 속도)
ser = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)  # 통신 안정화를 위해 2초 대기 (모듈 초기화 시간)

# Pygame 초기화 및 경고 음성 파일 로드
pygame.mixer.init()
pygame.mixer.music.load("warning.mp3")  # "환기를 좀 하세요" 음성 파일 경로

# CO₂ 농도 임계값 설정
CO2_THRESHOLD = 1000  # 임계값 (예: 1000ppm)


def read_co2():
    """
    Zigbee 모듈을 통해 CO₂ 농도를 주기적으로 읽고 임계값 초과 시 경고음 재생.
    """
    try:
        while True:  # 무한 루프를 돌며 CO₂ 농도 데이터를 계속 수신
            if ser.in_waiting > 0:  # 수신된 데이터가 있을 때만 읽음
                data = ser.read(ser.in_waiting)  # 수신된 모든 데이터를 읽음

                # CO₂ 농도 값 파싱
                co2_ppm = parse_co2_data(data)

                # 현재 CO₂ 농도 출력
                print(f"현재 CO₂ 농도: {co2_ppm} ppm")

                # CO₂ 농도가 임계값을 초과하면 경고 음성 출력
                if co2_ppm > CO2_THRESHOLD:
                    print("경고: CO₂ 농도가 높습니다. 환기 필요!")
                    play_warning()  # 경고 음성 재생 함수 호출
            time.sleep(1)  # 1초마다 CO₂ 농도 측정
    except KeyboardInterrupt:  # 프로그램을 중단할 때
        ser.close()  # 시리얼 포트를 닫아 통신 종료


def parse_co2_data(data):
    """
    수신한 Zigbee 데이터에서 CO₂ 농도 값을 추출하는 함수.
    데이터 시트를 참고하여 CO₂ 농도가 위치한 바이트를 찾아 파싱.

    Parameters:
        data (bytes): Zigbee 모듈로부터 수신된 데이터

    Returns:
        int: 추출된 CO₂ 농도 값 (ppm)
    """
    # 데이터 시트에 따라 데이터 형식이 다를 수 있습니다.
    # 예시: data[3:5]에 CO₂ 농도 데이터가 있다고 가정하고 추출
    # 'big'은 빅 엔디안 형식으로 변환
    co2_ppm = int.from_bytes(data[3:5], byteorder='big')
    return co2_ppm


def play_warning():
    """
    경고 음성을 재생하는 함수.
    """
    if not pygame.mixer.music.get_busy():  # 현재 음성이 재생 중이 아닐 때만 재생
        pygame.mixer.music.play()


# CO₂ 농도 측정 시작
# read_co2 함수는 Zigbee 통신으로 CO₂ 데이터를 수신하고 주기적으로 출력
read_co2()
