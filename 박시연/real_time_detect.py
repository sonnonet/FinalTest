import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist

# EAR 계산 함수 정의
def eye_aspect_ratio(eye):
    # 눈의 수직 거리
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    # 눈의 가로 거리
    C = dist.euclidean(eye[0], eye[3])
    # EAR 계산
    ear = (A + B) / (2.0 * C)
    return ear

# 초기 변수 설정
EYE_AR_THRESH = 0.3  # EAR 임계값
EYE_AR_CONSEC_FRAMES = 48  # 졸음으로 인식하기 위한 프레임 연속 수
counter = 0  # 프레임 카운터 초기화
ALARM_ON = False  # 알람 상태 초기화

# dlib의 얼굴 검출기와 랜드마크 예측기 로드
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# 좌/우 눈의 랜드마크 인덱스
(lStart, lEnd) = (42, 48)
(rStart, rEnd) = (36, 42)

# 카메라 초기화
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 프레임을 회색조로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 검출
    faces = detector(gray, 0)

    for face in faces:
        # 랜드마크 검출
        shape = predictor(gray, face)
        shape = np.array([[p.x, p.y] for p in shape.parts()])

        # 좌/우 눈 랜드마크 추출
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        # 좌/우 눈 EAR 계산
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # 평균 EAR 계산
        ear = (leftEAR + rightEAR) / 2.0

        # 눈 외곽선 그리기
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        # EAR 임계값 비교
        if ear < EYE_AR_THRESH:
            counter += 1
            # 연속된 프레임이 임계값을 초과하면 알람 상태로 설정
            if counter >= EYE_AR_CONSEC_FRAMES:
                if not ALARM_ON:
                    ALARM_ON = True
                    # 알람 소리 출력 (라즈베리파이에서 설정 필요)
                    print("Drowsiness Alert!")  # 여기서 부저나 알람 소리를 추가 가능
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            counter = 0
            ALARM_ON = False

    # 결과 프레임 표시
    cv2.imshow("Drowsiness Detector", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()