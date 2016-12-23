import random
import math


# def get_trail_array(distance):
#     """
#     :distance: 需要划动的像素点
#     :return :array_trail,[(x,y,t)] 由x,y,及休息时间t组成的元组构成的列表
#     """
#     array_trail = []
#     array_x = [1.0 / 3, 1.0 / 4, 1.0 / 5, 2.0 / 5, 1.0 / 6, 2.0 / 7, 3.0 / 8, 2.0 / 9]
#     array_y = [-0.1, -0.2, -0.3, -0.4, -0.5, 0.1, 0.2, 0.3, 0.4, 0.5]
#     last_move_distance = random.choice([-3, +3, -4, +4, -5, +5, -6, +6])
#     distance = distance + last_move_distance
#
#     x = math.ceil(distance * random.choice(array_x))
#     y = random.choice(array_y)
#     t = random.randint(3, 10) / 100.0
#     while distance - x >= 0:
#         print(x, y, t)
#
#         array_trail.append((x, y, t))
#         distance = distance - x
#         if distance == 0:
#             break
#         x = math.ceil(distance * random.choice(array_x))
#         y = random.choice(array_y)
#         t = random.randint(3, 10) / 100.0
#
#     x = 1 if last_move_distance < 0 else -1
#     last_move_distance = abs(last_move_distance)
#     for _ in range(last_move_distance):
#         y = random.choice(array_y)
#         t = random.randint(8, 20) / 100.0
#         array_trail.append((x, y, t))
#
#     return array_trail


def trail(distance):
    trail_list = []
    d = 0
    while distance - d > 3:
        x = random.randint(1, 3)
        y = random.randint(-1, 1)
        t = random.randint(3, 10) / 100
        trail_list.append((x, y, t))
        d += x
    if distance - d == 0:
        pass
    else:
        trail_list.append((distance - d, 0, random.randint(3, 10) / 100))

    return trail_list


# l = trail(1)
# z = 0
# for x, y, t in l:
#     z += x
#     print(x, y,t)
# print(z)
#
# print(3/100)
