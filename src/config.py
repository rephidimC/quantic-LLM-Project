import random
import numpy as np

SEED = 42

def set_seed():
    random.seed(SEED)
    np.random.seed(SEED)
