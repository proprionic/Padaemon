import pygame as pg
import pydotool

pydotool.init()
pg.init()
pg.joystick.init()

clock = pg.time.Clock()

smooth_x = 0.0
smooth_y = 0.0

BASE_SPEED = 800
DEADZONE = 0.1

button_map = {
    0: pydotool.left_click,
    1: pydotool.right_click,
}

joy = None


def curve(v):
    return (v * v) * (1 if v > 0 else -1)


while True:
    dt = clock.tick(120) / 1000

    for event in pg.event.get():
        if event.type == pg.JOYDEVICEADDED:
            joy = pg.joystick.Joystick(event.device_index)
            joy.init()

        if event.type == pg.JOYBUTTONDOWN:
            action = button_map.get(event.button)
            if action:
                action()

        if event.type == pg.JOYAXISMOTION:
            pass 
    if joy:
        # Left stick 
        axis_x = joy.get_axis(0)
        axis_y = joy.get_axis(1)

        if abs(axis_x) < DEADZONE:  
            axis_x = 0             
        if abs(axis_y) < DEADZONE: 
            axis_y = 0             

        smooth_x += (axis_x - smooth_x) * 0.2
        smooth_y += (axis_y - smooth_y) * 0.2

        speed_x = curve(smooth_x) * BASE_SPEED
        speed_y = curve(smooth_y) * BASE_SPEED

        dx = int(speed_x * dt)
        dy = int(speed_y * dt)

        if dx or dy:
            pydotool.mouse_move((dx, dy))

        # right stick
        scroll = joy.get_axis(4)

        if abs(scroll) > DEADZONE:
            pydotool.wheel_move(int(-scroll * 1.5)) 
