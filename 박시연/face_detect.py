import numpy as np
import cv2
import dlib
import sys
from math import atan2, degrees

# initialize face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

cap = cv2.VideoCapture('interview_face.mp4')

scaler = 0.5

while True:
    frame, img = cap.read()

    if not frame:
        break

    img = cv2.resize(img, (int(img.shape[1] * scaler), int(img.shape[0] * scaler)))
    original = img.copy()

    # 얼굴 포인트 찾기
    try:
        faces = detector(img)
        face = faces[0]
    except:
        break

    dlib_shape = predictor(img, face)
    shape_2d = np.array([[p.x, p.y] for p in dlib_shape.parts()])

    top_left = np.min(shape_2d, axis=0)
    bottom_right = np.max(shape_2d, axis=0)

    # np.int 대신 기본 int 사용
    center_X, center_Y = np.mean(shape_2d, axis=0).astype(int)

    # 얼굴 포인트 시각화
    for i in shape_2d:
        cv2.circle(img, center=tuple(i), radius=1, color=(255, 255, 255), thickness=2, lineType=cv2.LINE_AA)

    cv2.circle(img, center=tuple(top_left), radius=1, color=(255, 1, 1), thickness=2, lineType=cv2.LINE_AA)
    cv2.circle(img, center=tuple(bottom_right), radius=1, color=(255, 1, 1), thickness=2, lineType=cv2.LINE_AA)
    cv2.circle(img, center=tuple((center_X, center_Y)), radius=1, color=(1, 1, 255), thickness=2, lineType=cv2.LINE_AA)

    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' 키로 종료
        break

cap.release()
cv2.destroyAllWindows()
