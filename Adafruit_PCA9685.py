import Adafruit_PCA9685
import math
from time import sleep
import utils
import detect

pwm = Adafruit_PCA9685.PCA9685(busnum=1)#IIC总线1
PI = math.pi
zero = [485, 600]
d = 486#实际像素与摄像头像素关系
pwm.set_pwm_freq(50)#设置周期为20ms

o_point = None
o_distance = None
distance_peer_pt_x = None
distance_peer_pt_y = None
last_angle_x = 0
last_angle_y = 0


def work(channel, angle):
    if channel == 0:
        if not -90 <= angle <= 90:
            print(f'[WRN] Invalid angle {angle} for X!')
            return
        angle = -angle
    if channel == 1:
        if not -90<= angle <= 90:
            print(f'[WRN] Invalid angle {angle} for Y!')
            return#失败输出信息
    
    global last_angle_x, last_angle_y
    if channel == 0:
        step_angle = (angle - last_angle_x) / 40
        last_angle_x = angle
    else:
        step_angle = (angle - last_angle_y) / 40
        last_angle_y = angle
    pass
    for i in range(1, 41):
        duty = int(4096 * ((step_angle * i * 7.4) + 1500) / 20000 + 0.5)
        while True:  # 如果设置PWM失败就继续尝试，直到设置成功
            try:
                pwm.set_pwm(channel, 0, duty)
                sleep(0.02)
                break
            except OSError as e:
                print(f'[WRN] OSError occurred!\n{e}')
                continue
    pass

    # duty = int(4096 * ((angle * 7.4) + 1500) / 20000 + 0.5)
    # while True:  # 如果设置PWM失败就继续尝试，直到设置成功
    #     try:
    #         pwm.set_pwm(channel, 0, duty)
    #         break
    #     except OSError as e:
    #         print('[WRN] OSError occurred!\n{e}')
    #         continue
def work2(angle_x, angle_y):
    if not -90 <= angle_x <= 90:
        print(f'[WRN] Invalid angle {angle_x} for X!')
        return
    if not -90 <= angle_y <= 90:
        print(f'[WRN] Invalid angle {angle_y} for Y!')
        return
    
    global last_angle_x, last_angle_y
    angle_x = -angle_x
    step_angle_x = (angle_x - last_angle_x) / 100
    step_angle_y = (angle_y - last_angle_y) / 100
    # step_angle_x = angle_x / 50
    # step_angle_y = angle_y / 50
    pass
    for i in range(1, 101):
        duty_x = int(4096 * (((last_angle_x + step_angle_x * i) * 7.4) + 1500) / 20000 + 0.5)
        duty_y = int(4096 * (((last_angle_y + step_angle_y * i) * 7.4) + 1500) / 20000 + 0.5)
        while True:  # 如果设置PWM失败就继续尝试，直到设置成功
            try:
                pwm.set_pwm(0, 0, duty_x)
                pwm.set_pwm(1, 0, duty_y)
                sleep(0.01)
                break
            except OSError:
                print(f'[WRN] OSError occurred!')
                continue
    pass
    last_angle_x = angle_x
    last_angle_y = angle_y

    # duty = int(4096 * ((angle * 7.4) + 1500) / 20000 + 0.5)
    # while True:  # 如果设置PWM失败就继续尝试，直到设置成功
    #     try:
    #         pwm.set_pwm(channel, 0, duty)
    #         break
    #     except OSError as e:
    #         print('[WRN] OSError occurred!\n{e}')
    #         continue


def init(goal, current):
    y_goal = (-math.atan((goal[1] - 600) / d)) * 180 * 1 / PI
    x_goal = (-math.atan((goal[0] - 485) / d)) * 180 * 1 / PI  # 计算目标角度
    y_current = (-math.atan((current[1] - 600) / d)) * 180 * 1 / PI
    x_current = (-math.atan((current[0] - 485) / d)) * 180 * 1 / PI  # 计算目前角度
    for temp in range(1, 41, 1):
        work(0, x_current + temp * (x_goal - x_current) / 40)
        work(1, y_current + temp * (y_goal - y_current) / 40)
        sleep(0.5)


def init2():
    global o_point, o_distance, distance_peer_pt_x, distance_peer_pt_y

    work2(0, 0)
    sleep(1)
    detect.capture()
    o_point = detect.get_current_location()
    o_distance = utils.get_distance()

    work2(15, 0)
    sleep(1)
    detect.capture()
    point = detect.get_current_location()
    d_pt = ((o_point[0] - point[0]) ** 2 + (o_point[1] - point[1]) ** 2) ** 0.5
    # print(d_pt)
    d_distance = o_distance * math.tan(math.radians(15))
    # print(d_distance)
    distance_peer_pt_x = d_distance / d_pt

    work2(0, 15)
    sleep(1)
    detect.capture()
    point = detect.get_current_location()
    d_pt = ((o_point[0] - point[0]) ** 2 + (o_point[1] - point[1]) ** 2) ** 0.5
    # print(d_pt)
    d_distance = o_distance * math.tan(math.radians(15))
    # print(d_distance)
    distance_peer_pt_y = d_distance / d_pt

def goto(point: tuple):
    d_pt_x = point[0] - o_point[0]
    d_distance_x = d_pt_x * distance_peer_pt_x
    d_pt_y = point[1] - o_point[1]
    d_distance_y = d_pt_y * distance_peer_pt_y
    angle_x = math.degrees(math.atan(d_distance_x / o_distance))
    angle_y = -math.degrees(math.atan(d_distance_y / o_distance))
    print(angle_x, angle_y)
    work2(angle_x, angle_y)
    sleep(1)

# work2(0, 0)
# sleep(1)
init2()
goto((246, 668))
goto((295, 669))
goto((299, 726))
goto((245, 725))
detect.capture()
work2(0, 0)

# work(0, 15)
# work(1, 0)
# sleep(0.5)
# detect.capture()
# print(f'0:\ndistance: {utils.get_distance()}\nray: {detect.get_current_location()}')
# work(0, -15)
# work(1, 0)
# sleep(0.5)
# detect.capture()
# print(f'-15:\ndistance: {utils.get_distance()}\nray: {detect.get_current_location()}')

# init(goal=(510, 561), current=detect.get_current_location())
# sleep(1)
# init(goal=(525, 470), current=detect.get_current_location())
# sleep(0.3)
# init(goal=(605, 580), current=detect.get_current_location())
# sleep(0.3)
# init(goal=(495, 650), current=detect.get_current_location())
# sleep(0.3)
# init(goal=(415, 553), current=detect.get_current_location())
# sleep(0.3)
# init(goal=(525, 470), current=detect.get_current_location())
# sleep(0.3)
