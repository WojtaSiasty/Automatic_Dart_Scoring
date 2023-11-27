from menu import Menu
from camera import Camera

def main():
    cam1 = Camera(0)
    # cam2 = Camera(1,'sectors1')
    # cam3 = Camera(2,'sectors2')
    menu = Menu()
    menu.add_button_event(cam1.clear_arrays)

    while menu.window_exist():
        cam1.read_frame()
        # cam2.read_frame()
        # cam3.read_frame()

        if cam1.scores[0] != 0:
            menu.update_hit(1,cam1.scores[0])
        if cam1.scores[1] != 0:
            menu.update_hit(2,cam1.scores[1])
        if cam1.scores[2] != 0:
            menu.update_hit(3,cam1.scores[2])


        # cam2_hit1 = cam2.scores[0]
        # cam2_hit2 = cam2.scores[1]
        # cam2_hit3 = cam2.scores[2]

        # cam3_hit1 = cam3.scores[0]
        # cam3_hit2 = cam3.scores[1]
        # cam3_hit3 = cam3.scores[2]

        menu.window.update()



if __name__ == "__main__":
    main()
