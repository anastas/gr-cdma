#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: timing_estimator_hier
# Author: Achilleas Anastasopoulos
# Generated: Fri Oct  4 11:32:44 2013
##################################################

from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import numpy

class timing_estimator_hier(gr.hier_block2):

    def __init__(self, ts=(0+0j,), factor=0, alpha=0.01):
        gr.hier_block2.__init__(
            self, "timing_estimator_hier",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(1, 1, gr.sizeof_char*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.ts = ts
        self.factor = factor
        self.alpha = alpha

        ##################################################
        # Blocks
        ##################################################
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(1, (numpy.conjugate(ts[::-1])))
        self.blocks_peak_detector_xb_0_0 = blocks.peak_detector_fb(factor, factor, 0, alpha)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_peak_detector_xb_0_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_peak_detector_xb_0_0, 0), (self, 0))
        self.connect((self, 0), (self.interp_fir_filter_xxx_0, 0))


# QT sink close method reimplementation

    def get_ts(self):
        return self.ts

    def set_ts(self, ts):
        self.ts = ts
        self.interp_fir_filter_xxx_0.set_taps((numpy.conjugate(self.ts[::-1])))

    def get_factor(self):
        return self.factor

    def set_factor(self, factor):
        self.factor = factor
        self.blocks_peak_detector_xb_0_0.set_threshold_factor_rise(self.factor)
        self.blocks_peak_detector_xb_0_0.set_threshold_factor_fall(self.factor)

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.blocks_peak_detector_xb_0_0.set_alpha(self.alpha)


