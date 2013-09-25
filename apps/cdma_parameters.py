import numpy
from gnuradio import digital
#from gnuradio.digital.utils import tagged_streams



symbols_per_frame=200;
chips_per_symbol=16;
chips_per_frame = chips_per_symbol*symbols_per_frame

bits_per_header=12+16+8;
crc_bytes=4;

raw_bytes_per_sec=100000;

code_training=chips_per_symbol*(1,);
code_data=(chips_per_symbol/2)*(1,)+(chips_per_symbol/2)*(-1,);
pn_spreading=numpy.array([-1, -1, -1,  1, -1,  1, -1,  1,  1, -1, -1, -1,  1, -1,  1, -1])+0j;

pn_training = code_training*pn_spreading;
pn_data = code_data*pn_spreading;

training=numpy.array([
 -1., -1., -1.,  1.,  1.,  1.,  1.,  1.,  1., -1., -1.,  1.,  1.,  1., -1.,  1.,  1., -1.,
 -1.,  1.,  1.,  1.,  1., -1.,  1., -1.,  1.,  1.,  1.,  1., -1.,  1.,  1.,  1., -1.,  1.,
 -1.,  1., -1., -1.,  1., -1.,  1.,  1., -1.,  1., -1.,  1., -1., -1.,  1.,  1.,  1.,  1.,
 -1.,  1.,  1.,  1., -1., -1., -1., -1.,  1.,  1., -1., -1.,  1.,  1.,  1.,  1.,  1., -1.,
  1.,  1., -1., -1., -1.,  1., -1.,  1., -1., -1., -1., -1., -1., -1.,  1., -1.,  1., -1.,
  1., -1.,  1., -1.,  1.,  1.,  1.,  1., -1.,  1.,  1.,  1., -1.,  1., -1., -1., -1.,  1.,
  1., -1., -1., -1.,  1.,  1., -1.,  1., -1., -1.,  1.,  1., -1.,  1., -1., -1.,  1., -1.,
 -1.,  1., -1., -1., -1., -1., -1., -1.,  1., -1., -1.,  1.,  1.,  1.,  1.,  1., -1., -1.,
 -1.,  1.,  1., -1., -1.,  1., -1., -1., -1.,  1., -1.,  1.,  1.,  1.,  1., -1.,  1.,  1.,
  1., -1., -1., -1., -1., -1., -1.,  1.,  1.,  1.,  1.,  1., -1., -1.,  1., -1.,  1.,  1.,
 -1.,  1.,  1.,  1., -1.,  1., -1.,  1., -1., -1., -1., -1., -1., -1.,  1.,  1.,  1.,  1.,
  1.,  1.,
  ])

training_length = 200; # number of non-zero training symbols
training_nz=numpy.array(training[0:training_length]);

training_percent = 10; # in power

length_tag_name = "packet_len"
num_tag_name = "packet_num"
header_mod = digital.constellation_bpsk();
header_formatter = digital.packet_header_default(bits_per_header,  length_tag_name,num_tag_name,header_mod.bits_per_symbol());
payload_mod = digital.constellation_qpsk()

symbols_per_header = bits_per_header/header_mod.bits_per_symbol()

payload_symbols_per_frame = symbols_per_frame-symbols_per_header
payload_bytes_per_frame = (payload_symbols_per_frame*payload_mod.bits_per_symbol())/8
raw_payload_bytes_per_frame = payload_bytes_per_frame-crc_bytes

symbols_per_sec = symbols_per_frame*raw_bytes_per_sec/raw_payload_bytes_per_frame
frames_per_sec = symbols_per_sec/symbols_per_frame
chips_per_sec = symbols_per_sec*chips_per_symbol

peak_factor = 0.1
