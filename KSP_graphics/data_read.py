import krpc  # библиотека для подключения к KSP и сбора данных
import json  # библиотека для работы с json форматом

# подключение к серверу KSP
connection = krpc.connect(name='VARKT')
vessel = connection.space_center.active_vessel

# списки с результатами
DragX = []
DragY = []
DragZ = []
Height = []
Time = []
SpeedX = []
SpeedY = []
SpeedZ = []

# Получаем ориентацию корабля
Orbit = vessel.orbit.body.reference_frame

reference_frame = vessel.orbit.body.reference_frame

Position = vessel.position(reference_frame)
velocity = vessel.velocity(reference_frame)

# Получение начального положения корабля для вычисления перемещения
initialPositionX = Position[0]
initialPositionY = Position[1]
initialPositionZ = Position[2]

# Получаем данные
while True:
    Time.append(vessel.met) # время в c
    Height.append(vessel.flight(Orbit).mean_altitude) # высота в м
    
    velocity = vessel.velocity(reference_frame)

    # скорости в проекциях 
    vertical_speed = vessel.flight(vessel.orbit.body.reference_frame).vertical_speed / 1000 # скорость по X в км/c
    horizontal_speed = vessel.flight(vessel.orbit.body.reference_frame).horizontal_speed / 1000 # скорость по Y в км/c
    SpeedX.append(horizontal_speed)
    SpeedY.append(vertical_speed)
    SpeedZ.append(velocity[2])
    
    # положение в пространстве

    reference_frame = vessel.orbit.body.reference_frame

    Position = vessel.position(reference_frame)

    currentPositionX = Position[0]
    currentPositionY = Position[1]
    currentPositionZ = Position[2]
    
    # смешение по проециям
    DragX.append(currentPositionX - initialPositionX)
    DragY.append(currentPositionY - initialPositionY)
    DragZ.append(currentPositionZ - initialPositionZ)

    if vessel.met > 250: 
        print("Истекло 250 секунд")   
        break
    
    if (vessel.flight(Orbit).mean_altitude >= 70_000):
        print("Мы вышли на орбиту")
        break

print("Данные считаны")

data = {"height": Height, "time": Time, "speedX": SpeedX, "speedY": SpeedY, 
        "speedZ": SpeedZ, "dragX": DragX, "dragY": DragY, "dragZ": DragZ}

with open("graphic.json", "w") as f:
    json.dump(fp=f,obj=data)