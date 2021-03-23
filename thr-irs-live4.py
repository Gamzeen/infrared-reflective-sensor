import requests
import threading
import RPi.GPIO as GPIO
import time
import smbus
from time import sleep
import smbus
i=0
b=0
y=0
url_live="http://api-gw.aes.cmvteknoloji.com/secured/device/control/"
url = "http://api-gw.aes.cmvteknoloji.com/public/login"

GPIO.setmode(GPIO.BOARD)
channel=16
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(channel,GPIO.RISING)  # add rising edge detection on a channel
#do_something()

class MLX90614():
    MLX90614_RAWIR1=0x04
    MLX90614_RAWIR2=0x05
    MLX90614_TA=0x06
    MLX90614_TOBJ1=0x07
    MLX90614_TOBJ2=0x08
    MLX90614_TOMAX=0x20
    MLX90614_TOMIN=0x21
    MLX90614_PWMCTRL=0x22
    MLX90614_TARANGE=0x23
    MLX90614_EMISS=0x24
    MLX90614_CONFIG=0x25
    MLX90614_ADDR=0x0E
    MLX90614_ID1=0x3C
    MLX90614_ID2=0x3D
    MLX90614_ID3=0x3E
    MLX90614_ID4=0x3F
    comm_retries = 5
    comm_sleep_amount = 0.1

    def __init__(self, address=0x5a, bus_num=1):
        self.bus_num = bus_num
        self.address = address
        self.bus = smbus.SMBus(bus=bus_num)

    def read_reg(self, reg_addr):
        err = None
        for i in range(self.comm_retries):
            try:
                return self.bus.read_word_data(self.address, reg_addr)
            except IOError as e:
                err = e
                #"Rate limiting" - sleeping to prevent problems with sensor
                #when requesting data too quickly
                sleep(self.comm_sleep_amount)
        #By this time, we made a couple requests and the sensor didn't respond
        #(judging by the fact we haven't returned from this function yet)
        #So let's just re-raise the last IOError we got
        raise err

    def data_to_temp(self, data):
        temp = (data*0.02) - 273.15
        return temp

    def get_amb_temp(self):
        data = self.read_reg(self.MLX90614_TA)
        return self.data_to_temp(data)

    def get_obj_temp(self):
        data = self.read_reg(self.MLX90614_TOBJ1)
        return self.data_to_temp(data)



def request_token():
    
    username="kutsal"
    password="kutsal"
    payload = "{ \n    \"username\": \""+username+"\",\n    \"password\": \""+password+"\"\n}"
    headers = {
        'Cmv-Application-Name': 'ReDesk',
        'Content-Type': 'application/json'
        }
    response = requests.request("POST", url, headers=headers, data = payload)
    #print("response",response)
    response_utf =response.text.encode('utf8')
    #print("response_utf: ",response_utf)
    #print("")

    sresponse=str(response_utf) 
    #print("String str response ",sresponse)
    #print("")
    split_sresponse=sresponse.split('"')
    response_token=split_sresponse[5]
    #print(response_token)
    return response_token

def alive():
    response_token=request_token()
    clientId="SSCB"
    firmId="115"
    payload = "{ \n    \"clientId\": \""+clientId+"\",\n    \"firmId\": \""+firmId+"\"\n}"
    headers = {
            'Authorization': 'a',
            'Content-Type': 'application/json'
            }
    response_token="Bearer "+response_token
    headers['Authorization']=response_token

    response = requests.request("POST", url_live,headers=headers, data = payload)
    #print("response",response)
    response_utf =response.text.encode('utf8')
    #print("response_utf",response_utf)
    
def irs_sensor():
    global i
    z=0
    GPIO.event_detected(channel)
    sensor = MLX90614()
    detection="false"
    #print("before detect",GPIO.event_detected(channel))
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
                print("sensor.get_obj_temp()",sensor.get_obj_temp(),"\n")
                pass
        except RuntimeError:
            pass
    time.sleep(2)
        #print("edge falling and pass")

def countdown(): 
    t=15
    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        #print(timer, end="\r") 
        time.sleep(1) 
        t -= 1
        if t==0:
            live_At=alive()
            print("live atti")
             
    #print('Fire in the hole!!',"\n") 
  
  
# input time in seconds 
#t = input("Enter the time in seconds: ") 
  
def bak():
    global b
    b+=1
    print("bak",b)
    
    time.sleep(1)
  
def yaz():
    global y
    y+=1
    print("yaz",y)
    
    time.sleep(1)
if __name__ == "__main__":
    
    #barcode_reader()
    
    while True:
        t1=threading.Thread(target=countdown,daemon="True")
        t2=threading.Thread(target=irs_sensor)
        t3=threading.Thread(target=bak,daemon="True")
        t4=threading.Thread(target=yaz)
        #print("t2 started")


        #print("t1 started")
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        #t1.join()
        t4.join()#parcaciklarin sonlandirilmasini bekliyor
        #t3.join()
        #t4.join()



