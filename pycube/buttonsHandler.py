import time 
import pygame

class ButtonKeys(object):
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"
    X = "1"
    A = "2"
    B = "3"
    Y = "4"
    L1 = "6"
    L2 = "8"
    R1 = "5"
    R2 = "7"
    START = "9"
    SELECT = "10"
    L3 = "11"
    R3 = "12"

    
class ButtonsHandler(object):
    def __init__(self):
        self.got_joystick = False
        self.lastTime = time.time()
        try:
            for i in range(pygame.joystick.get_count()):
                joy = pygame.joystick.Joystick(i)
                #joy.init()
                if "Accelerometer" not in joy.get_name():
                    self.gamepad = joy
                    self.gamepad.init()
                    print("[*] Initializing Gamepad...")
                    self.got_joystick = True
                    print(f"[*] Initializing Gamepad {self.gamepad.get_name()}")
                else:
                    print("Only Accelerator Found")
        except pygame.error as e:
            print(e)
            print("[**] Joystick not found on the system")
        
    def getButtonsPressed(self):
        if (time.time() - self.lastTime) > 0.09 and self.got_joystick:
            buttons, analog = self.get()
            self.lastTime = time.time()
            return (buttons, analog)
        else:
            return ([],[])

    def __del__(self):
        try:
            if self.got_joystick:
                self.gamepad.quit()
        except:
            pass
    
    def get(self):
        if self.got_joystick:
            digital = []
            analog = [0,0,0,0]
            pygame.event.pump()
            LR, UD = self.gamepad.get_hat(0)
                        
            if LR == -1:
                digital.append('Left')
            elif LR == 1:
                digital.append('Right')

            if UD == -1:
                digital.append('Down')
            elif UD == 1:
                digital.append('Up')

            # Read input from the buttons
            for i in range(0, self.gamepad.get_numbuttons()):
                if  self.gamepad.get_button(i) == 1:
                    digital.append(str(i+1))

            # Read inputs from the two axes
            for i in range(0, self.gamepad.get_numaxes()):
                analog[i] = self.gamepad.get_axis(i)


            return (digital, analog)
        else:
            return ([],[])
    
    def test(self):
        while 1:
            print(self.get())

if __name__ == "__main__":
    pygame.init()
    b = ButtonsHandler()
    b.test()