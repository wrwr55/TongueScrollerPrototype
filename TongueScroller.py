import cv2, mediapipe as mp, numpy as np, pyautogui, time
mp_face_mesh = mp.solutions.face_mesh
face_mesh =mp_face_mesh.FaceMesh(refine_landmarks=True)
cap =cv2.VideoCapture(0)

cooldown = 1.0
lastPress = 0
state = "neutral"

lip_base, chin_base = 0.0,0.0
alpha = 0.1

def regionColor(frame,landmark,w,h,size=15,y_offset=0):
    cx,cy =int(landmark.x * w), int(landmark.y * h + y_offset)
    x1,x2 = max(0,cx -size),min(w,cx+size)
    y1,y2 = max(0,cy - size), min(h,cy + size)
    roi = frame[y1:y2,x1:x2]
    if roi.size ==0:
        return 0, (x1,y1,x2,y2)
    hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    lower = np.array([0,100,80])
    upper = np.array([15,255,255])
    mask = cv2.inRange(hsv,lower,upper)
    red_ratio=cv2.countNonZero(mask) / (roi.shape[0] * roi.shape[1])
    return red_ratio,(x1,y1,x2,y2)

print("Facial trigger active. Press esc to quit")

if not cap.isOpened():
    print("No camera found.")
    exit()

while True:
    working, frame = cap.read()
    if not working:
        break
    
    frame = cv2.flip(frame,1)
    rgb= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    
    h,w,_ = frame.shape
    triggered = None
    
    if results.multi_face_landmarks:
        for f in results.multi_face_landmarks:
            lip = f.landmark[13]
            chin = f.landmark[152]
            
            lip_ratio,lip_box = regionColor(frame,lip,w,h,size=10)
            chin_ratio,chin_box = regionColor(frame,chin,w,h,size=18, y_offset=-30)
            
            cv2.rectangle(frame,(lip_box[0],lip_box[1]),(lip_box[2],lip_box[3]),(0,255,255),1)
            cv2.rectangle(frame,(chin_box[0],chin_box[1]),(chin_box[2],chin_box[3]),(0,255,255),1)
    
            if lip_base == 0:
                lip_base,chin_base= lip_ratio,chin_ratio
                
            lip_base = (1-alpha) * lip_base + alpha * lip_ratio
            chin_base = (1-alpha) * chin_base + alpha * chin_ratio
            
            
            lip_active =lip_ratio > lip_base +0.12
            chin_active = chin_ratio > chin_base +0.12
            
            now = time.time()
            if state == "neutral":
                if lip_active and now - lastPress > cooldown:
                    triggered ='lip'
                    state ='lip'
                    lastPress =now
                elif chin_active and now - lastPress > cooldown:
                    triggered ='chin'
                    state ='chin'
                    lastPress =now
            else:
                if not lip_active and not chin_active:
                    state = "neutral"
    if triggered == 'lip':
        cv2.putText(frame,"Upper Lip",(30,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2)
        pyautogui.press("down")
    elif triggered == 'chin':
        cv2.putText(frame,"Chin",(30,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2)
        pyautogui.press("up")
    
    cv2.putText(frame,f"State: {state}", (30,90),cv2.FONT_HERSHEY_SIMPLEX,1,(200,255,200),2)
    cv2.imshow("Click esc to exit", frame)
    
    if cv2.waitKey(5) & 0xFF == 27:
        break
    
cap.release()
cv2.destroyAllWindows()
                        
                    
                