from models.brain_wave import BrainWave, BrainWaveType

def generate_focused_brain_wave():
    focused_bw = BrainWave(BrainWaveType.FOCUSED)
    focused_bw.visualize_data()
    focused_bw.save_to_csv("./waves/focused_brain_wave.csv")

def generate_unfocused_brain_wave():
    unfocused_bw = BrainWave(BrainWaveType.UNFOCUSED)
    unfocused_bw.visualize_data()
    unfocused_bw.save_to_csv("./waves/unfocused_brain_wave.csv")

if __name__ == "__main__":
    generate_focused_brain_wave()
    generate_unfocused_brain_wave()
