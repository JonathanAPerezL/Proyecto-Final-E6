#Brujula
import time
from math import atan2, degrees
import math
import board
import adafruit_lsm303dlh_mag
import adafruit_lsm303_accel
#MOTOT AZIMUTH
import RPi.GPIO as GPIO
import time
#interptretacion de datos
import json,urllib.request, time
from urllib import response
import datetime
from pytz import timezone

#Brujula
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
anglea=90

#MOTOR
in1 = 23
in2 = 24
in3 = 10
in4 = 9

#Pines Elevacion
in11 = 17
in22 = 18
in33= 27
in44 = 22

step_sleep = 0.002
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# setting up
GPIO.setmode( GPIO.BCM )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )
GPIO.setup( in11, GPIO.OUT )
GPIO.setup( in22, GPIO.OUT )
GPIO.setup( in33, GPIO.OUT )
GPIO.setup( in44, GPIO.OUT )


 
# initializing
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )
GPIO.output( in11, GPIO.LOW )
GPIO.output( in22, GPIO.LOW )
GPIO.output( in33, GPIO.LOW )
GPIO.output( in44, GPIO.LOW )
motor_pins = [in1,in2,in3,in4]
motor_step_counter = 0 ;



def dezpup(azi, ele, d1):
    motor_pins = [in1,in2,in3,in4]
    motor_step_counter = 0 ;

    motor_pins1 = [in11,in22,in33,in44]
    motor_step_counter1 = 0
    step_count = int(azi*2*65*1/5.625)
    direction = d1
    step_count1 = int(ele*2.4*64*1/5.625)
    direction1 = True
    
    i = 0
    for i in range(step_count):
        for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        if direction==True:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction==False:
            motor_step_counter = (motor_step_counter + 1) % 8
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
        time.sleep( step_sleep )

    j = 0
    for j in range(step_count1):
        for pin in range(0, len(motor_pins1)):
            GPIO.output( motor_pins1[pin], step_sequence[motor_step_counter1][pin] )
        if direction1==True:
            motor_step_counter1 = (motor_step_counter1 - 1) % 8
        elif direction1==False:
            motor_step_counter1 = (motor_step_counter1 + 1) % 8
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
        time.sleep( step_sleep )
    motor_step_counter1 = 0 ;
    motor_step_counter = 0 ;
    low();

def dezpdo(azi, ele, d2):
    motor_pins = [in1,in2,in3,in4]
    motor_step_counter = 0 ;

    motor_pins1 = [in11,in22,in33,in44]
    motor_step_counter1 = 0
    
    step_count = int(azi*2*65*1/5.625)
    direction = d2
    step_count = int(-1*ele*2.4*64*1/5.625)
    direction1 = False
    
    i = 0
    for i in range(step_count):
        for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        if direction==True:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction==False:
            motor_step_counter = (motor_step_counter + 1) % 8
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
        time.sleep( step_sleep )

    j = 0
    for j in range(step_count1):
        for pin in range(0, len(motor_pins1)):
            GPIO.output( motor_pins1[pin], step_sequence[motor_step_counter1][pin] )
        if direction1==True:
            motor_step_counter1 = (motor_step_counter1 - 1) % 8
        elif direction1==False:
            motor_step_counter1 = (motor_step_counter1 + 1) % 8
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
        time.sleep( step_sleep )
    motor_step_counter1 = 0 ;
    motor_step_counter = 0 ;
    low();


def low():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.output( in11, GPIO.LOW )
    GPIO.output( in22, GPIO.LOW )
    GPIO.output( in33, GPIO.LOW )
    GPIO.output( in44, GPIO.LOW )

def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.output( in11, GPIO.LOW )
    GPIO.output( in22, GPIO.LOW )
    GPIO.output( in33, GPIO.LOW )
    GPIO.output( in44, GPIO.LOW )
    GPIO.cleanup()

