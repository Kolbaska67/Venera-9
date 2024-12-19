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
    for i in range(len(array1)):
        result.append(abs(array1[i] - array2[i]))
    return result


def mediana(array: list) -> float:
    """mediana

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


def otn_error(abs_error, array):
    result = []
    for i in range(len(array)):
        result.append(abs_error[i] / array[i])
    return result
        

stages = [ 
    {'massa_stage': 50_000, 'massa_fuel': 110_000, 'burn_time': 90, 'f_tract': 2_700_000}, 
    {'massa_stage': 15_000, 'massa_fuel': 20_000, 'burn_time': 60, 'f_tract': 500_000}, 
    {'massa_stage': 10_000, 'massa_fuel': 600, 'burn_time': 60, 'f_tract': 6_000} 
] 

e = 2.718281828459045
pi = 3.14

R_KERBIN = 600000  # м радиус Кербина
MU = 0.028  # кг/моль молярная масса воздуха 
C = 0.5  # безразмерная коэффициент лобового сопротивления
S = 13.5  # м2 площадь поперечного сечения
Po0 = 1.225  # кг/м3 плотность воздуха
G = 6.674e-11  # н*м2/кг2 гравитационная постоянная
M_KERBIN = 5.2915793e22  #кг масса Кербина
R = 8.314  # дж/(моль*К) универсальная газовая постояннная
START_T = 300  # К начальная температура
P0 = 101_325  # Па давление 
Psoplo = 70  # атмосфера давление сопла
g = 9.81  # м/c2 ускорение свободного падения


def corner(height: float) -> float:
    """ Угол, в зависимости от высоты

    Args:
        height (float): высота

    Returns:
        float: угол в градусах
    """
    if height < 80000: 
        return 90 * (1 - height / 80000) 
    return 0 


def kf(massa_fuel: float, time: float) -> float: 
    """ коэффициент , сколько сгорело топлива
    Args:
        m (float): масса топлива
        t (float): время

    Returns:
        float: коэффициент , сколько сгорело топлива
    """
    return massa_fuel / time 


massa_rocket = 210_000  # кг масса ракеты
T = 300  # температура ракеты 


def system(y: list, t: list, num_stage: int) -> list:
    """Вычисление необходимой функции для решения ОДУ

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
        num_stage (int): номер ступени

    Returns:
        list: массив, содержащий значение y для каждого желаемого времени в t, с начальным значением y0 в первой строке.
    """

    Xx, speedX, Xy, speedY = y

    global T

    stage = stages[num_stage]
    
    alpha = np.radians(corner(Xy)) # угол поворота ракеты

    massa_fuel = stage["massa_fuel"]
    F_traction = stage['f_tract']
    burn_time = stage['burn_time']
    
    k = kf(massa_fuel, burn_time)
    
    if T > 50:
        T = START_T - 6 * (Xy // 1000)
        
    cur_massa = massa_rocket - k * t # текущая масса = масса ракеты на данном стадии - использованное топливо
    v = speedX ** 2 + speedY ** 2
    
    p = P0 * e ** ((-g * Xy * MU) / (R * T)) # давление от высоты
    po = (p * MU) / (R * T) # плотность ракеты от высоты
    
    F_grav = (G * M_KERBIN * cur_massa) / ((R_KERBIN + Xy) ** 2) # сила гравитации
    F_resist = C * S * v * po / 2 # сила сопротивления
    
    dSpeedX = (F_traction - F_resist) * np.cos(alpha) / cur_massa
    dSpeedY = ((F_traction - F_resist) * np.sin(alpha) - F_grav) / cur_massa 
    
    return [speedX, dSpeedX, speedY, dSpeedY]


start_value = [0, 0, 0, 0] # начальные значения

# первая ступень 
time1 = np.linspace(0, stages[0]["burn_time"],20_000) # Время работы первой ступени 
result1 = odeint(system, start_value, time1, args=(0,)) # Решение системы для первой ступени 
 
# вторая ступень 
massa_rocket -= (stages[0]['massa_stage'] + stages[0]['massa_fuel']) # Масса ракеты после отсоединения первой ступени 
time2 = np.linspace(0, stages[1]["burn_time"], 19_000) # Время работы второй ступени 
result2 = odeint(system, result1[-1, :], time2, args=(1,)) # Решение системы для второй ступени


# третья ступень 
massa_rocket -= (stages[1]['massa_stage'] + stages[1]['massa_fuel']) # Масса ракеты после отсоединения второй ступени 
time3 = np.linspace(0, stages[2]["burn_time"], 1300) # Время работы третьей ступени 
result3 = odeint(system, result2[-1, :], time3, args=(2,)) # Решение системы для третьей ступени 
  
time = np.concatenate([time1, time1[-1] + time2, time1[-1] + time2[-1] + time3]) 

graphics = dict()
with open("KSP_graphics/graphic.json") as f:
    graphics = json.load(f)
    
timeKSP = graphics["time"]
m = min(len(timeKSP), len(time))
timeKSP = timeKSP[:m]
time = time

x_coords_KSP = graphics["x_coords"][:m]
y_coords_KSP = graphics["y_coords"][:m]
speedX_KSP = graphics["speedX"][:m]
speedY_KSP = graphics["speedY"][:m]

# Объединение результатов 
Xx = np.concatenate([result1[:, 0], result2[:, 0], result3[:, 0]])
SpeedX = np.concatenate([result1[:, 1], result2[:, 1], result3[:, 1]]) 
Xy = np.concatenate([result1[:, 2], result2[:, 2], result3[:, 2]])
SpeedY = np.concatenate([result1[:, 3], result2[:, 3], result3[:, 3]])

Abs_error_y_coords = abs_error(y_coords_KSP, Xy)
Abs_error_x_coords = abs_error(x_coords_KSP, Xx)
Abs_error_speedX = abs_error(speedX_KSP, SpeedX)
Abs_error_speedY = abs_error(speedY_KSP, SpeedY)

print(f"Медина погрешности координаты по Y: {mediana(Abs_error_y_coords)}")
print(f"Медина погрешности координаты по X: {mediana(Abs_error_x_coords)}")
print(f"Медина погрешности скорости по X: {mediana(Abs_error_speedX)}")
print(f"Медина погрешности скорости по Y: {mediana(Abs_error_speedY)}")

plt.figure(figsize=(15, 15))    

plt.subplot(2, 2, 1)
plt.plot(timeKSP, x_coords_KSP, color="red", label="Координата по X KSP")
plt.plot(time, Xx, color="blue", label="Координата по X МатМодель")
plt.plot(time, Abs_error_x_coords, color="orange", label="Абсолютная погрешность")
plt.xlabel('Время, с')
plt.ylabel('Координата по X, м')
plt.grid(color='black') 
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(timeKSP, y_coords_KSP, color="red", label="Координата по Y KSP")
plt.plot(time, Xy, color="blue", label="Координата по Y МатМодель")
plt.plot(time, Abs_error_y_coords, color="orange", label="Абсолютная погрешность")
plt.xlabel('Время, с')
plt.ylabel('Координата по Y, м')
plt.grid(color='black') 
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(timeKSP, speedX_KSP, color="red", label="Скорость по X KSP")
plt.plot(time, SpeedX, color="blue", label="Скорось по X МатМодель")
plt.plot(time, Abs_error_speedX, color="orange", label="Абсолютная погрешность")
plt.xlabel('Время, с')
plt.ylabel('Скорость по оси X, м/c')
plt.grid(color='black') 
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(timeKSP, speedY_KSP, color="red", label="Скорость по Y KSP")
plt.plot(time, SpeedY, color="blue", label="Скорость по Y МатМодель")
plt.plot(time, Abs_error_speedY, color="orange", label="Абсолютная погрешность")
plt.xlabel('Время, с')
plt.ylabel('Скорость по оси Y, м/c')
plt.grid(color='black') 
plt.legend()

plt.tight_layout(pad=1.5)
plt.savefig("Compare_graphics/compare_graphics.png")
plt.show()