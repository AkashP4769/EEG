import pandas as pd
from models.brain_wave import BrainWave, BrainWaveType
from models.perlin_noise import PerlinConfig, Perlin1D

# You can simulate how the brain waves will be recieved
# just like from our sensor
# You can switch from focused and unfocused brain waves by pressing 'space' key
# tick represents how many times the simulation is run in a second, its like polling

def simulate_brain_signal(ticks_per_second: int, focused_config: PerlinConfig, unfocused_config: PerlinConfig) -> pd.DataFrame:
    import time
    from pynput import keyboard

    perlin1 = Perlin1D(seed=focused_config.seed)
    perlin2 = Perlin1D(seed=unfocused_config.seed)
    keys_pressed = set()
    wave_values = []
    wave_types = []

    alpha = 0.0  # blending factor: 0 = unfocused, 1 = focused
    transition_speed = 0.01  # how fast to transition per tick

    def on_press(key):
        try:
            keys_pressed.add(key.char)
        except AttributeError:
            keys_pressed.add(str(key))

    def on_release(key):
        try:
            keys_pressed.discard(key.char)
        except AttributeError:
            keys_pressed.discard(str(key))
        if key == keyboard.Key.esc:  # Stop loop if ESC pressed
            return False

    def simulation_loop(ticks_per_second=60):
        nonlocal alpha
        tick_duration = 1.0 / ticks_per_second
        last_time = time.perf_counter()
        i = 0

        while True:
            now = time.perf_counter()
            if now - last_time >= tick_duration:
                last_time = now

                # --- INPUT HANDLING ---
                target_alpha = 1.0 if "Key.space" in keys_pressed else 0.0
                # Smoothly move alpha toward target_alpha
                if alpha < target_alpha:
                    alpha = min(target_alpha, alpha + transition_speed)
                elif alpha > target_alpha:
                    alpha = max(target_alpha, alpha - transition_speed)

                # --- NOISE GENERATION ---
                n1 = (perlin1.noise(i * focused_config.scale) + 1) / 2
                n1 = focused_config.base + n1 * focused_config.amplitude

                n2 = (perlin2.noise(i * unfocused_config.scale) + 1) / 2
                n2 = unfocused_config.base + n2 * unfocused_config.amplitude

                # Blend between the two noises
                n = (1 - alpha) * n2 + alpha * n1
                wave_values.append(n)

                if alpha < 0.2:
                    wave_types.append(BrainWaveType.UNFOCUSED.value)
                elif alpha > 0.8:
                    wave_types.append(BrainWaveType.FOCUSED.value)
                else:
                    wave_types.append(BrainWaveType.MIXED.value)

                state = "mixed"
                if alpha < 0.2:
                    state = "unfocused"
                elif alpha > 0.8:
                    state = "focused"

                print(f"{state} (α={alpha:.2f}) - {n:.2f}")

                i += 1

                # break condition for demo
                if "Key.esc" in keys_pressed:
                    print("Quitting...")
                    break

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        simulation_loop(ticks_per_second=ticks_per_second)

    wave_data = pd.DataFrame({
        "values": wave_values,
        "type": wave_types
    })

    return wave_data

if __name__ == "__main__":
    focused_config = PerlinConfig(length=1000, scale=0.005, amplitude=100, base=500)
    unfocused_config = PerlinConfig(length=1000, scale=0.005, amplitude=100, base=100)

    wave_data = simulate_brain_signal(ticks_per_second=60, focused_config=focused_config, unfocused_config=unfocused_config)
    brain_wave = BrainWave(type=BrainWaveType.MIXED, wave_data=wave_data)

    brain_wave.visualize_data(heading="Simulated Brain Wave (Focused vs Mixed vs Unfocused)")
    brain_wave.save_to_csv("./waves/simulated_brain_wave.csv")