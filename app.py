from flask import Flask, render_template, Response
from flask import request, jsonify
import cv2
import mediapipe as mp
import numpy as np
import threading
import pyttsx3
import time

app = Flask(__name__)

# ================= COMMANDS =================
commands = [
    "I need water",
    "I am hungry",
    "I need help",
    "I love you mom",
    "I am in pain",
    "Call the doctor"
]

current_index = 0

# ================= SPEECH SYSTEM =================
is_speaking = False

def speak_text(text):
    global is_speaking
    if is_speaking:
        return

    def run():
        global is_speaking
        is_speaking = True
        engine = pyttsx3.init()
        engine.setProperty('rate',150)
        engine.setProperty('volume',1)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        is_speaking = False

    threading.Thread(target=run, daemon=True).start()

# ================= MEDIAPIPE =================
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(refine_landmarks=True)

LEFT_EYE = [33,160,158,133,153,144]
RIGHT_EYE = [362,385,387,263,373,380]
LEFT_IRIS = [474,475,476,477]

# ================= TIMERS =================
blink_cooldown = 0
speech_lock = 0

# ⭐ NEW TIMERS FOR SLOW UI
gaze_hold_frames = 0
GAZE_HOLD_THRESHOLD = 12   # ~1 sec hold to change command

# ================= BLINK FUNCTION =================
def eye_aspect_ratio(eye):
    vertical = np.linalg.norm(eye[1]-eye[5]) + np.linalg.norm(eye[2]-eye[4])
    horizontal = np.linalg.norm(eye[0]-eye[3])
    return vertical / horizontal

# ================= CAMERA LOOP =================
def generate_frames():
    global blink_cooldown, speech_lock, current_index, gaze_hold_frames

    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame,1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)
        h,w,_ = frame.shape

        if blink_cooldown > 0:
            blink_cooldown -= 1
        if speech_lock > 0:
            speech_lock -= 1

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark

            def get_coords(ids):
                return np.array([(int(landmarks[i].x*w), int(landmarks[i].y*h)) for i in ids])

            left_eye = get_coords(LEFT_EYE)
            right_eye = get_coords(RIGHT_EYE)
            iris = get_coords(LEFT_IRIS)

            # ===== GREEN AI DOTS =====
            for p in np.concatenate((left_eye,right_eye,iris)):
                cv2.circle(frame, tuple(p), 2, (0,255,0), -1)

            # ===== BLINK DETECTION =====
            ear = (eye_aspect_ratio(left_eye)+eye_aspect_ratio(right_eye))/2

            if ear < 0.20 and blink_cooldown == 0 and speech_lock == 0:
                speak_text(commands[current_index])
                speech_lock = 90
                blink_cooldown = 40

            # ===== GAZE NAVIGATION (SLOW & SMOOTH) =====
            if speech_lock == 0:
                iris_center = iris.mean(axis=0)
                eye_center = left_eye.mean(axis=0)
                gaze_ratio = iris_center[0] - eye_center[0]

                # LOOK LEFT (HOLD)
                if gaze_ratio < -18:
                    gaze_hold_frames += 1
                    if gaze_hold_frames > GAZE_HOLD_THRESHOLD:
                        current_index = (current_index - 1) % len(commands)
                        gaze_hold_frames = 0

                # LOOK RIGHT (HOLD)
                elif gaze_ratio > 18:
                    gaze_hold_frames += 1
                    if gaze_hold_frames > GAZE_HOLD_THRESHOLD:
                        current_index = (current_index + 1) % len(commands)
                        gaze_hold_frames = 0

                else:
                    gaze_hold_frames = 0

        # ===== DISPLAY UI =====
        cv2.rectangle(frame,(20,20),(620,90),(255,255,255),-1)

        cv2.putText(frame,"Selected:",(30,55),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,0),2)

        cv2.putText(frame,commands[current_index],(30,80),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0),2)

        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')

# ================= ROUTES =================
# ===== BUTTON SPEAK ROUTE =====
@app.route('/speak', methods=['POST'])
def speak_from_button():
    data = request.get_json()
    text = data.get("text","")

    if text != "":
        speak_text(text)

    return jsonify({"status":"ok"})
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)