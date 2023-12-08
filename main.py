from menu import Menu
from camera import Camera


def main():
    cam1 = Camera(0)
    cam2 = Camera(1)
    cam3 = Camera(2)
    menu = Menu()
    menu.add_button_event(cam1.clear_arrays)
    menu.add_button_event(cam2.clear_arrays)
    menu.add_button_event(cam3.clear_arrays)
    
    while menu.window_exist():
        cam1.read_frame()
        cam2.read_frame()
        cam3.read_frame()
        cam1.show_cam('Kamera1')
        cam2.show_cam('Kamera2')
        cam3.show_cam('Kamera3')

        cam2_hit1 = cam2.scores[0]
        cam2_hit2 = cam2.scores[1]
        cam2_hit3 = cam2.scores[2]

        cam3_hit1 = cam3.scores[0]
        cam3_hit2 = cam3.scores[1]
        cam3_hit3 = cam3.scores[2]

        #współrzędne y kamer
        ycam1 = [y for x, y in cam1.cross_positions]
        ycam2 = [y for x, y in cam2.cross_positions]
        ycam3 = [y for x, y in cam3.cross_positions]

        print('Kamera 1: ',ycam1)
        print('Kamera 2: ',ycam2)
        print('Kamera 3: ',ycam3)


        #Sprawdzenie czy x-y się zaznaczyły
        #trzeci się nie zaznaczył
        for i in range(3):
            if cam1.scores[i] != 0 and cam2.scores[i] != 0:
                if cam3.scores[i] == 0:
                    if ycam1[i] < ycam2[i]:
                        cam3.scores[i] = cam1.scores[i]
                        cam3.cross_positions.append(cam1.lowest_point)
                    else:
                        cam3.scores[i] = cam2.scores[i]
                        cam3.cross_positions.append(cam2.lowest_point)
            
            #drugi się nie zaznaczył
                elif cam1.scores[i] != 0 and cam3.scores[i] != 0:
                    if cam2.scores[i] == 0:
                        if ycam1[i] < ycam3[i]:
                            cam2.scores[i] = cam1.scores[i]
                            cam2.cross_positions.append(cam1.lowest_point)
                        else:
                            cam2.scores[i] = cam3.scores[i]
                            cam2.cross_positions.append(cam1.lowest_point)

            #pierwszy się nie zaznaczył
                else:
                    if cam1.scores[i] == 0:
                        if ycam2[i] < ycam3[i]:
                            cam1.scores[i] = cam2.scores[i]
                            cam1.cross_positions.append(cam1.lowest_point)
                        else:
                            cam1.scores[i] = cam3.scores[i]
                            cam1.cross_positions.append(cam3.lowest_point)


            #warunki
            #wszystkie sie zgadzaja
            if  cam1.scores[i] != 0 and cam2.scores[i] != 0 and cam3.scores[i] != 0:
                if cam1.scores[i] == cam2.scores[i] and cam1.scores[i] == cam3.scores[i]:
                    menu.update_hit(i+1,cam1.scores[i])
                elif cam1.scores[i] == cam2.scores[i] and cam1.scores[i] != cam3.scores[i]:
                    menu.update_hit(i+1,cam1.scores[i])
                elif cam1.scores[i] != cam2.scores[i] and cam1.scores[i] == cam3.scores[i]:
                    menu.update_hit(i+1,cam1.scores[i])   
                else:
                    menu.update_hit(i+1,cam2.scores[i])
        
            #wszystkie inne
            #wynik 1
            if  cam1.scores[i] != 0 and cam2.scores[i] != 0 and cam3.scores[i] != 0:
                if cam1.scores[i] != cam2.scores[i] and cam2.scores[i] != cam3.scores[i]:
                    #pierwsza najnizsza
                    if  ycam1[i] > ycam2[i] and  ycam1[i] > ycam3[i]:
                        menu.update_hit(i+1,cam1.scores[i])
                    #trzecia najnizsza
                    elif  ycam1[i] > ycam2[i] and  ycam1[i] < ycam3[i]:
                        menu.update_hit(i+1,cam3.scores[i])
                    #druga najnizsza
                    else:
                        menu.update_hit(i+1,cam2.scores[i])


        menu.window.update()



if __name__ == "__main__":
    main()
