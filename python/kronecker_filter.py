#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2013 <+YOU OR YOUR COMPANY+>.
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
    docstring for block kronecker_filter
    """
    def __init__(self, sequence1, sequence2):
        gr.hier_block2.__init__(self,
            "kronecker_filter",
            gr.io_signature(1, 1, gr.sizeof_gr_complex),  # Input signature
            gr.io_signature(1, 1, gr.sizeof_gr_complex)) # Output signature

        n=len(sequence2)

        # Build  filterbank
        self._s2ss = blocks.stream_to_streams(gr.sizeof_gr_complex,n)
        self._ss2s = blocks.streams_to_stream(gr.sizeof_gr_complex,n)
        self._filter2=filter.interp_fir_filter_ccc(1,sequence2)
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
