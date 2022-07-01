import ISS_Info
import turtle
import time

screen = turtle.Screen()
screen.setup(720,360)
screen.setworldcoordinates(-180,-90,180,90)
screen.bgpic("guate.png")
screen.register_shape("am.gif")
screen.register_shape("descarga.gif")
screen.register_shape("tr.gif")

#iss0 = turtle.Turtle()
iss = turtle.Turtle()
#iss0.shape("am.gif")
iss.shape("descarga.gif")
#iss0.penup()
iss.penup()


lat2 = 0
lon2 = 0


while True:
    location = ISS_Info.iss_current_loc()
    lat = location['iss_position']['latitude']
    lon = location['iss_position']['longitude']

    print("Datos de Posicion: \n Latitud: {}, Longitud: {}".format(lat,lon))
    
    #iss0.goto(float(lon),float(lat))
    iss.goto(float(lon),float(lat))
    iss.dot(3, "yellow")

    time.sleep(1)
    lat2=lat
    lon2=lon
    