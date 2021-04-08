import threading
import RPi.GPIO as GPIO
import time
import smbus
from time import sleep
import smbus
i=0

GPIO.setmode(GPIO.BOARD)
channel=16
#Relay_channel = [11, 12]
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(channel,GPIO.RISING)  # add rising edge detection on a channel
#do_something()

def irs_sensor():
    global i

    GPIO.event_detected(channel)
    #sensor = MLX90614()
    detection="false"
    time.sleep(0.1)
    #print("before detect",GPIO.event_detected(channel))
    try:
        edge=GPIO.wait_for_edge(channel, GPIO.FALLING)
        #print("edge",edge)
        if edge is None:
            print("channel is none")
        else :
            i+=1
            #print("edge detected")  
            #print(i,".kez ",'Button pressed')
            #print("sensor.get_obj_temp()",sensor.get_obj_temp(),"\n")
            
            try:
                edge2=GPIO.wait_for_edge(channel, GPIO.RISING)
                if edge is None:
                    print("edge2 isNone")
                    pass
                    #print("edge2 channel none")
                else:
                    print(i,".kez ",'Button pressed')
                    #print("else durumu")
            except RuntimeError:
                pass
    except:
        pass
    time.sleep(2)

if __name__=="__main__":
    print("ir sensor")
    while True:
        #global i
        t2=threading.Thread(target=irs_sensor)
        t2.start()
        t2.join()
        #print("t2 started")

        #irs_sensor()

 


