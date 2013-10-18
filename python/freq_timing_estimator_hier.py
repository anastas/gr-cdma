#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: freq_timing_estimator_hier
# Author: Achilleas Anastasopoulos
# Generated: Wed Oct  9 09:05:28 2013
##################################################

from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio import digital
from gnuradio.filter import firdes
import numpy

class freq_timing_estimator_hier(gr.hier_block2):

    def __init__(self, ts, factor, alpha, samp_rate, freqs):
        gr.hier_block2.__init__(
            self, "freq_timing_estimator_hier",
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


# QT sink close method reimplementation

    def get_ts(self):
        return self.ts

    def set_ts(self, ts):
        self.ts = ts
        for i in range(self.n):
          self._filter[i].set_taps((numpy.conjugate(self.ts[::-1])))

    def get_factor(self):
        return self.factor

    def set_factor(self, factor):
        self.factor = factor
        self.blocks_peak_detector.set_threshold_factor_rise(self.factor)
        self.blocks_peak_detector.set_threshold_factor_fall(self.factor)

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.blocks_peak_detector.set_alpha(self.alpha)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_freqs(self):
        return self.freqs

    def set_freqs(self, freqs):
        self.freqs = freqs
        for i in range(self.n):
          self._filter[i].set_center_freq(self.freqs[i])


