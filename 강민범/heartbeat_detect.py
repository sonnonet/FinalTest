import serial
import time

# 아두이노가 연결된 시리얼 포트 설정
arduino_port = "COM3"  # Windows에서 포트를 확인 후 변경 (예: COM3)
baud_rate = 9600  # 아두이노와 동일한 속도

# 시리얼 포트 열기
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # 연결 안정화 대기

print("Heart rate monitoring started...")

try:
    while True:
        # 시리얼 데이터 읽기
        if ser.in_waiting > 0:
            heart_rate = ser.readline().decode('utf-8').strip()
            print(f"Heart Rate: {heart_rate} bpm")
        time.sleep(1)  # 1초 대기 (아두이노 전송 주기와 맞춤)
except KeyboardInterrupt:
    print("Monitoring stopped.")
finally:
    ser.close()  # 시리얼 포트 닫기
