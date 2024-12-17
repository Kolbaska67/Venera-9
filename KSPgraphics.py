import matplotlib.pyplot as plt  # библиотека для рисования графиков
import json  # библиотека для работы с json

# получаем данные из json файла
graphics = dict()
with open("graphic.json") as f:
    graphics = json.load(f)
    
SpeedX = graphics["speedX"]
SpeedY = graphics["speedY"]
SpeedZ = graphics["speedZ"]
Height = graphics["height"]
Time = graphics["time"]
DragX = graphics["dragX"]
DragY = graphics["dragY"]
DragZ = graphics["dragZ"]

# Строим графики
plt.subplot(4, 2, 1)
plt.plot(Time, Height)
plt.xlabel('Время, с')
plt.ylabel('Высота, м')
plt.grid(color='black') 

plt.subplot(4, 2, 2)
plt.plot(Time, SpeedX)
plt.xlabel('Время, с')
plt.ylabel('Скорость по оси X, км/с')
plt.grid(color='black') 

plt.subplot(4, 2, 3)
plt.plot(Time, SpeedY)
plt.xlabel('Время, с')
plt.ylabel('Скорость по оси Y, км/с')
plt.grid(color='black') 

plt.subplot(4, 2, 4)
plt.plot(Time, SpeedZ)
plt.xlabel('Время, с')
plt.ylabel('Скорость по оси Z, км/с')
plt.grid(color='black') 

plt.subplot(4, 2, 5)
plt.plot(Time, DragX)
plt.xlabel('Время, с')
plt.ylabel('Смещение по оси X, м')
plt.grid(color='black') 

plt.subplot(4, 2, 6)
plt.plot(Time, DragY)
plt.xlabel('Время, с')
plt.ylabel('Смещение по оси Y, м')
plt.grid(color='black') 

plt.subplot(4, 2, 7)
plt.plot(Time, DragZ)
plt.xlabel('Время, с')
plt.ylabel('Смещение по оси Z, м')
plt.grid(color='black') 


plt.tight_layout(pad=1.5)
plt.show()
