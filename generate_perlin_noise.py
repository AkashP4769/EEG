import time
from models.perlin_noise import Perlin1D, PerlinConfig


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
    focused_perlin_config = PerlinConfig(length=1000, scale=0.05, amplitude=200, base=400)
    focused_values = Perlin1D.generate_perlin_series(focused_perlin_config)
    
    print("High biased noise:", focused_values[:20])
    run_series_with_polling_rate(focused_values, 1000)


    # # Lower range noise around 100–300
    # low_perlin_config = PerlinConfig(length=1000, scale=0.05, amplitude=200, base=100, seed=42)
    # low_values = generate_perlin_series(low_perlin_config)
    # print("Low biased noise:", low_values[:20])
