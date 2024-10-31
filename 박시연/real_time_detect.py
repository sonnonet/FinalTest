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