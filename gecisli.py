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
from ultrasonic_sensor import ultrasonic_distance_sensor

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)  
Relay_channel = [11, 12]

rfbarcode_condition="false"
mesafe_condition="false"

url_token = "http://api-gw.aes.cmvteknoloji.com/public/login"
url_card_control = "http://api-gw.aes.cmvteknoloji.com/secured/card/control"
url_live="http://api-gw.aes.cmvteknoloji.com/secured/device/control/"
url_local="http://localhost:9090/public/decrypt"

def relay_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Relay_channel[0], GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(Relay_channel[1], GPIO.OUT, initial=GPIO.HIGH)
    time.sleep(2)
def relay(Relay):  
    print ('...Relay channel %d on' % (Relay))
    GPIO.output(Relay_channel[Relay], GPIO.LOW)
    time.sleep(0.5)
    print ('...Relay channel %d off' % (Relay))
    GPIO.output(Relay_channel[Relay], GPIO.HIGH)
    time.sleep(0.5)
def request_token():
    liste=kullanici_giris()
    username=liste[0]
    password=liste[1]
    payload = "{ \n    \"username\": \""+username+"\",\n    \"password\": \""+password+"\"\n}"
    headers = {
        'Cmv-Application-Name': 'ReDesk',
        'Content-Type': 'application/json'
        }
    response = requests.request("POST", url_token, headers=headers, data = payload)
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
    print("response",response)
    response_utf =response.text.encode('utf8')
    print("response_utf",response_utf)
    
class BarCodeReader(reader.Reader):
    pass

class RFIDReader(reader.Reader):
    pass

def local_post(value,direction):
    payload=value
    response = requests.request("POST", url_local,  data = payload)
    response= str(response.text.encode('utf8'))
    response=response.split(',')
    response_lenght=len(response)
    print(response_lenght)
    
    response=local_response(response_lenght,response)
    print("response listesi",response)
    serial_no_control=serial_number_control(response,direction)

    #gate_trigger(serial_number_onay,direction)
    print("direction",direction)
    
    mesafe_cagir
def serial_number_control(response,direction):
    serial_number= getserial()#serial_number
    serial_number=str (serial_number)
    print("serial_number",serial_number)
    #mac_adress="000000001174fa70"
    if serial_number in response:
        serial_number_avaliability=0
    else :
        serial_number_avaliability=-1
    return serial_number_avaliability

def local_response(response_lenght,response):
    liste=[]
    for i in range(response_lenght):        
        if i==0:
            response_token0=response[0]
            response_token0=response_token0.split("'")
            response[0]=response_token0[1]
            
        if i== (response_lenght-1):
            response_token0=response[response_lenght-1]
            split=response_token0.split("'")
            response[response_lenght-1]=split[0]
        
        liste.append(response[i])
        print()
        #print("response_token {} :".format(i),response[i])
        
    print ("liste",liste)
    print("")
    return liste

def barcode_reader(rfbarcode_cagir):
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
        online_post(value,direction,rfbarcode_cagir)
    else:
        value="5b3f932d4da1e436283ab9375845b61f6c9fad28f15b067a8c8df8a886932794e9df66230436a03a9f6613052a21595eb012169c79008f5611777723d64f3d6abc5f916ef6cbc9d228aace425c1928b8c66d859c3d2906d6df1a2c3f83c30700c8cedae174741c7593f4b115dedbfbcb80d0d44a33ea2763d8d4a5d4b95a8e4f7849c8372550994a759832b673e52d3ac75bd63f3881760e208565eeb56c9ce527ea79c429719553dbcae9f4bbe9baed5f3fa0477dc917b53e595c16a8176b4d383d03877c57777b858f8e2f6c42cf8103fa7dd4b7aa3b041428ad5e9630e704f1187ff6666d02ad95feac90929574a52b7a28a5e12042a2dd75aa316c1f7d68"

        local_post(value,direction)
            
    reader.disconnect()

def online_post(value,direction,rfbarcode_cagir):
    response=13
    print("reuresponse",response)
    gate_trig=rf_control(response,rfbarcode_cagir)

def rf_control(response,rfbarcode_cagir):
    global rfbarcode_condition
    global mesafe_condition

    print("rf_control","rfbarcode_cagir ",rfbarcode_cagir,"response",response)
    
     
    if response == 13 :
        global rfbarcode_condition
        rfbarcode_condition="true"
        if rfbarcode_condition=="true" and mesafe_condition=="true":
            relay(1)
            rfbarcode_condition="false"
            mesafe_condition="false"
    else:
        rfbarcode_condition="false"
        

       
def temp_sonic(mesafe_cagir):
    global rfbarcode_condition
    global mesafe_condition

    
    distance=ultrasonic_distance_sensor()
    
    print("temp_sonic"," mesafe_cagir:",mesafe_cagir)
    print("distance",distance)
#     global mesafe_condition

        #temperature_distance="false"
    if distance > 0 and distance < 10:
        sensor = MLX90614()
        temperature=sensor.get_obj_temp()
            #print("sensor.get_amb_temp()",sensor.get_amb_temp())
        print("sensor.get_obj_temp()",temperature)
        time.sleep(1)
        print ("Mesafe:",distance - 0.5,"cm")
        print("")
        if temperature<30 :
            time.sleep(3)
            mesafe_condition="true"
            if  mesafe_condition=="true" and rfbarcode_condition=="true":
                relay(1)
      
                rfbarcode_condition="false"
                mesafe_condition="false"
        else:
            mesafe_condition="false"
   
    if distance>=10 and distance<30:
        print("Mesafe:",distance - 0.5,"cm","Elinizi yaklaştırın")
        print("")
            #temperature_distance="false"
        #return temperature_distance
      

    else:
        pass
        
if __name__ == "__main__":
    relay_setup()    
    #barcode_reader()
    while True:
        t2=threading.Thread(target=temp_sonic, args=("false",),daemon=True)
        print("t2 started")

        t1=threading.Thread(target=barcode_reader, args=("false",),daemon=True)
        print("t1 started")
        
        t1.start()
        
        t2.start()
        t1.join()
        t2.join()
        
