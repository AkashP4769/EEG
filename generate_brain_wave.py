from models.brain_wave import BrainWave, BrainWaveType
from models.perlin_noise import PerlinConfig

# Example showing how to create a brain wave

def generate_focused_brain_wave():
    # Creates a default focused brain wave
    focused_bw = BrainWave(BrainWaveType.FOCUSED)
    focused_bw.visualize_data()

    # If you want a custom focused brain wave
    custom_config = PerlinConfig(length=1000, scale=0.005, amplitude=60, base=320)
    focused_bw_custom = BrainWave(BrainWaveType.FOCUSED, config=custom_config)
    focused_bw_custom.visualize_data()

    # Then you can save the wave data
    focused_bw_custom.save_to_csv("./waves/focused_brain_wave_custom.csv")

def generate_unfocused_brain_wave():
    # Creates a default unfocused brain wave
    unfocused_bw = BrainWave(BrainWaveType.UNFOCUSED)
    unfocused_bw.visualize_data()

    # If you want a custom unfocused brain wave
    custom_config = PerlinConfig(length=1000, scale=0.005, amplitude=80, base=180)
    unfocused_bw_custom = BrainWave(BrainWaveType.UNFOCUSED, config=custom_config)
    unfocused_bw_custom.visualize_data()

    # Then you can save the wave data
    unfocused_bw_custom.save_to_csv("./waves/unfocused_brain_wave_custom.csv")

if __name__ == "__main__":
    generate_focused_brain_wave()
    generate_unfocused_brain_wave()
