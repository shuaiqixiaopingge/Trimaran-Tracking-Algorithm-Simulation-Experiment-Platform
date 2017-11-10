import time
from math import cos, sin, pi

import numpy as np
from numpy.random import normal

from PID import PID
from decisionMaker import Maker
# from drawer import Drawer
import matplotlib as mlp
import matplotlib.pyplot as plt


def simulate(state, left, right, dt):
    x = state['x']
    y = state['y']
    u0 = state['u']
    v0 = state['v']
    phi = state['phi']
    r0 = state['alpha']

    left = left / 60
    right = right / 60

    u = v0 * sin(phi) + u0 * cos(phi)
    v = v0 * cos(phi) - u0 * sin(phi)
    du = (-6.7 * u ** 2 + 15.9 * r0 ** 2 + 0.01205 * (left ** 2 + right ** 2) - 0.0644 * (
        u * (left + right) + 0.45 * r0 * (left - right)) + 58 * r0 * v) / 33.3
    dv = (-29.5 * v + 11.8 * r0 - 33.3 * r0 * u) / 58
    dr = (-0.17 * v - 2.74 * r0 - 4.78 * r0 * abs(r0) + 0.45 * (
        0.01205 * (left ** 2 - right ** 2) - 0.0644 * (
            u * (left - right) + 0.45 * r0 * (left + right)))) / 6.1
    u1 = u + du * dt
    v1 = v + dv * dt
    r = r0 + dr * dt
    phi1 = phi + (r + r0) * dt / 2
    U = u1 * cos(phi) - v1 * sin(phi)
    V = u1 * sin(phi) + v1 * cos(phi)
    X = x + (u0 + U) * dt / 2
    Y = y + (v0 + V) * dt / 2

    phi1 = phi1 % (2 * pi)

    return {
        'x': X,
        'y': Y,
        'u': U,
        'v': V,
        'phi': phi1,
        'alpha': r
    }


kp = 800
ki = 3
kd = 10

# 设置你的目标点
points = [
    [0, 0],
    [0, 50],
    [50, 50],
    [50, 0],
    [0, 0]
]

# 这里随机生成状态
old_state = {
    'x': 0,
    'y': 0,
    'u': normal(0, 0.2),
    'v': normal(0, 0.2),
    # 'phi': np.random.rand() * 2 * pi,
    'phi': 3.14159/4,
    'alpha': normal(0, 0.01)
}

if __name__ == '__main__':

    re = []
    data_x = []
    data_y = []
    for _ in range(10):

        pid = PID(kp=kp, ki=ki, kd=kd, minout=-2500, maxout=500, sampleTime=0.1)
        maker = Maker(points)
        state = old_state
        data = []
        cost = 0
        for i in range(8000):

            ideal_angle = maker.LOGMaker(state,10)
            cost += maker.getCost(state)
            if ideal_angle==-1000:
                break

            output = pid.compute(state['phi'], ideal_angle)
            output = 0 if abs(output)<5 else output
            left, right = 1000 + output, 1000
            data.append([state['x'], state['y'], state['u'], state['v'], state['phi'], state['alpha'], left, right])
            data_x.append(state['x'])
            data_y.append(state['y'])
            state = simulate(state, left, right, 0.1)
        re.append(cost/i)

    print(np.mean(re))
    file_name = './data/' + time.strftime("%Y-%m-%d__%H:%M", time.localtime())
    plt.plot(data_x, data_y)
    plt.show()
    # drawer = Drawer()
    # drawer.drawFromData(data, file_name, cost)
