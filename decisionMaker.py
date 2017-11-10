import math
from math import pi

RADIUS = 4


class Maker:
    def __init__(self, points):
        self.points = points
        self.s = points[0]
        self.e = points[1]
        self.pointer = 1

    def getCost(self, state):
        x, y = state['x'], state['y']
        x0, y0 = self.s
        x1, y1 = self.e

        p = x1 - x0
        q = y1 - y0

        a = (x * (p ** 2) + y * p * q - y0 * p * q + (q ** 2) * x0) / (p ** 2 + q ** 2)
        b = (x * p * q + y * (q ** 2) + (p ** 2) * y0 - p * q * x0) / (p ** 2 + q ** 2)

        dist = (a - x) ** 2 + (b - y) ** 2
        return dist

    # def getDecision(self, state):
    #     # 请在这里输入你的循迹算法, state是一个字典, 共有6个量
    #     # 可以使用字符串调取, 'x', 'y', 'u','v','phi','alpha'
    #     # 如:
    #     # x = state['x']
    #     # 请返回理想航向角, 弧度制, 范围0~2PI
    #
    #
    #     x = state['x']
    #     y = state['y']
    #
    #     x0, y0 = self.s
    #     x1, y1 = self.e
    #
    #     if ((x1 - x) ** 2 + (y1 - y) ** 2) < RADIUS ** 2:
    #         if self.pointer == (len(self.points) - 1):
    #             return -1000
    #         self.s = self.points[self.pointer]
    #         self.e = self.points[self.pointer + 1]
    #         self.pointer += 1
    #
    #     p = x1 - x0
    #     q = y1 - y0
    #
    #     a = (x * (p ** 2) + y * p * q - y0 * p * q + (q ** 2) * x0) / (p ** 2 + q ** 2)
    #     b = (x * p * q + y * (q ** 2) + (p ** 2) * y0 - p * q * x0) / (p ** 2 + q ** 2)
    #
    #     mid_point_x = (x1 + 2 * a) / 3
    #     mid_point_y = (y1 + 2 * b) / 3
    #
    #     # mid_point_x = (x1 + a) / 2
    #     # mid_point_y = (y1 + b) / 2
    #
    #     # mid_point_x = x1
    #     # mid_point_y = y1
    #
    #     if mid_point_x==x:
    #         direction = pi / 2
    #     else:
    #         direction = math.atan((mid_point_y - y) / (mid_point_x - x))
    #
    #     dx = mid_point_x - x
    #     dy = mid_point_y - y
    #
    #     if dx < 0:
    #         direction = pi + direction
    #     elif dy < 0:
    #         direction = 2 * pi + direction
    #
    #     return direction

    def LOGMaker(self, state, radius):
        x = state['x']
        y = state['y']

        x0, y0 = self.s
        x1, y1 = self.e

        p = x1 - x0
        q = y1 - y0

        a = (x * (p ** 2) + y * p * q - y0 * p * q + (q ** 2) * x0) / (p ** 2 + q ** 2)
        b = (x * p * q + y * (q ** 2) + (p ** 2) * y0 - p * q * x0) / (p ** 2 + q ** 2)

        distance = ((x - a) ** 2 + (y - b) ** 2) ** 0.5

        if distance >= radius:
            direction = math.atan2((b - y), (a - x))
            if direction<0:
               direction += 2*math.pi
            return direction

        else:
            along_distance = (radius ** 2 - distance ** 2) ** 0.5
            angle = math.atan2((y1 - y0), (x1 - x0))

            m = a + along_distance * math.cos(angle)
            n = b + along_distance * math.sin(angle)

            direction = math.atan2((n - y), (m - x))

            # dx = m - x
            # dy = n - y
            #
            # if dx < 0:
            #     direction = math.pi + direction
            # elif dy < 0:
            #     direction = 2 * math.pi + direction

            if direction < 0:
                direction += 2*math.pi

            if ((x1 - x) ** 2 + (y1 - y) ** 2) < RADIUS ** 2:
                if self.pointer == (len(self.points) - 1):
                    return -1000
                self.s = self.points[self.pointer]
                self.e = self.points[self.pointer + 1]
                self.pointer += 1
            return direction