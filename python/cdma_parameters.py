import random
import numpy
from gnuradio import digital
#from gnuradio.digital.utils import tagged_streams

print "CDMA PARAMETERS"

length_tag_name = "packet_len"
num_tag_name = "packet_num"

# header info
bits_per_header=12+16+8;
header_mod = digital.constellation_bpsk();
symbols_per_header = bits_per_header/header_mod.bits_per_symbol()
if (1.0*bits_per_header)/header_mod.bits_per_symbol() != symbols_per_header:
  print "Error in evaluating symbols per header; adjusting bits per header"
  bits_per_header=(symbols_per_header+1)*header_mod.bits_per_symbol()
  symbols_per_header = bits_per_header/header_mod.bits_per_symbol()
header_formatter = digital.packet_header_default(bits_per_header,  length_tag_name,num_tag_name,header_mod.bits_per_symbol());


print "bits_per_header=",bits_per_header
print "symbols_per_header=",symbols_per_header
print "\n"


#payload info
payload_bytes_per_frame = 50;
crc_bytes=4;
coded_payload_bytes_per_frame = payload_bytes_per_frame+crc_bytes
payload_mod = digital.constellation_qpsk()
coded_payload_symbols_per_frame = (coded_payload_bytes_per_frame * 8)/payload_mod.bits_per_symbol()
if (coded_payload_bytes_per_frame * 8.0)/payload_mod.bits_per_symbol() != coded_payload_symbols_per_frame:
  print "Error in evaluating payload symbols per frame; adjusting payload bytes per frame"
  k = coded_payload_bytes_per_frame / payload_mod.bits_per_symbol()
  coded_payload_bytes_per_frame = (k+1)*payload_mod.bits_per_symbol()
  payload_bytes_per_frame = coded_payload_bytes_per_frame - crc_bytes
  coded_payload_symbols_per_frame = (coded_payload_bytes_per_frame * 8)/payload_mod.bits_per_symbol()

symbols_per_frame = symbols_per_header + coded_payload_symbols_per_frame

print "payload_bytes_per_frame=", payload_bytes_per_frame
print "coded_payload_bytes_per_frame=", coded_payload_bytes_per_frame
print "coded_payload_symbols_per_frame=", coded_payload_symbols_per_frame
print "symbols_per_frame=", symbols_per_frame
print "\n"

numpy.random.seed(666)
training_long = (2*numpy.random.randint(0,2,symbols_per_frame)-1+0j)

training_length = symbols_per_frame; # number of non-zero training symbols
if training_length > symbols_per_frame:
  print "Error in training length evaluation"
  training_length = symbols_per_frame
#training=numpy.array(training_long[0:training_length]+(symbols_per_frame-training_length)*[0,])+0j;
training=training_long[0:training_length];

print "training_length =", training_length
print "\n"

# cdma parameters
chips_per_symbol=8;	
chips_per_frame = chips_per_symbol*symbols_per_frame
pulse_training = numpy.array((1,1,1,1,-1,1,1,-1))+0j
pulse_data =numpy.array((-1,1,-1,1,-1,-1,-1,-1))+0j
training_percent = 10; # % of power for training

#timing parameters
peak_o_var = training_percent*symbols_per_frame*chips_per_symbol/(100+training_percent) #peak over variance for matched filter output 
EsN0dBthreshold = 10; 	# the threshold of switching from Acquisition to Tracking mode automatically.
epsilon = 1e-6; 	#tolerance
n_filt = 21;		# numbers of filters
freqs=[(2*k-n_filt+1)*(max(1/(2*symbols_per_frame),0.005))/(2*chips_per_symbol) for k in range(n_filt)];	#Normalized frequency list.

