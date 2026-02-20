import random
import numpy as np

def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)

if __name__ == "__main__":
    set_seed()
    print("Seeds set.")
