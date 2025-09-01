from matplotlib import pyplot as plt
from perlin_noise import generate_perlin_series

def visualize_perlin_noise():
    """
    Lets keep base=100 and amplitude=200 for lower range noise.
    and base=400 and amplitude=200 for higher range noise.
    reduce the scale for smoother noise.
    """

    base = 150
    amplitude = 50
    scale = 0.005  # Lower scale for smoother noise
    values = generate_perlin_series(length=1000, scale=scale, base=base, amplitude=amplitude)

    plt.figure(figsize=(10, 4))
    plt.plot(values, linewidth=2)
    plt.title(f"1D Perlin Noise (base={base}, amplitude={amplitude}, scale={scale})")
    plt.xlabel("Step")
    plt.ylabel("Value")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()

if __name__ == "__main__":
    visualize_perlin_noise()