#Buscamos el Norte o el 0 segun nuestra brujula
azimut_1=90
while True:
    if (azimut_1 !=0):
        print("Buscando el Norte")
        def vector_2_degrees(y, x):
            angle = degrees(atan2(y, x))
            #print(angle)
            if angle < 0:
                angle += 360
            return angle

        def get_heading(_sensor):
            magnet_x, magnet_y, magnet_z = _sensor.magnetic
            return vector_2_degrees(magnet_y, magnet_x)   

        azimut_1 = get_heading(sensor)
        if (azimut_1<180):
            azimutd=-1*azimut_1
        elif(azimut_1>180):
            azimutd=360-azimut_1
        if (azimutd>0):
            step_count = int(azimutd*2*65*1/5.625)
            direction = False
        elif (azimutd<0):
            step_count = int(-1*azimutd*2*65*1/5.625)
            direction = True
        

        print("Angulo de de Azimut del sensor:{:.2f}".format(azimut_1))
        
        i = 0
        for i in range(step_count):
            for pin in range(0, len(motor_pins)):
                GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
            if direction==True:
                motor_step_counter = (motor_step_counter - 1) % 8
            elif direction==False:
                motor_step_counter = (motor_step_counter + 1) % 8
            else: # defensive programming
                print( "uh oh... direction should *always* be either True or False" )
                cleanup()
                exit( 1 )
            time.sleep( step_sleep )


        motor_step_counter = 0 
        low()
        #print("el angulo es: ", azimut_1)
        time.sleep(1)

    elif(azimut_1 == 0):
        break
    
print("INICIO")

ini = True
while ini == True:
    try:
        #Buscamos proximos pases
        url = "https://api.n2yo.com/rest/v1/satellite/radiopasses/25544/14.67055/-90.58384/0/2/10/&apiKey=Y48HRM-E5Y2VD-R7E5F8-4W48"

        response = urllib.request.urlopen(url)
        result = json.loads(response.read())
        #leemos las coordenadas de inicio
        startaz = result["passes"][0]["startAz"]
        maxaz = result["passes"][0]["maxAz"]
        endaz = result["passes"][0]["endAz"]
        #buscamos el tiempo de inicio, elv max y fin, junto con la hora UTC actual
        max_el = result["passes"][0]["maxEl"]
        start_time = result["passes"][0]["startUTC"]
        max_time = result["passes"][0]["maxUTC"]
        end_time = result["passes"][0]["endUTC"]
        actual_time = datetime.datetime.now()
        unix_time = datetime.datetime.timestamp(actual_time)
        time_wait = 5
        time_wait_actual= int(int(start_time-int(unix_time))/60)
        print("Tiempo de espera actual en min: ",time_wait_actual)
        if(time_wait_actual<= time_wait):
            print("INICIANDO POSICIONAMIENTO")
            if (startaz>180):
                angle1=360-startaz
                print(angle1)
                step_count = int(angle1*2*65*1/5.625)
                direction = True
            elif (startaz<=180):
                angle1=startaz
                step_count = int(-1*angle1*2*65*1/5.625)
                direction = False
                
            i = 0
            for i in range(step_count):
                for pin in range(0, len(motor_pins)):
                    GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
                if direction==True:
                    motor_step_counter = (motor_step_counter - 1) % 8
                elif direction==False:
                    motor_step_counter = (motor_step_counter + 1) % 8
                else: # defensive programming
                    print( "uh oh... direction should *always* be either True or False" )
                    cleanup()
                    exit( 1 )
                time.sleep( step_sleep )
            
            azimut_1 = 0
            magnet_x, magnet_y, magnet_z = sensor.magnetic
            a = degrees(atan2(magnet_y, magnet_x))
            if a < 0:
                azimut_1 = a+360

            while True:
                try:
                    if (azimut_1 >= startaz+2 or azimut_1 <= startaz-2):

                        def vector_2_degrees(y, x):
                            angle = degrees(atan2(y, x))
                            #print(angle)
                            if angle < 0:
                                angle += 360
                            return angle

                        def get_heading(_sensor):
                            magnet_x, magnet_y, magnet_z = _sensor.magnetic
                            return vector_2_degrees(magnet_y, magnet_x)   

                        azimut_1 = get_heading(sensor)
                        print(azimut_1)
                        print(startaz)
                        if (azimut_1<startaz):
                            azimutd=-1*(azimut_1 -startaz)
                        elif(azimut_1>startaz):
                            azimutd=startaz-azimut_1
                        if (azimutd>0):
                            step_count = int(azimutd*2*64*1/5.625)
                            direction = False
                        elif (azimutd<0):
                            step_count = int(-1*azimutd*2*64*1/5.625)
                            direction = True
                        

                        print("Angulo de de Azimut del sensor:{:.2f}".format(azimut_1))
                        
                        i = 0
                        for i in range(step_count):
                            for pin in range(0, len(motor_pins)):
                                GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
                            if direction==True:
                                motor_step_counter = (motor_step_counter - 1) % 8
                            elif direction==False:
                                motor_step_counter = (motor_step_counter + 1) % 8
                            else: # defensive programming
                                print( "uh oh... direction should *always* be either True or False" )
                                cleanup()
                                exit( 1 )
                            time.sleep( step_sleep )


                        motor_step_counter = 0 
                        low()
                        #print("el angulo es: ", azimut_1)

                    elif(azimut_1 <= startaz+2 and azimut_1 >= startaz-2):
                        break
                except Exception as e:
                    print(e)
                    exit(0)
             
            ang1=0
            ang2=0
            dire=True
            if (startaz>maxaz):
                ang1= int(startaz-maxaz)
                dire = True
                print(ang1)
            elif (startaz<maxaz):
                ang1= int(maxaz-startaz)
                dire = False
                print(ang1)
            elif (startaz>maxaz and maxaz<90):
                ang1= 360-startaz+maxaz
                dire = False
                print(ang1)

