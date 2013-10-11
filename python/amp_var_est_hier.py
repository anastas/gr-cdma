#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: amp_var_est_hier
# Author: Achilleas Anastasopoulos
# Description: Estimate signal amplitude and noise variance using method of moments
# Generated: Wed Oct  9 10:49:54 2013
##################################################

from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes

class amp_var_est_hier(gr.hier_block2):

    def __init__(self, alpha=0.001):
        gr.hier_block2.__init__(
            self, "amp_var_est_hier",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signaturev(2, 2, [gr.sizeof_float*1, gr.sizeof_float*1]),
        )

        ##################################################
        # Parameters
        ##################################################
        self.alpha = alpha

        ##################################################
        # Blocks
        ##################################################
        self.single_pole_iir_filter_xx_0_0_1_0 = filter.single_pole_iir_filter_cc(alpha, 1)
        self.single_pole_iir_filter_xx_0_0_1 = filter.single_pole_iir_filter_ff(alpha, 1)
        self.blocks_sub_xx_0_0 = blocks.sub_ff(1)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((0.5, ))
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.single_pole_iir_filter_xx_0_0_1, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.single_pole_iir_filter_xx_0_0_1_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0_0_1, 0), (self.blocks_sub_xx_0_0, 0))
        self.connect((self.blocks_sub_xx_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0_0_1_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_sub_xx_0_0, 1))
        self.connect((self.blocks_complex_to_mag_0, 0), (self, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self, 1))


# QT sink close method reimplementation

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.single_pole_iir_filter_xx_0_0_1.set_taps(self.alpha)
        self.single_pole_iir_filter_xx_0_0_1_0.set_taps(self.alpha)


