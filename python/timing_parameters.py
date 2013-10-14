import random
import numpy
from gnuradio import digital

symbol_rate=50000
N=100

seed=666
numpy.random.seed(seed)
ts = (2*numpy.random.randint(0,2,N)-1+0j)