#             if (maxaz>endaz and maxaz>90):
#                 ang2= int(maxaz-endaz)
#                 print(ang2)
            print(maxaz)
            print(endaz)
            if (maxaz<endaz):
                ang2= int(endaz-maxaz)
                print(ang1)
            elif (maxaz>endaz and maxaz>90):
                ang2= 360-maxaz+endaz
                print(ang2)
                
            t1 = int(max_time-start_time)
            t2 = int(end_time-max_time)

            m1 = max_el/ang1
            m11 = ang1/t1
            m2 = -max_el/ang2
            m22 = ang2/t2
            cont1=0
            cont2=0
            tu=10
            td=10
            az1=0
            az11=0
            aza=0
            el1=0
            el11=0
            ela=0
            az2=0
            az22=0
            aza2=0
            el2=0
            el22=0
            ela2=0
            while True:
                try:
                    print("Posicion aceptada, Esperando...")
                    actual_time = datetime.datetime.now()
                    unix_time = datetime.datetime.timestamp(actual_time)
                    prue1=1
                    if (prue1==1):
                        print("Iniciando Seguimiento")
                        while True:
                            try:
                                if(cont1 <= t1):
                                    print("up",cont1)
                                    print("up",t1)
                                    time.sleep(20)
                                    az1 = tu*m11
                                    az11 = az1-aza
                                    aza = az1
                                    el1 = az1*m1
                                    el11= el1-ela
                                    ela=el1
                                    tu = tu + 20
                                    cont1 +=20
                                    dezpup(az11, el11, dire)

                                elif(cont1 >= t1 and cont2 <= t2):
                                    print("down",cont2)
                                    print("down",t2)
                                    time.sleep(20)
                                    az2 = td*m22
                                    az22 = az2-aza2
                                    aza2 = az2
                                    el2 = az2*m2
                                    el22= el2-ela2
                                    ela2=el2
                                    td = td + 20
                                    cont2 +=20
                                    #print("el down", el22)
                                    dezpup(az22, el22, dire)
                                else:
                                    ini == False
                                    break
                            except Exception as e:
                                print(e)
                                exit(0)
                            
                        time.sleep(30)
                except Exception as e:
                    print(e)
                    exit(0)
                   
        else:
            time.sleep(30)

    except Exception as e:
        print(e)
        exit(0)

