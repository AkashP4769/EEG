import random
from collections import deque
import time


MAX_SIZE = 10
THRESHOLD = 1
deque = deque(maxlen=MAX_SIZE)


def main():
    active_blinks = 0
    prev_popped = 0
    
    blinks = [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0]
    index = 0

    while True:
        val = blinks[index]
        index += 1
        if index >= len(blinks):
            break

        print(f"Received value: {val}")
        prev = deque[-1] if len(deque) > 0 else 0
        print(f"Previous value in deque: {prev}")

        if prev == 0 and val >= THRESHOLD:
            active_blinks += 1
            print(f"Blink detected! active blinks: {active_blinks}")

        if val >= THRESHOLD:
            deque.append(1)
        else:
            deque.append(0)

        if len(deque) >= MAX_SIZE:
            popped = deque.popleft()
            if popped == 0 and prev_popped == 1:
                active_blinks -= 1
                print(f"Blink ended! Total blinks: {active_blinks}")

            prev_popped = popped
        
        if(active_blinks == 2):
            print("Double blink detected!")
            # active_blinks = 0  # Reset after detection
            # deque.clear()
    
        time.sleep(0.5)
        



if __name__ == "__main__":
    main()