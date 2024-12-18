import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

stages = [ 
    {'massa_stage': 50_000, 'massa_fuel': 110_000, 'burn_time': 100, 'f_tract': 2_700_000}, 
    {'massa_stage': 15_000, 'massa_fuel': 20_000, 'burn_time': 120, 'f_tract': 500_000}, 
    {'massa_stage': 25_000, 'massa_fuel': 600, 'burn_time': 50, 'f_tract': 50_000} 
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


massa_rocket = 210000  # кг масса ракеты
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
time1 = np.linspace(0, stages[0]["burn_time"]) # Время работы первой ступени 
result1 = odeint(system, start_value, time1, args=(0,)) # Решение системы для первой ступени 
 
# вторая ступень 
massa_rocket -= (stages[0]['massa_stage'] + stages[0]['massa_fuel']) # Масса ракеты после отсоединения первой ступени 
time2 = np.linspace(0, stages[1]["burn_time"], 100) # Время работы второй ступени 
result2 = odeint(system, result1[-1, :], time2, args=(1,)) # Решение системы для второй ступени


# третья ступень 
massa_rocket -= (stages[1]['massa_stage'] + stages[1]['massa_fuel']) # Масса ракеты после отсоединения второй ступени 
time3 = np.linspace(0, stages[2]["burn_time"], 100) # Время работы третьей ступени 
result3 = odeint(system, result2[-1, :], time3, args=(2,)) # Решение системы для третьей ступени 
  
 
# Объединение результатов 
time = np.concatenate([time1, time1[-1] + time2, time1[-1] + time2[-1] + time3]) 
Xx = np.concatenate([result1[:, 0], result2[:, 0], result3[:, 0]]) 
SpeedX = np.concatenate([result1[:, 1], result2[:, 1], result3[:, 1]]) 
Xy = np.concatenate([result1[:, 2], result2[:, 2], result3[:, 2]]) 
SpeedY = np.concatenate([result1[:, 3], result2[:, 3], result3[:, 3]])

plt.figure(figsize=(15, 15))  

plt.subplot(2, 2, 1)
plt.plot(time, Xx)
plt.xlabel('Время (с)')
plt.ylabel('Координата по X (м)')

plt.subplot(2, 2, 2)
plt.plot(time, Xy)
plt.xlabel('Время (с)')
plt.ylabel('Координата по Y')

plt.subplot(2, 2, 3)
plt.plot(time, SpeedX)
plt.xlabel('Время (с)')
plt.ylabel('Скорость по X')

plt.subplot(2, 2, 4)
plt.plot(time, SpeedY)
plt.xlabel('Время')
plt.ylabel('Скорость по Y')


plt.show()
