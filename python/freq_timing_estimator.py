#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2014 Achilleas Anastasopoulos, Zhe Feng.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio import digital
from gnuradio.filter import firdes
import numpy

class freq_timing_estimator(gr.hier_block2):
    """frequency timing estimator class."""
    def __init__(self, ts, factor, alpha, samp_rate, freqs):
        """
	Description:
        This block is designed to perform frequency and timing acquisition for a known training sequence in the presense of frequency and timing offset and noise. Its input is a complex stream.  It has three outputs: 
 1)  a stream of flags (bytes) indicating the begining of the training sequence (to be used from subsequent blocks to "chop" the incoming stream,
 2)  a stream with the current acquired frequency offset, and
 3)  a stream with the current acquired peak of the matched filter 

	Internally, it consists of a user defined number of parallel matched filters (as many as the size of the freqs vector), each consistng of a frequency Xlating FIR filter with sample rate samp_rate, filter taps matched to the training sequence ts, and center frequency freqs[i]. The filter outputs are magnitude squared and passed through a max block and then through a peak detector. 
 
	Args:
	     ts: the training sequence. For example, in DSSS system, it's the chip-based spread training sequence. 
	     factor: the rise and fall factors in peak detector, which is the factor determining when a peak has started and ended.  In the peak detector, an average of the signal is calculated. When the value of the signal goes over factor*average, we start looking for a peak. When the value of the signal goes below factor*average, we stop looking for a peak. factor takes values in (0,1). 
	     alpha: the smoothing factor of a moving average filter used in the peak detector takeng values in (0,1).
	     samp_rate: the sample rate of the system, which is used in the freq_xlating_fir_filter.
	     freqs: the vector of center frequencies for each matched filter. Note that for a training sequence of length Nt, each matched filter can recover a sequence with normalized frequency offset ~ 1/(2Nt).
        """

        gr.hier_block2.__init__(
            self, "freq_timing_estimator",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signaturev(3, 3, [gr.sizeof_char*1, gr.sizeof_float*1, gr.sizeof_float*1]),
        )

        ##################################################
        # Parameters
        ##################################################
        self.ts = ts
        self.factor = factor
        self.alpha = alpha
        self.samp_rate = samp_rate
        self.freqs = freqs
        self.n = n = len(freqs)
        ##################################################
        # Blocks
        ##################################################
        self._filter=[0]*self.n
        self._c2mag2=[0]*self.n
        for i in range(self.n):
          self._filter[i]= filter.freq_xlating_fir_filter_ccc(1, (numpy.conjugate(self.ts[::-1])), self.freqs[i], self.samp_rate)
          self._c2mag2[i] = blocks.complex_to_mag_squared(1)

        self.blocks_max = blocks.max_ff(1)
        self.blocks_peak_detector = blocks.peak_detector_fb(self.factor, self.factor, 0, self.alpha)

        self.blocks_argmax = blocks.argmax_fs(1)
        self.blocks_null_sink = blocks.null_sink(gr.sizeof_short*1)
        self.digital_chunks_to_symbols = digital.chunks_to_symbols_sf((freqs), 1)
        self.blocks_sample_and_hold = blocks.sample_and_hold_ff()

        ##################################################
        # Connections
        ##################################################
        for i in range(self.n):
          self.connect((self, 0), (self._filter[i], 0))
          self.connect((self._filter[i], 0), (self._c2mag2[i], 0))
          self.connect((self._c2mag2[i], 0), (self.blocks_max, i))
          self.connect((self._c2mag2[i], 0), (self.blocks_argmax, i))
        self.connect((self.blocks_max, 0), (self.blocks_peak_detector, 0))
        self.connect((self.blocks_peak_detector, 0), (self, 0))
        self.connect((self.blocks_argmax, 0), (self.blocks_null_sink, 0))
        self.connect((self.blocks_argmax, 1), (self.digital_chunks_to_symbols, 0))
        self.connect((self.digital_chunks_to_symbols, 0), (self.blocks_sample_and_hold, 0))
        self.connect((self.blocks_peak_detector, 0), (self.blocks_sample_and_hold, 1))
        self.connect((self.blocks_sample_and_hold, 0), (self, 1))
        self.connect((self.blocks_max, 0), (self, 2))



    def get_ts(self):
    	"""
get the training sequence
    	"""
        return self.ts


    def set_ts(self, ts):
    	"""
set identical training sequence to all the frequency xlating filters . 
    	"""
        self.ts = ts
        for i in range(self.n):
          self._filter[i].set_taps((numpy.conjugate(self.ts[::-1])))

    def get_factor(self):
    	"""
get the rise and fall factor of peak detector
    	"""
        return self.factor

    def set_factor(self, factor):
    	"""
set identical factor to rise factor and fall factor of peak detector
    	"""
        self.factor = factor
        self.blocks_peak_detector.set_threshold_factor_rise(self.factor)
        self.blocks_peak_detector.set_threshold_factor_fall(self.factor)

    def get_alpha(self):
    	"""
get the smoothing factor of peak detector
    	"""
        return self.alpha

    def set_alpha(self, alpha):
    	"""
set the smoothing factor of peak detector
    	"""
        self.alpha = alpha
        self.blocks_peak_detector.set_alpha(self.alpha)

    def get_samp_rate(self):
    	"""
get the sample rate of frequency xlating FIR filter
    	"""
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
    	"""
set the sample rate of frequency xlating FIR filter
    	"""
        self.samp_rate = samp_rate

    def get_freqs(self):
    	"""
get the center frequencies of frequency xlating FIR filters
    	"""
        return self.freqs

    def set_freqs(self, freqs):
    	"""
set freqs to all the center frequencies of frequency xlating FIR filters
    	"""
        self.freqs = freqs
        for i in range(self.n):
          self._filter[i].set_center_freq(self.freqs[i])


