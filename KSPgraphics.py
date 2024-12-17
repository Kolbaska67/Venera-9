import matplotlib.pyplot as plt  # библиотека для рисования графиков
import json  # библиотека для работы с json

# получаем данные из json файла
graphics = dict()
with open("graphic.json") as f:
    graphics = json.load(f)
    
Speed = graphics["speed"]
SpeedX = graphics["speedX"]
SpeedY = graphics["speedY"]
Height = graphics["height"]
Time = graphics["time"]

# Строим графики
plt.subplot(2, 2, 1)
plt.plot(Time, Height)
plt.xlabel('Время, с')
plt.ylabel('Высота, м')
plt.grid(color='black') 

plt.subplot(2, 2, 2)
plt.plot(Time, Speed)
plt.xlabel('Время, с')
plt.ylabel('Скорость, км/с')
plt.grid(color='black') 

plt.subplot(2, 2, 3)
plt.plot(Time, SpeedX)
plt.xlabel('Время, с')
plt.ylabel('Скорость по оси X, км/с')
plt.grid(color='black') 

plt.subplot(2, 2, 4)
plt.plot(Time, SpeedY)
plt.xlabel('Время, с')
plt.ylabel('Скорость по оси Y, км/с')
plt.grid(color='black') 

plt.tight_layout(pad=1.5)
plt.savefig("result.png")
plt.show()
