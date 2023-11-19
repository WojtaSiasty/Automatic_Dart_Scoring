from menu import Menu
from camera import Camera

def main():
    cam1 = Camera(0,'sectors1')
    menu = Menu()
    while menu.window_exist():
        cam1.read_frame()
        cam1_hit1 = cam1.scores[0]
        cam1_hit2 = cam1.scores[1]
        cam1_hit3 = cam1.scores[2]
        menu.window.update()

    #menu.destroy()
    #cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
