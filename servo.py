try:
    import RPi.GPIO as GPIO
    import math
    from time import sleep
except KeyboardInterrupt:
    print("import defeat")

PI=math.pi
servo_pinx=35
servo_piny=37

judge_circl=0
distance=1000
angle_x_now=0.0000
angle_y_now=0.0000
angle_x_after=0.0000
angle_y_after=0.0000
ox=300
oy=300

def servo_init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(servo_pinx, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(servo_piny, GPIO.OUT, initial=GPIO.HIGH)
    servox = GPIO.PWM(servo_pinx, 50)
    servoy = GPIO.PWM(servo_piny, 50)
    servox.start(7.25)
    servoy.start(7.25) 
    sleep(0.2)
    servox.start(7.125)
    sleep(0.1)
    servoy.start(7.375)
    sleep(0.1)
def servo_work(x0,y0,x1,y1): 
    global ox,oy,judge_circl,angle_x,distance
    if judge_circl==0:
        temp0=((x0-ox)**2+distance**2)**(1/2)
        temp1=((x1-ox)**2+distance**2)**(1/2)
        temp2=(temp0**2+temp1**2-(x1-x0)**2)/2/temp0/temp1
        angle_x=math.acos(temp2)*180/PI+angle_x
        temp0=((x0-ox)**2+distance**2)**(1/2)
        temp1=((x1-ox)**2+distance**2)**(1/2)
        temp2=(temp0**2+temp1**2-(x1-x0)**2)/2/temp0/temp1
        angle_x=math.acos(temp2)*180/PI+angle_x
    elif judge_circl==1:
        print("degree is ",angle_x)
        return
    
servo_init()
    


        servoy.ChangeDutyCycle(0)
    for dc in range(1,251,1):
        servox.ChangeDutyCycle(7.25-dc*0.001)
        sleep(0.01)
        servox.ChangeDutyCycle(0)
    for dc in range(1,251,1):
        servoy.ChangeDutyCycle(7.25+dc*0.002)
        sleep(0.01)
        servoy.ChangeDutyCycle(0)
    for dc in range(1,251,1):
        servox.ChangeDutyCycle(7+0.002*dc)
        sleep(0.01)
        servox.ChangeDutyCycle(0)
    for dc in range(1,251,1):
        servoy.ChangeDutyCycle(7.75-dc*0.002)
        sleep(0.01)
        servoy.ChangeDutyCycle(0)
    for dc in range(1,251,1):
        servox.ChangeDutyCycle(7.5-0.001*dc)
        sleep(0.01)
        servox.ChangeDutyCycle(0)