
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt


from model.preprocessing import *

model = load_model("C:\\Users\\singh\\OneDrive\\Desktop\\Deep_Fakes\\FInal_Code\\model\\Model_Final.h5")

# video_file = "C:\\Users\\Janhavi Vidhate\\OneDrive\\Desktop\\DeepfakeDetection_WebApp\\model\\id0_id1_0002.mp4"

def prediction(video_file):
    frames = create_required_frames(video_file)
    predictions = []
    for frame in frames:
        frame1 = np.expand_dims(np.divide(frame, 255), axis=0)
        pr = model.predict(frame1)
        predictions.append(pr[0][0])
    
    avg_prob = sum(predictions)/len(predictions)
    if avg_prob <0.35:
        return 0, avg_prob
    else:
        return 1, avg_prob

def face_marker(single_frame, color, avg_prob):
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
  img = cv2.rectangle(single_frame, (x1, y1), (x2, y2), color=color, thickness=2)
  text = "Prob:" + str(avg_prob)
  img = cv2.putText(img, text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color=color, thickness=2)
  return img

def final_video_process(video_file):
    # Prediction
    predict, avg_prob = prediction(video_file)
    if predict == 0:
        color = (255, 0, 0)
    else:
        color = (0, 255, 0)

    # face detection and color the prediction
    final_frames = []
    cap = cv2.VideoCapture(video_file)
    succ, frame = cap.read()
    succ = True
    while succ:
        succ, frame = cap.read()
        if succ:    
            frame = face_marker(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), color, avg_prob)

            final_frames.append(frame)
            # if cv2.waitkey(10) == 27:
            #     break
        else:
            break
    return final_frames


#frames = final_video_process(video_file)
#p,a=prediction(video_file)
#print(p,(1-a))
# v = cv2.VideoCapture(video_file)
# height = int(v.get(3))
# width = int(v.get(4))
# channel = 3
# fps = 30
# sec = 8
# fourcc = cv2.VideoWriter_fourcc(*"MJPG")
# out = cv2.VideoWriter('project.avi', 0, 30, (width, height))

# for frame in frames:
#   out.write(frame)
# out.release()