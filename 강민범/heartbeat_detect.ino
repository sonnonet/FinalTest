#define SENSOR_PIN A0  // 심박 센서가 연결된 핀
int heartRate;

void setup() {
  Serial.begin(9600);  // 시리얼 통신 시작 (9600bps)
  pinMode(SENSOR_PIN, INPUT);
}

void loop() {
  // 센서 값 읽기
  int sensorValue = analogRead(SENSOR_PIN);

  // 센서 값을 심박수 값으로 변환 (단순 예제)
  heartRate = map(sensorValue, 0, 1023, 60, 100); // 실제로는 더 복잡한 계산이 필요할 수 있음

  // 측정된 심박수를 시리얼 포트를 통해 전송
  Serial.println(heartRate);

  delay(1000); // 1초 대기
}
