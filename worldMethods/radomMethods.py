import random


def random_time(value_range=(300, 500)):
    """
    生成单个区间的随机值
    参数：
        value_range: 数值范围元组 (start, end)
    返回：
        区间内的随机值
    """
    return random.randint(value_range[0], value_range[1])


def random_position(range1, range2):
    """
    生成两个独立区间的随机值
    参数：
        range1: 第一个区间元组 (start1, end1)
        range2: 第二个区间元组 (start2, end2)
    返回：
        包含两个随机值的元组 (random1, random2)
    """
    rand1 = random_time((range1[0], range1[1]))
    rand2 = random_time((range2[0], range2[1]))
    return (rand1, rand2)


# 使用示例
if __name__ == "__main__":
    print(random_time())
    print(random_position((100, 500), (545, 854)))
