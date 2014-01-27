#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Timing Test Tx
# Generated: Thu Dec 12 15:31:27 2013
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import cdma.timing_parameters as tp
import numpy
import wx

class timing_test_tx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Timing Test Tx")

        ##################################################
        # Variables
        ##################################################
        self.symbol_rate = symbol_rate = tp.symbol_rate
        self.Q = Q = 15
        self.EsN0dB = EsN0dB = 20
        self.Es = Es = 1
        self.ts = ts = tp.ts
        self.samp_rate = samp_rate = symbol_rate*Q
        self.pulse = pulse = numpy.array((1, 1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, -1, 1))+0j
        self.df_Hz = df_Hz = 0
        self.N0 = N0 = 10**(-EsN0dB/10) * Es
        self.N = N = tp.N

        ##################################################
        # Blocks
        ##################################################
        _df_Hz_sizer = wx.BoxSizer(wx.VERTICAL)
        self._df_Hz_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_df_Hz_sizer,
        	value=self.df_Hz,
        	callback=self.set_df_Hz,
        	label="df_Hz",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._df_Hz_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_df_Hz_sizer,
        	value=self.df_Hz,
        	callback=self.set_df_Hz,
        	minimum=-5000,
        	maximum=5000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_df_Hz_sizer)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(Q, (pulse))
        self.blocks_vector_source_x_0 = blocks.vector_source_c(ts, True, 1, "")
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, symbol_rate)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1_0_0_0 = blocks.multiply_const_vcc((0.1, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((Es**0.5, ))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "/tmp/timing.fifo", False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, df_Hz, 1, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, (Q*N0/2)**0.5, 0)
        _EsN0dB_sizer = wx.BoxSizer(wx.VERTICAL)
        self._EsN0dB_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_EsN0dB_sizer,
        	value=self.EsN0dB,
        	callback=self.set_EsN0dB,
        	label="EsN0dB",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._EsN0dB_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_EsN0dB_sizer,
        	value=self.EsN0dB,
        	callback=self.set_EsN0dB,
        	minimum=-20,
        	maximum=80,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_EsN0dB_sizer)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_1_0_0_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.blocks_multiply_const_vxx_1_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_0, 0), (self.blocks_null_sink_0, 0))


# QT sink close method reimplementation

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_samp_rate(self.symbol_rate*self.Q)
        self.set_symbol_rate(tp.self.symbol_rate)
        self.blocks_throttle_0.set_sample_rate(self.symbol_rate)

    def get_Q(self):
        return self.Q

    def set_Q(self, Q):
        self.Q = Q
        self.set_samp_rate(self.symbol_rate*self.Q)
        self.analog_noise_source_x_0.set_amplitude((self.Q*self.N0/2)**0.5)

    def get_EsN0dB(self):
        return self.EsN0dB

    def set_EsN0dB(self, EsN0dB):
        self.EsN0dB = EsN0dB
        self.set_N0(10**(-self.EsN0dB/10) * self.Es)
        self._EsN0dB_slider.set_value(self.EsN0dB)
        self._EsN0dB_text_box.set_value(self.EsN0dB)

    def get_Es(self):
        return self.Es

    def set_Es(self, Es):
        self.Es = Es
        self.set_N0(10**(-self.EsN0dB/10) * self.Es)
        self.blocks_multiply_const_vxx_1.set_k((self.Es**0.5, ))

    def get_ts(self):
        return self.ts

    def set_ts(self, ts):
        self.ts = ts
        self.set_ts(tp.self.ts)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_pulse(self):
        return self.pulse

    def set_pulse(self, pulse):
        self.pulse = pulse
        self.interp_fir_filter_xxx_0.set_taps((self.pulse))

    def get_df_Hz(self):
        return self.df_Hz

    def set_df_Hz(self, df_Hz):
        self.df_Hz = df_Hz
        self.analog_sig_source_x_0.set_frequency(self.df_Hz)
        self._df_Hz_slider.set_value(self.df_Hz)
        self._df_Hz_text_box.set_value(self.df_Hz)

    def get_N0(self):
        return self.N0

    def set_N0(self, N0):
        self.N0 = N0
        self.analog_noise_source_x_0.set_amplitude((self.Q*self.N0/2)**0.5)

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N
        self.set_N(tp.self.N)

if __name__ == '__main__':
    import ctypes
    import os
    if os.name == 'posix':
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = timing_test_tx()
    tb.Start(True)
    tb.Wait()

