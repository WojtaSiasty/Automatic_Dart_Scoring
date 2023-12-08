import cv2
import numpy as np
import pickle
import time
class Camera():
    def __init__(self, cam_number):
    
        # Inicjalizacja kamery z ustawioną rozdzielczością
        self.cap = cv2.VideoCapture(cam_number)
        self.cap.set(3, 1920)  # Szerokość obrazu
        self.cap.set(4, 1080)  # Wysokość obrazu

        # Inicjalizacja detektora ruchu z dostosowanymi parametrami
        self.mog2 = cv2.createBackgroundSubtractorMOG2(history=30, varThreshold=80, detectShadows=False)

        # Lista przechowująca pozycje krzyżyków
        self.cross_positions = []

        self.start_time = time.time()

        # Czas ostatniego rysowania krzyżyka
        self.last_draw_time = 0

        self.scores = [0, 0, 0]

        # Filtracja konturów na podstawie obszaru obiektu
        self.min_contour_area = 1000  # Minimalne pole powierzchni
        self.max_contour_area = 60000  # Maksymalne pole powierzchni

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
        ret, self.frame = self.cap.read()

        elapsed_time = time.time() - self.start_time

        # Wykrywanie obszarów ruchu przy użyciu detektora tła
        self.fgmask = self.mog2.apply(self.frame)

        # Filtrowanie Gaussa, aby usunąć szumy
        self.fgmask = cv2.GaussianBlur(self.fgmask, (5, 5), 0)

        # Znajdowanie konturów na masce
        contours, _ = cv2.findContours(self.fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if elapsed_time > 8:
            for contour in contours:
                area = cv2.contourArea(contour)
                crosses = len(self.cross_positions)
                if crosses < 3:
                    if self.min_contour_area < area < self.max_contour_area:
                        current_time = time.time()
                        if current_time - self.last_draw_time > 1.5:
                            self.lowest_point = tuple(contour[contour[:, :, 1].argmax()][0])
                            self.cross_positions.append(self.lowest_point)
                            self.last_draw_time = current_time

                            score = self.calculate_score(self.lowest_point)
                            self.scores[crosses] = score


    def clear_arrays(self, _):
        self.cross_positions = []
        self.scores = [0,0,0]

        # key = cv2.waitKey(30)
        # if key & 0xFF == ord('q'):
        #     break
        # elif key == ord('f'):
        #     cross_positions = []
        #     print(scores)
        #     scores = [0,0,0]
    def show_cam(self, name):
        for position in self.cross_positions:
            cv2.drawMarker(self.frame, position, (0, 0, 255), markerType=cv2.MARKER_TILTED_CROSS, markerSize=20, thickness=2)
        
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(name, 650, 500)
        cv2.namedWindow(name+'motion', cv2.WINDOW_NORMAL)
        cv2.resizeWindow(name+'motion', 650, 500)

        cv2.imshow(name, self.frame)
        cv2.imshow(name+'motion', self.fgmask)


    # cap.release()
    # cv2.destroyAllWindows()
