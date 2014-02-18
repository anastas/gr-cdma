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

class kronecker_filter(gr.hier_block2):
    """
    Kronecker filter class. 
    """
    def __init__(self, sequence1, sequence2, samp_rate, center_freq):
        """
	Description:
	This block is functionally equivalent to a conventional frequency xlating FIR filter, with filter taps given by the kronecker product of sequence1 with sequence2.
	This block consists of two filtering steps. First, the received samples are filtered using a frequency xlating filter with frequency offset equal to center_freq and taps equal to sequence2.  Second, the output is fed into a S/P converter to generate len(sequence2) parallel substreams, and each substream is filtered with identical filter with taps equal to sequence1. Then all substreams are connected to a P/S converter to generate the output sequence. 

	Complexity discussion:
	Originally the filter taps have length len(sequence1)*len(sequence2).
	For the kronecker we have one filter of len(sequence2), followed by a bank of len(sequence2) filters, each of length len(sequence1) operating at a rate 1/len(sequence2), for a total complexity of roughly len(sequence2)+len(sequence1), thus resulting in considerable complexity reduction.

	Args:
	     sequence1: the identical taps of each parallel filter in the filter bank.
	     sequence2: the taps of the first filter.
	     samp_rate: the samp_rate of the first freq_xlating_fir filter.
	     center_freq: the center frequency of the freq_xlating_fir filter.
        """

        gr.hier_block2.__init__(self,
            "kronecker_filter",
            gr.io_signature(1,1, gr.sizeof_gr_complex),  # Input signature
            gr.io_signature(1,1, gr.sizeof_gr_complex)) # Output signature

        self.n = n = len(sequence2)

        # Build  filterbank
        self._s2ss = blocks.stream_to_streams(gr.sizeof_gr_complex,n)
        self._ss2s = blocks.streams_to_stream(gr.sizeof_gr_complex,n)
        self._filter2=filter.freq_xlating_fir_filter_ccc(1,sequence2,center_freq,samp_rate)
        self._filter=[0]*n
        for i in range(n):
          self._filter[i]=filter.interp_fir_filter_ccc(1,sequence1)

        # Connect blocks             
        self.connect(self, self._filter2)
        self.connect(self._filter2, self._s2ss)
        for i in range(n):
          self.connect((self._s2ss, i),self._filter[i])
          self.connect(self._filter[i],(self._ss2s, i))

        self.connect(self._ss2s,self)


    def get_sequence1(self):
    	"""
get sequence1 which is the identical taps of the parallel filters.
    	"""
	return self.sequence1

    def set_sequence1(self, sequence1):
    	"""
set sequence1 identically to taps of each parallel filter.
    	"""
	self.sequence1 = sequence1
	for i in range(self.n):
          self._filter[i].set_taps((self.sequence1))

    def get_sequence2(self):
    	"""
get sequence2 which is the taps of the first freq_xlating_fir_filter.
    	"""
	return self.sequence2

    def set_sequence2(self, sequence2):
    	"""
set sequence2 to the taps of the first freq_xlating_fir_filter.
    	"""
	self.sequence2 = sequence2
	self._filter2.set_taps(self.sequence2)
