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


# ---------------------------
# Wrapper with Amplitude + Offset
# ---------------------------

def generate_perlin_series(length=1000, scale=0.1, amplitude=100, base=0, seed=None) -> list[int]:
    """
    Generate 1D Perlin noise values.
    
    length    : number of samples
    scale     : frequency of noise
    amplitude : height of the variation
    base      : offset (e.g., 400 for higher values, 100 for lower values)
    seed      : optional random seed
    """
    perlin = Perlin1D(seed=seed)
    values = []
    for i in range(length):
        n = perlin.noise(i * scale)
        # Noise output is typically in range [-1, 1], so normalize to [0,1]
        n = (n + 1) / 2
        values.append((base + n * amplitude))
    return values


# ---------------------------
# Example usage
# ---------------------------


def run_series_with_polling_rate(perlin_values: list[int], polling_rate: int) -> None:
    """
    Print items from a list with a given rate (items per second).
    
    values : list of items
    rate   : number of items per second
    """
    delay = 1.0 / polling_rate  # time between prints
    for v in perlin_values:
        print(v)
        time.sleep(delay)



if __name__ == "__main__":
    # Higher range noise around 400–600
    high_values = generate_perlin_series(length=1000, scale=0.05, amplitude=200, base=400, seed=42)
    print("High biased noise:", high_values[:20])

    run_series_with_polling_rate(high_values, 1000)


    # # Lower range noise around 100–300
    # low_values = generate_perlin_series(length=100, scale=0.05, amplitude=200, base=100, seed=42)
    # print("Low biased noise:", low_values[:20])
