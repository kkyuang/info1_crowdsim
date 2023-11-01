from Entity import Entity
import random
import numpy as np


n = 20
Entities = [Entity(position=np.array([random.randrange(0, 100), random.randrange(0, 100)]), size=0.2, destination=np.array([random.randrange(0, 100), random.randrange(0, 100)])) for i in range(n)]

