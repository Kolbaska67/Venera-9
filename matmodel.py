import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from math import cos, sin, sqrt

stages = [
    {"fuel_mass": 46779, 'burn_time': 254, 'Ssop': 1.9, 'Rsop': 60},
    {"fuel_mass": 12400, 'burn_time': 92, 'Ssop': 1.3, 'Rsop': 50},
]

e = 2.718281828459045
pi = 3.14
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


def system(y: list, t: list, number_stage: int) -> list:
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

x1 = [result1[:, 0]]
x4 = [result1[:, 1]]
x2 = [result1[:, 2]]
x3 = [result1[:, 4]]

plt.subplot(4, 2, 1)
plt.plot(time1, x3)
plt.xlabel('Время, с')
plt.ylabel('Высота, м')
plt.grid(color='black') 

plt.subplot(4, 2, 3)
plt.plot(time1, x4)
plt.xlabel('Время, с')
plt.ylabel('Скорость по оси X, км/с')
plt.grid(color='black') 

plt.subplot(4, 2, 6)
plt.plot(time1, x1)
plt.xlabel('Время, с')
plt.ylabel('Смещение по оси X, м')
plt.grid(color='black') 

plt.subplot(4, 2, 7)
plt.plot(time1, x2)
plt.xlabel('Время, с')
plt.ylabel('Смещение по оси Y, м')
plt.grid(color='black') 

plt.subplot(4, 2, 8)
plt.plot(time1, x3)
plt.xlabel('Время, с')
plt.ylabel('Смещение по оси Z, м')
plt.grid(color='black') 


plt.tight_layout(pad=1.5)
plt.savefig("result.png")
plt.show()
