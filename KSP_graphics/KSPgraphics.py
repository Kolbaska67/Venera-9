import matplotlib.pyplot as plt  # библиотека для рисования графиков
import json  # библиотека для работы с json

# получаем данные из json файла
graphics = dict()
with open("graphic.json") as f:
    graphics = json.load(f)
    
SpeedX = graphics["speedX"]
SpeedY = graphics["speedY"]
x_coords = graphics["x_coords"]
y_coords = graphics["y_coords"]
Time = graphics["time"]

# Строим график

plt.figure(figsize=(15, 15))   

plt.subplot(2, 2, 1)
plt.plot(Time, x_coords)
plt.xlabel('Время, с')
plt.ylabel('Координата по X, м')
plt.grid(color='black') 

plt.subplot(2, 2, 2)
plt.plot(Time, y_coords)
plt.xlabel('Время, с')
plt.ylabel('Координата по Y, м')
plt.grid(color='black') 

plt.subplot(2, 2, 3)
plt.plot(Time, SpeedX)
plt.xlabel('Время, с')
plt.ylabel('Скорость по оси X, м/с')
plt.grid(color='black') 

plt.subplot(2, 2, 4)
plt.plot(Time, SpeedY)
plt.xlabel('Время, с')
plt.ylabel('Скорость по оси Y, м/с')
plt.grid(color='black') 

plt.show()
