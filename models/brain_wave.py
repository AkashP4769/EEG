from enum import Enum
import os
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
from generate_perlin_noise import PerlinConfig, Perlin1D
import pandas as pd
import matplotlib.lines as mlines

#Create a brainwavetype of enum, focused, unfocused
#Would be beneficial, infuture if we want to add more brain wave types, related to eyes etc.
class BrainWaveType(Enum):
    FOCUSED = "focused"
    UNFOCUSED = "unfocused"
    MIXED = "mixed"   # contains both focused and unfocused

class BrainWave:

    # init method takes a brain wave type and an optional PerlinConfig
    # If a wave_data is provided, it will be used directly. else it will create one with config
    # If no config is provided, a default one is generated based on the wave type.
    def __init__(self, type: BrainWaveType, config: PerlinConfig=None, wave_data: pd.DataFrame=None):
        self.type = type
        self.config = config
        self.wave_data = wave_data if wave_data is not None else pd.DataFrame({
            "values": self.generate_wave_from_perlin(config),
            "type": self.type.value
        })

    # Or you can create a your own custom wave by giving a perlin configuration
    def generate_wave_from_perlin(self, config: PerlinConfig=None):
        self.config = config
        if self.config is None:
            if self.type == BrainWaveType.FOCUSED:
                self.config = PerlinConfig(length=1000, scale=0.005, amplitude=50, base=300)
            else:
                self.config = PerlinConfig(length=1000, scale=0.005, amplitude=100, base=200)

        wave_values = Perlin1D.generate_perlin_series(self.config)

        return wave_values

    # Just as it says, saves to csv
    def save_to_csv(self, path: str):
        if self.wave_data is None:
            raise ValueError("Wave data is not generated.")

        #create path if doesnt exist
        output_directory = os.path.dirname(path)
        os.makedirs(output_directory, exist_ok=True)
        self.wave_data.to_csv(path, index=False)

    def visualize_data(self, heading: str = "Brain Wave Simulation"):
        # Map type → color
        color_map = {
            BrainWaveType.FOCUSED.value: "green",
            BrainWaveType.UNFOCUSED.value: "red",
            BrainWaveType.MIXED.value: "blue"
        }

        # Build line segments
        x = np.arange(len(self.wave_data))
        y = self.wave_data["values"].values
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # Choose color for each segment based on type of its starting point
        colors = [color_map[t] for t in self.wave_data["type"].iloc[:-1]]

        # Create collection
        lc = LineCollection(segments, colors=colors, linewidth=2)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.add_collection(lc)
        ax.autoscale()
        ax.set_xlabel("Tick")
        ax.set_ylabel("Wave Value")
        plt.grid(True, linestyle="--", alpha=0.5)

        # 🔹 Custom Heading
        ax.set_title(heading, fontsize=14, fontweight="bold")

        # 🔹 Custom Legend (proxy lines)
        legend_handles = [
            mlines.Line2D([], [], color=color, linewidth=3, label=label)
            for label, color in color_map.items()
        ]
        ax.legend(handles=legend_handles, title="State", loc="upper right")

        plt.show()
