import krpc  # библиотека для подключения к KSP и сбора данных
import json  # библиотека для работы с json форматом

# подключение к серверу KSP
connection = krpc.connect(name='VARKT')
vessel = connection.space_center.active_vessel

# списки с результатами
Height = []
Speed = []
Time = []
SpeedX = []
SpeedY = []

# Получаем ориентацию корабля
Orbit = vessel.orbit.body.reference_frame

# Получаем данные
while True:
    Speed.append(vessel.flight(Orbit).speed / 1000) # скорость в км/c
    Time.append(vessel.met) # время в c
    Height.append(vessel.flight(Orbit).mean_altitude) # высота в м
    # скорости в проекциях 
    vertical_speed = vessel.flight(vessel.orbit.body.reference_frame).vertical_speed / 1000 # скорость по X в км/c
    horizontal_speed = vessel.flight(vessel.orbit.body.reference_frame).horizontal_speed / 1000 # скорость по Y в км/c

    SpeedX.append(horizontal_speed)
    SpeedY.append(vertical_speed)

    if vessel.met > 250: 
        print("Истекло 250 секунд")   
        break

print("Данные считаны")

data = {"speed": Speed, "height": Height, "time": Time, "speedX": SpeedX, "speedY": SpeedY}

with open("graphic.json", "w") as f:
    json.dump(fp=f,obj=data)
