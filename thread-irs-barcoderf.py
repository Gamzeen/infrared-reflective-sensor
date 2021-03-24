import time
import requests
import threading
import RPi.GPIO as GPIO
from time import sleep
from keyboard_alike import reader
from keyboard_alike.kullanici import kullanici_giris 
from keyboard_alike.serial_number import getserial
from keyboard_alike.choice import make_your_choice#enter choice
from firmId_direction import firm_id_and_direction
from temperature_sensor import MLX90614

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)  

rfbarcode_condition="false"
mesafe_condition="false"
i=0
b=0
y=0
#url_live="http://api-gw.aes.cmvteknoloji.com/secured/device/control/"
#url = "http://api-gw.aes.cmvteknoloji.com/public/login"

url_token = "http://api-gw.aes.cmvteknoloji.com/public/login"
url_card_control = "http://api-gw.aes.cmvteknoloji.com/secured/card/control"
url_live="http://api-gw.aes.cmvteknoloji.com/secured/device/control/"
url_local="http://localhost:9090/public/decrypt"
GPIO.setmode(GPIO.BOARD)
channel=16
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(channel,GPIO.RISING)  # add rising edge detection on a channel
#do_something()


class BarCodeReader(reader.Reader):
    pass

    
def irs_sensor():
    global mesafe_condition
    global rfbarcode_condition
    global i
    print("irs")
    z=0
    GPIO.event_detected(channel)
    sensor = MLX90614()
    detection="false"
    #print("before detect",GPIO.event_detected(channel))
    try:
        edge=GPIO.wait_for_edge(channel, GPIO.FALLING,timeout=5000)
        #print("edge",edge)
        if edge is None:
            print("channel is none")
        else :
            i+=1
            #print("edge detected")
            print(i,".kez ",'Button pressed')
    #        print("sensor.get_obj_temp()",sensor.get_obj_temp(),"\n")
            
            try:
                edge2=GPIO.wait_for_edge(channel, GPIO.RISING,timeout=5000)
                if edge is None:
                    pass
                    #print("edge2 channel none")
                else:
                    temperature=sensor.get_obj_temp()
                    print("sensor.get_obj_temp()",temperature,"\n")
                    if temperature<30:
                        print("irs_sensor","rfbarcode_condition ",rfbarcode_condition,"mesafe_condition",mesafe_condition)
                        
                        if rfbarcode_condition=="false" and mesafe_condition=="false" :
                            #b mesafe cagrilmamissa
                            #rf cagir
                            print("rfbarcode_condition:",rfbarcode_condition," mesafe_condition:",mesafe_condition)
                            print("mesafe istek atti")
                            mesafe_condition="true"
                            rfbarcode_condition="true"
                            barcode_reader()
                            mesafe_condition="false"
                            rfbarcode_condition="false"


                
                        if  rfbarcode_condition=="true" and mesafe_condition=="true":
                            #mesafe cagrilmissa
                            print("mesafe roleyi tetikliyor")  
                    else:
                        pass 
                   
            except RuntimeError:
                pass
    except:
        pass
    time.sleep(2)
        #print("edge falling and pass")


def barcode_reader():
    reader = BarCodeReader(0xac90, 0x3002, 84, 16, should_reset=True)
    firmId_direction=firm_id_and_direction()
    firm_id=firmId_direction[0]
    direction=firmId_direction[1]
    print("barkodddddddddddddd")
    #while True:
        
    reader.initialize()
    data=reader.read().strip()
        #value=data[0:13]
    value="8696630145727"#ust satirlari normal kodda aktif et
    print("value",value,type(value))
        #direction="EXIT"
    if value == "8696630145727":
        online_post(value,direction)
    else:
        value="5b3f932d4da1e436283ab9375845b61f6c9fad28f15b067a8c8df8a886932794e9df66230436a03a9f6613052a21595eb012169c79008f5611777723d64f3d6abc5f916ef6cbc9d228aace425c1928b8c66d859c3d2906d6df1a2c3f83c30700c8cedae174741c7593f4b115dedbfbcb80d0d44a33ea2763d8d4a5d4b95a8e4f7849c8372550994a759832b673e52d3ac75bd63f3881760e208565eeb56c9ce527ea79c429719553dbcae9f4bbe9baed5f3fa0477dc917b53e595c16a8176b4d383d03877c57777b858f8e2f6c42cf8103fa7dd4b7aa3b041428ad5e9630e704f1187ff6666d02ad95feac90929574a52b7a28a5e12042a2dd75aa316c1f7d68"

        local_post(value,direction)
            
    reader.disconnect()

def online_post(value,direction):
    global rfbarcode_condition
    global mesafe_condition
    response=13
    #print("reuresponse",response)
    #print("barcode_reader","rfbarcode_condition ",rfbarcode_condition,"mesafe_condition",mesafe_condition)
    if response==1 :
        if rfbarcode_condition=="false" and mesafe_condition=="false":
            #a rf daha once cagrilmamissa
            #mesafe cagir
            print("rfbarcode_condition:",rfbarcode_condition," mesafe_condition:",mesafe_condition)
            print("rfid istek atti")
            rfbarcode_condition="true"
            mesafe_condition="true"
            print("rfbarcode_condition:",rfbarcode_condition," mesafe_condition:",mesafe_condition)
            irs_sensor()
            rfbarcode_condition="false"
            mesafe_condition="false"
            print("rfbarcode_condition:",rfbarcode_condition," mesafe_condition:",mesafe_condition)

        if rfbarcode_condition=="true" and mesafe_condition=="true":
            #rf cagrilmissa
            print("rfid role tetikliyor ")
    else:
        pass 

if __name__ == "__main__":
    
    #barcode_reader()
    i=0
    while i<3:
        t1=threading.Thread(target=irs_sensor,daemon="True")
        #time.sleep(2)
        t2=threading.Thread(target=barcode_reader,daemon="True")
        t1.start()
        t2.start()
        #t1.join()
        t2.join()
        i+=1
        #t3.join()
        #t4.join()
