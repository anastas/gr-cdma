import random
import numpy
from gnuradio import digital
#from gnuradio.digital.utils import tagged_streams

length_tag_name = "packet_len"
num_tag_name = "packet_num"

# header info
bits_per_header=12+16+8;
header_mod = digital.constellation_bpsk();
symbols_per_header = bits_per_header/header_mod.bits_per_symbol()
if (1.0*bits_per_header)/header_mod.bits_per_symbol() != symbols_per_header:
  print "Error in evaluating symbols per header; adjusting bits per header"
  bits_per_header=(symbols_per_header+1)*header_mod.bits_per_symbol()
header_formatter = digital.packet_header_default(bits_per_header,  length_tag_name,num_tag_name,header_mod.bits_per_symbol());

print "symbols_per_header=",symbols_per_header



#payload info
payload_bytes_per_frame = 50;
crc_bytes=4;
coded_payload_bytes_per_frame = payload_bytes_per_frame+crc_bytes
payload_mod = digital.constellation_qpsk()
coded_payload_symbols_per_frame = (coded_payload_bytes_per_frame * 8)/payload_mod.bits_per_symbol()
if (coded_payload_bytes_per_frame * 8.0)/payload_mod.bits_per_symbol() != coded_payload_symbols_per_frame:
  print "Error in evaluating payload symbols per frame; adjusting payload bytes per frame"
  # add code to fix payload_bytes_per_frame

print "coded_payload_symbols_per_frame=", coded_payload_symbols_per_frame

symbols_per_frame = symbols_per_header + coded_payload_symbols_per_frame

print "symbols_per_frame=", symbols_per_frame

training_long=[
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
  ] # random long sequence (ideally should be designed to have good autocorrelation properties up to the training_length)

training_long=[];
for i in range(symbols_per_frame):
  x=random.randint(0,1)*2-1
  training_long=training_long+[x];
  

training_length = symbols_per_frame; # number of non-zero training symbols
if training_length > symbols_per_frame:
  print "Error in training length evaluation"
  training_length = symbols_per_frame
training=numpy.array(training_long[0:training_length]+(symbols_per_frame-training_length)*[0,])+0j;

print "training_length =", training_length

# cdma parameters
chips_per_symbol=16;
chips_per_frame = chips_per_symbol*symbols_per_frame
code_training=chips_per_symbol*(1,); # simple rectangular pulse
code_data=(chips_per_symbol/2)*(1,)+(chips_per_symbol/2)*(-1,); # orthogonal to training
pn_spreading=numpy.array([-1, -1, -1,  1, -1,  1, -1,  1,  1, -1, -1, -1,  1, -1,  1, -1])+0j; # should be designed so that pn_training and pn_data have good auto and cross correlation properties...

pn_training = code_training*pn_spreading;
pn_data = code_data*pn_spreading;


training_percent = 10; # % of power for training
peak_factor = 0.2; # for peak finder in CDMA Rx

# parameters determining absolute data rates
payload_bytes_per_sec=100000;
frames_per_sec = payload_bytes_per_sec/payload_bytes_per_frame
symbols_per_sec = symbols_per_frame*frames_per_sec
chips_per_sec = symbols_per_sec*chips_per_symbol

print "payload_bytes_per_sec= ",payload_bytes_per_sec
print "frames_per_sec= ",frames_per_sec
print "symbols_per_sec= ",symbols_per_sec
print "chips_per_sec= ",chips_per_sec
