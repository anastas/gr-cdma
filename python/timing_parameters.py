import random
import numpy
from gnuradio import digital

samp_rate=100000
N=1000

seed=666
numpy.random.seed(seed)
ts = (2*numpy.random.randint(0,2,N)-1+0j)
