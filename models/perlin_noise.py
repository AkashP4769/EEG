import math
import random
from datetime import datetime
import time

# ---------------------------
# 1D Perlin Noise Implementation
# ---------------------------

def fade(t):
    """Fade function as defined by Ken Perlin"""
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(a, b, t):
    """Linear interpolation"""
    return a + t * (b - a)

def grad(hash, x):
    """Gradient function for 1D"""
    g = hash & 15
    grad = 1 + (g & 7)  # Gradient value is 1-8
    if g & 8:
        grad = -grad
    return grad * x


class PerlinConfig:
    def __init__(self, length, scale, amplitude, base, seed=None):
        self.length = length
        self.scale = scale
        self.amplitude = amplitude
        self.base = base
        self.seed = seed

class Perlin1D:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.p = [i for i in range(256)]
        random.shuffle(self.p)
        self.p += self.p  # Repeat for overflow
    
    def noise(self, x):
        """Generate Perlin noise value at x"""
        xi = int(math.floor(x)) & 255
        xf = x - math.floor(x)
        
        u = fade(xf)
        
        a = self.p[xi]
        b = self.p[xi + 1]
        
        return lerp(grad(a, xf), grad(b, xf - 1), u)
    
    @staticmethod
    def generate_perlin_series(config: PerlinConfig) -> list[int]:
        """
        Generate 1D Perlin noise values.
        
        length    : number of samples
        scale     : frequency of noise
        amplitude : height of the variation
        base      : offset (e.g., 400 for higher values, 100 for lower values)
        seed      : optional random seed
        """
        perlin = Perlin1D(seed=config.seed)
        values = []
        for i in range(config.length):
            n = perlin.noise(i * config.scale)
            # Noise output is typically in range [-1, 1], so normalize to [0,1]
            n = (n + 1) / 2
            values.append((config.base + n * config.amplitude))
        return values