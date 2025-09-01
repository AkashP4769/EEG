from enum import Enum
import os
from matplotlib import pyplot as plt
from generate_perlin_noise import PerlinConfig, Perlin1D
import pandas as pd

#Create a brainwavetype of enum, focused, unfocused
#Would be beneficial, infuture if we want to add more brain wave types, related to eyes etc.
class BrainWaveType(Enum):
    FOCUSED = "focused"
    UNFOCUSED = "unfocused"

class BrainWave:

    # init method takes a brain wave type and an optional PerlinConfig
    # If no config is provided, a default one is generated based on the wave type.
    def __init__(self, type: BrainWaveType, config: PerlinConfig=None):
        self.type = type
        self.config = config
        self.wave_data = self.generate_wave_from_perlin(self.config)

    # Or you can create a your own custom wave by giving a perlin configuration
    def generate_wave_from_perlin(self, config: PerlinConfig=None):
        self.config = config
        if self.config is None:
            if self.type == BrainWaveType.FOCUSED:
                self.config = PerlinConfig(length=1000, scale=0.005, amplitude=50, base=300)
            else:
                self.config = PerlinConfig(length=1000, scale=0.005, amplitude=100, base=200)

        wave_values = Perlin1D.generate_perlin_series(self.config)
        self.wave_data = wave_values
        return self.wave_data

    # Just as it says, saves to csv
    def save_to_csv(self, path: str):
        if self.wave_data is None:
            raise ValueError("Wave data is not generated.")

        df = pd.DataFrame({"EEG": self.wave_data, "Type": self.type.value})

        #create path if doesnt exist
        output_directory = os.path.dirname(path)
        os.makedirs(output_directory, exist_ok=True)
        df.to_csv(path, index=False)


    # If you want to see everything in a graph
    def visualize_data(self):
        if self.wave_data is None:
            raise ValueError("Wave data is not generated.")
        
        plt.figure(figsize=(12, 6))
        plt.plot(self.wave_data, label=f"EEG - {self.type.value}")
        plt.title(f"Brain Wave - {self.type.value}")
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.show()
