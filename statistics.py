"""
Generate all important statistics value
"""
import numpy as np
from random import random


def expotential_value(lambda_value):
    w = 1 - random()
    return -1 * (np.log(w)/lambda_value)
