import cv2
import numpy as np
import pickle

class Camera():
    def __init__(self, cam_number):
    
        # Inicjalizacja kamery z ustawioną rozdzielczością
        self.cap = cv2.VideoCapture(cam_number)
        self.cap.set(3, 1920)  # Szerokość obrazu
        self.cap.set(4, 1080)  # Wysokość obrazu

        # Inicjalizacja detektora ruchu z dostosowanymi parametrami
        self.mog2 = cv2.createBackgroundSubtractorMOG2(history=10, varThreshold=50, detectShadows=False)

        # Lista przechowująca pozycje krzyżyków
        self.cross_positions = []

        # Czas ostatniego rysowania krzyżyka
        self.last_draw_time = 0

        self.scores = [0, 0, 0]

        # Filtracja konturów na podstawie obszaru obiektu
        self.min_contour_area = 10000  # Minimalne pole powierzchni
        self.max_contour_area = 35000  # Maksymalne pole powierzchni

        with open('sectors'+str(cam_number), 'rb') as f:
            self.sectorsWithScore = pickle.load(f)


    # Funkcja, która oblicza ogólny wynik
    def calculate_score(self, point):
        for sector, score in self.sectorsWithScore:
            # Konwertuj wielokąt sektora na listę punktów
            points = np.array(sector, dtype=np.int32)
            # Przekształć punkt na tuplę NumPy
            point = np.array(point, dtype=np.float32)
            # Sprawdź, w którym sektorze znajduje się punkt
            distance = cv2.pointPolygonTest(points, point, measureDist=True)
            # Jeśli punkt jest w sektorze, dodaj odpowiednią liczbę punktów do wyniku ogólnego
            if distance >= 0:
                return score


    def read_frame(self):
        # Odczyt klatki z kamery
        ret, frame = self.cap.read()

        # Wykrywanie obszarów ruchu przy użyciu detektora tła
        fgmask = self.mog2.apply(frame)

        # Filtrowanie Gaussa, aby usunąć szumy
        fgmask = cv2.GaussianBlur(fgmask, (5, 5), 0)

        # Znajdowanie konturów na masce
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            crosses = len(self.cross_positions)
            if crosses < 3:
                if self.min_contour_area < area < self.max_contour_area:
                    current_time = cv2.getTickCount()
                    if current_time - self.last_draw_time > cv2.getTickFrequency():
                        lowest_point = tuple(contour[contour[:, :, 1].argmax()][0])
                        self.cross_positions.append(lowest_point)
                        self.last_draw_time = current_time

                        score = self.calculate_score(lowest_point)
                        self.scores[crosses] = score

        
        # key = cv2.waitKey(30)
        # if key & 0xFF == ord('q'):
        #     break
        # elif key == ord('f'):
        #     cross_positions = []
        #     print(scores)
        #     scores = [0,0,0]

        # for position in self.cross_positions:
        #     cv2.drawMarker(frame, position, (0, 0, 255), markerType=cv2.MARKER_TILTED_CROSS, markerSize=20, thickness=2)

        #cv2.imshow('Camera View', frame)
        #cv2.imshow('Motion Detection', fgmask)


    # cap.release()
    # cv2.destroyAllWindows()
