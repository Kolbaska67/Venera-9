import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from math import cos, sin, sqrt
import json


def abs_error(array1: list, array2: list) -> list:
    """abs_error
    Функция, которая высчитывает абсолютную погрешность 

    Args:
        array1 (list): Первая функция
        array2 (list): Вторая функция

    Returns:
        list: Абсолютную погрешность
    """
    result = []
    for i in range(array1):
        result.append(abs(array1[i] - array2[i]))
    return result


def mediana(array: list) -> float:
    """mediana
    Вычисляет значение медианы в двух функциях

    Args:
        array1 (list): Значение функции 1

    Returns:
        float: медианное значение
    """
    n = len(array)
    array.sort()
    if (n % 2 == 0):
        return array[n // 2]
    return (array[n // 2 + 1] + array[n // 2]) / 2
        

stages = [
    {"fuel_mass": 46779, 'burn_time': 254, 'Ssop': 1.9, 'Rsop': 60},
    {"fuel_mass": 12400, 'burn_time': 92, 'Ssop': 1.3, 'Rsop': 50},
]

e = 2.718281828459045
pi = 3.14
# H = sqrt(x ** 2 + y ** 2 + z ** 2 + 2 * REARTH * z + REARTH ** 2) - REARTH
ALPHA = 75 #кг/с
REARTH = 600000 #м
PHI = 0.00654 #радиан
MU = 0.028 #кг/моль
C = 0.5 #безразмерная
S = 13.5 #м2
Po0 = 1.225 #кг/м3
G = 6.674 * 1e-11 #н*м2/кг2
#g = 9.81 #м/с2
M = 5.2915793e22  #кг
Vgas = 2943 #м/с
R = 8.314 #дж/(моль*К)
T = 290 #кельвин
P0 = 1#атмосфера 1,013250·10 ** 5
Psoplo = 70#атмосфера

m0 = 700000 #кг


def m(t):
    return m0 - ALPHA * t


def gamma(t):
    return pi / 2 - PHI * t


def beta(t):
    return PHI * t


def v_vector(vx, vy, vz):
    return vx ** 2 + vy ** 2


def height(x, y, z):
    return sqrt(x ** 2 + y ** 2 + z ** 2 + 2 * REARTH * z + REARTH ** 2) - REARTH


def acceleration_of_free_fall(h):
    return (M * G) / ((REARTH + h) ** 2)


def system(y, t, number_stage):
    """system
    Вычисление необходимой функции для решения ОДУ

    Args:
        y (list): список переменных:
            x1 - координата по X
            x2 - координата по Y
            x3 - координата по Z
            x4 - скорость по X
            x5 - скорость по Y
            x6 - скорость по Z
            x7 - ускорение по X
            x8 - ускорение по Y
            x9 - ускорение по Z
        t (list): последовательность точек, для которых требуется найти значение y. 
        number_stage (int): номер ступени

    Returns:
        list: массив, содержащий значение y для каждого желаемого времени в t, с начальным значением y0 в первой строке.
    """
   
    x1, x4, x2, x5, x3, x6 = y

    stage = stages[number_stage]

    Ssop = stage['Ssop']
    Rsop = stage['Rsop']

    gamma0 = gamma(t)
    beta0 = beta(t)

    v = v_vector(x4, x5, x6)
    h = height(x1, x2, x3)
    g = acceleration_of_free_fall(h)

    ftag = ALPHA * Vgas + Ssop * (Psoplo - P0 * e ** ((-MU * g * h) / (R * T)))
    ftazh = (m0 - ALPHA * t) * g
    fsop = 0.5 * v ** 2 * C * S * Po0 * e ** ((-MU * g * h) / (R * T))

    summa_sqrt = x4 ** 2 + x5 ** 2 + x6 ** 2

    x7 = (1 / m(t)) * np.cos(gamma0) * np.cos(beta0) * (ftag - fsop)
    x8 = np.sin(gamma0) * np.sin(beta0) * (ftag - fsop) * (1 / m(t))
    x9 = (-ftazh + (np.sin(gamma0)) * (-fsop + ftag) * (1 / m(t))) * (-1)


    return [x4, x7, x5, x8, x6, x9]


initial_conditions = [1, 1, 1, 1, 1, 1]

time1 = np.linspace(0, stages[0]["burn_time"])

result1= odeint(system, initial_conditions, time1, args=(0,))

graphics = dict()
with open("graphic.json") as f:
    graphics = json.load(f)
    
Time = graphics["time"]
m = min(len(Time), len(time1))
Time = Time[:m]
time1 = time1[:m]

SpeedX = graphics["speedX"][:m]
Height = graphics["height"][:m]
DragX = graphics["dragX"][:m]
DragY = graphics["dragY"][:m]
DragZ = graphics["dragZ"][:m]

x1 = [result1[:, 0]][:m]
x4 = [result1[:, 1]][:m]
x2 = [result1[:, 2]][:m]
x5 = [result1[:, 3]][:m]
x3 = [result1[:, 4]][:m]
x6 = [result1[:, 5]][:m]

Abs_error_height = abs_error(Height, x3)
Abs_error_speedX = abs_error(SpeedX, x4)
Abs_error_dragX = abs_error(DragX, x1)
Abs_error_dragY = abs_error(DragY, x2)
Abs_error_dragZ = abs_error(DragZ, x3)


print(f"Медина погрешности высоты: {mediana(Abs_error_height)}")
print(f"Медина погрешности скорости по X: {mediana(Abs_error_speedX)}")
print(f"Медина погрешности смещения по X: {mediana(Abs_error_dragX)}")
print(f"Медина погрешности смещения по Y: {mediana(Abs_error_dragY)}")
print(f"Медина погрешности смещения по Z: {mediana(Abs_error_dragZ)}")

plt.figure(figsize=(15, 15))    

plt.subplot(3, 2, 1)
plt.plot(time1, x3, color="red", label="Высота от времени KSP")
plt.plot(Time, Height, color="blue", label="Высота от времени МатМодель")
plt.plot(Time, Abs_error_height, color="orange", label="Абсолютная погрешность")
plt.xlabel('Время, с')
plt.ylabel('Высота, м')
plt.grid(color='black') 
plt.legend()

plt.subplot(3, 2, 2)
plt.plot(time1, x4, color="red", label="Скорость по X KSP")
plt.plot(Time, SpeedX, color="blue", label="Скорость по X МатМодель")
plt.plot(Time, Abs_error_speedX, color="orange", label="Абсолютная погрешность")
plt.xlabel('Время, с')
plt.ylabel('Скорость по оси X, км/с')
plt.grid(color='black') 
plt.legend()

plt.subplot(3, 2, 6)
plt.plot(time1, x1, color="red", label="Смещение по X KSP")
plt.plot(Time, DragX, color="blue", label="Смещение по X МатМодель")
plt.plot(Time, Abs_error_dragX, color="orange", label="Абсолютная погрешность")
plt.xlabel('Время, с')
plt.ylabel('Смещение по оси X, м')
plt.grid(color='black') 
plt.legend()

plt.subplot(3, 2, 7)
plt.plot(time1, x2, color="red", label="Смещение по Y KSP")
plt.plot(Time, DragY, color="blue", label="Смещение по Y МатМодель")
plt.plot(Time, Abs_error_dragY, color="orange", label="Абсолютная погрешность")
plt.xlabel('Время, с')
plt.ylabel('Смещение по оси Y, м')
plt.grid(color='black') 
plt.legend()

plt.subplot(3, 2, 8)
plt.plot(time1, x3, color="red", label="Смещение по Z KSP")
plt.plot(Time, DragZ, color="blue", label="Смещение по Z МатМодель")
plt.plot(Time, Abs_error_dragZ, color="orange", label="Абсолютная погрешность")
plt.xlabel('Время, с')
plt.ylabel('Смещение по оси Z, м')
plt.grid(color='black') 
plt.legend()

plt.tight_layout(pad=1.5)
plt.savefig("compare_graphics.png")
plt.show()
