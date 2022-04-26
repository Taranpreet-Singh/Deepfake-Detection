import numpy as np
import cv2
import dlib
import PIL
from PIL import Image
import glob
# face detector and landmarks predictor
shape_pred_loc = "C:\\Users\\singh\\OneDrive\\Desktop\\Deep_Fakes\\FInal_Code\\model\\shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_pred_loc)

# Face detection
def face_detection(single_frame):
  gray = cv2.cvtColor(single_frame, cv2.COLOR_RGB2GRAY)
  face_cords = detector(gray)
  if len(face_cords) == 0:
    return 0
  face_cord = face_cords[0]
  x1 = face_cord.left()
  y1 = face_cord.top()
  x2 = face_cord.right()
  y2 = face_cord.bottom()
  # print(y1, y2, x1, x2)
  face = single_frame[y1:y2, x1:x2]
  return [gray, face_cord]  # gray face, coordinates for actual image

def final_image_extraction(frame):
  try:
    gray, face_cord = face_detection(frame)
  except:
    return 0 
  # if len(face_cord) == 0:
  #   return 0
  try:
    landmarks = predictor(gray, face_cord)

    # Eyes Section
    e_req_points = [17, 19, 24, 26, 29]   
    e_point_cords = []
    for i in e_req_points:
      x = landmarks.part(i).x
      y = landmarks.part(i).y
      e_point_cords.append([x, y])
    x1 = e_point_cords[0][0]
    y1 = min(e_point_cords[1][1], e_point_cords[2][1])
    x2 = e_point_cords[3][0]
    y2 = e_point_cords[4][1]
    eyes = frame[y1:y2, x1:x2, :]  
    new_eyes = cv2.resize(eyes, (120, 60))

    # Mouth Section
    m_req_points = [33, 36, 45, 55, 56, 57, 58, 59]   
    m_point_cords = []
    for i in m_req_points:
      x = landmarks.part(i).x
      y = landmarks.part(i).y
      m_point_cords.append([x, y])
    x1 = m_point_cords[1][0]
    y1 = m_point_cords[0][1]+5
    x2 = m_point_cords[2][0]
    y2 = max(m_point_cords[3][1], m_point_cords[4][1], m_point_cords[5][1], m_point_cords[6][1], m_point_cords[7][1]) + 10
    mouth = frame[y1:y2, x1:x2, :]
    new_mouth = cv2.resize(mouth, (120, 60))

    # Cocatination Section
    concate = cv2.vconcat([new_eyes, new_mouth])
    new_concate = cv2.resize(concate, (120, 120))
    return new_concate
  except:   
    return []

def create_required_frames(video):
    cap = cv2.VideoCapture(video)
    frames = []
    succ, frame = cap.read()
    succ = True
    while succ:
        succ, frame = cap.read()
        if succ:    
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
            # if cv2.waitkey(10) == 27:
            #     break
        else:
            break
    final_frames = []
    for frame in frames[::15]:
        img = final_image_extraction(frame) 
        if type(img) == np.ndarray:
          final_frames.append(img)

    return final_frames
