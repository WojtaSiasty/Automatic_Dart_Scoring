import cv2
import numpy as np
import time
import pickle

cap = cv2.VideoCapture(0)
cap.set(3, 1920)  # Szerokość obrazu
cap.set(4, 1080)  # Wysokość obrazu

# Rozpocznij pomiar czasu
start_time = time.time()

sectors = []
path = []
def mousePoints(event, x,y,flags,params):
    if event == cv2.EVENT_LBUTTONDOWN:
        path.append([x,y])


while True:
    ret, img = cap.read()

    # Sprawdź, czy minęła już 1 sekunda
    elapsed_time = time.time() - start_time
    if elapsed_time >= 1:
        break

while True:
    for point in path:
        cv2.circle(img,point,4,(0,0,255),cv2.FILLED)
    
    pts = np.array(path,np.int32).reshape((-1,1,2))
    img = cv2.polylines(img, [pts], True, (255,0,0), 2)

    cv2.imshow('Board', img)
    cv2.setMouseCallback('Board', mousePoints)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key == ord('f'):
        score = int(input("Enter Score: "))
        sectors.append([path,score])
        print("Total sectors: ",len(sectors))
        path = []
    elif key == ord('s'):
        with open('sectors','wb') as f:
            print(sectors)
            pickle.dump(sectors,f)
        break


# Zwolnij zasoby i zamknij okno OpenCV
cap.release()
cv2.destroyAllWindows()
