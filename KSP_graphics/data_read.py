import numpy as np
import krpc  # библиотека для подключения к KSP и сбора данных
import json  # библиотека для работы с json форматом

# подключение к серверу KSP
connection = krpc.connect(name='VARKT')
vessel = connection.space_center.active_vessel

# списки с результатами
y_coords = []
x_coords = []
Time = []
SpeedX = []
SpeedY = []

# Получаем ориентацию корабля
Orbit = vessel.orbit.body.reference_frame

reference_frame = vessel.orbit.body.reference_frame

Position = vessel.position(reference_frame)

# Начальная позиция для расчета смещения
initial_position = vessel.position(vessel.orbit.body.reference_frame)
# Длина вектора
initial_position_vec_length = np.linalg.norm(initial_position)

# Получаем данные
while True:
    Time.append(vessel.met) # время в c
    y_coords.append(vessel.flight(Orbit).mean_altitude) # высота в м
    
    # Текущее положение для расчета смещения
    current_position = vessel.position(vessel.orbit.body.reference_frame)
    
    # Расчет смещения
    current_position = current_position / np.linalg.norm(current_position) * initial_position_vec_length
    horizontal_displacement = np.linalg.norm(current_position - initial_position)
    
    x_coords.append(horizontal_displacement)
    
    # скорости в проекциях 
    vertical_speed = vessel.flight(vessel.orbit.body.reference_frame).vertical_speed  # скорость по X в м/c
    horizontal_speed = vessel.flight(vessel.orbit.body.reference_frame).horizontal_speed  # скорость по Y в м/c
    SpeedX.append(horizontal_speed)
    SpeedY.append(vertical_speed)
    
    if vessel.met > 250: 
        print("Истекло 250 секунд")   
        break
    
print("Данные считаны")

data = {"y_coords": y_coords, "x_coords": x_coords, "time": Time, "speedX": SpeedX, "speedY": SpeedY}

with open("graphic.json", "w") as f:
    json.dump(fp=f,obj=data)