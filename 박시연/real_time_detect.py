import cv2
import dlib
import imutils
from imutils import face_utils
from scipy.spatial import distance as dist


# EAR를 계산하는 함수
def eye_aspect_ratio(eye):
    p2_minus_p6 = dist.euclidean(eye[1], eye[5])
    p3_minus_p5 = dist.euclidean(eye[2], eye[4])
    p1_minus_p4 = dist.euclidean(eye[0], eye[3])
    ear = (p2_minus_p6 + p3_minus_p5) / (2.0 * p1_minus_p4)
    return ear


# 상수 및 변수 초기화
FACIAL_LANDMARK_PREDICTOR = "shape_predictor_68_face_landmarks.dat"
MINIMUM_EAR = 0.2  # EAR 임계값
MAXIMUM_FRAME_COUNT = 10  # 졸음으로 간주할 연속 프레임 수

# dlib 얼굴 감지기 및 랜드마크 예측기 초기화
faceDetector = dlib.get_frontal_face_detector()
landmarkFinder = dlib.shape_predictor(FACIAL_LANDMARK_PREDICTOR)

# 웹캠 피드 가져오기
webcamFeed = cv2.VideoCapture(0)

# 눈의 랜드마크 인덱스 설정
(leftEyeStart, leftEyeEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rightEyeStart, rightEyeEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# 졸음 감지 카운터 초기화
EYE_CLOSED_COUNTER = 0

try:
    while True:
        (status, image) = webcamFeed.read()
        if not status:
            break

        # 이미지 크기 조정 및 회색조 변환
        image = imutils.resize(image, width=800)
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 얼굴 검출
        faces = faceDetector(grayImage, 0)

        for face in faces:
            # 얼굴 랜드마크 찾기
            faceLandmarks = landmarkFinder(grayImage, face)
            faceLandmarks = face_utils.shape_to_np(faceLandmarks)

            # 왼쪽, 오른쪽 눈의 좌표 가져오기
            leftEye = faceLandmarks[leftEyeStart:leftEyeEnd]
            rightEye = faceLandmarks[rightEyeStart:rightEyeEnd]

            # EAR 계산
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0

            # 눈 주위에 윤곽선 그리기
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(image, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(image, [rightEyeHull], -1, (0, 255, 0), 1)

            # EAR 임계값 체크
            if ear < MINIMUM_EAR:
                EYE_CLOSED_COUNTER += 1
            else:
                EYE_CLOSED_COUNTER = 0

            # EAR 값 출력
            cv2.putText(image, f"EAR: {round(ear, 2)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # 졸음 경고
            if EYE_CLOSED_COUNTER >= MAXIMUM_FRAME_COUNT:
                cv2.putText(image, "Warning!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # 프레임 출력
        cv2.imshow("Frame", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Error! : {e}")

finally:
    webcamFeed.release()
    cv2.destroyAllWindows()
