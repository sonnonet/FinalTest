import cv2
import dlib
import imutils
from imutils import face_utils
from scipy.spatial import distance as dist

# EAR을 계산하는 함수
def eye_aspect_ratio(eye):
    p2_minus_p6 = dist.euclidean(eye[1], eye[5])
    p3_minus_p5 = dist.euclidean(eye[2], eye[4])
    p1_minus_p4 = dist.euclidean(eye[0], eye[3])
    ear = (p2_minus_p6 + p3_minus_p5) / (2.0 * p1_minus_p4)
    return ear

# 초기 설정
FACIAL_LANDMARK_PREDICTOR = "shape_predictor_68_face_landmarks.dat"
MINIMUM_EAR = 0.2
MAXIMUM_FRAME_COUNT = 5

# dlib 초기화
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor(FACIAL_LANDMARK_PREDICTOR)

# 웹캠 피드 시작
webcam_feed = cv2.VideoCapture(0)

# 눈 랜드마크 인덱스
(leftEyeStart, leftEyeEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rightEyeStart, rightEyeEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# 졸음 감지 카운터
eye_closed_counter = 0

def process_frame(frame):
    """프레임을 처리하여 EAR을 계산하고 졸음 경고를 표시합니다."""
    global eye_closed_counter

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray_frame, 0)

    for face in faces:
        landmarks = landmark_predictor(gray_frame, face)
        landmarks = face_utils.shape_to_np(landmarks)

        left_eye = landmarks[leftEyeStart:leftEyeEnd]
        right_eye = landmarks[rightEyeStart:rightEyeEnd]

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0

        cv2.putText(frame, f"EAR: {round(ear, 2)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        left_eye_hull = cv2.convexHull(left_eye)
        right_eye_hull = cv2.convexHull(right_eye)
        cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)

        if ear < MINIMUM_EAR:
            eye_closed_counter += 1
        else:
            eye_closed_counter = 0

        if eye_closed_counter >= MAXIMUM_FRAME_COUNT:
            cv2.putText(frame, "DROWSINESS ALERT!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

    return frame

try:
    while True:
        status, frame = webcam_feed.read()
        if not status:
            print("웹캠에서 프레임을 읽을 수 없습니다.")
            break

        frame = imutils.resize(frame, width=800)
        processed_frame = process_frame(frame)

        cv2.imshow("Drowsiness Detection", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    # 리소스 해제
    webcam_feed.release()
    cv2.destroyAllWindows()
