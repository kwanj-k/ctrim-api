""" Generate a random Code"""

import math, random


def generate_code():
    val = math.floor(10000 + random.random()*90000)
    return val
