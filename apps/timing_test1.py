#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Timing Test
# Generated: Mon Oct  7 11:34:28 2013
##################################################

execfile("/home/anastasl/.grc_gnuradio/amp_var_est.py")
execfile("/home/anastasl/.grc_gnuradio/chopper_correlator.py")
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import numbersink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import cdma
import numpy
import wx

class timing_test(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Timing Test")

        ##################################################
        # Variables
        ##################################################
        self.N = N = 10000
        self.EsN0dB = EsN0dB = 20
        self.ts = ts = 2*numpy.random.randint(0,2,N)-1+0j
        self.N0 = N0 = 10**(-EsN0dB/10)
        self.var = var = N+N0
        self.samp_rate = samp_rate = 100000
        self.peak = peak = abs(sum(ts*numpy.conjugate(ts)))**2
        self.onoff = onoff = 1

        ##################################################
        # Blocks
        ##################################################
        self._onoff_chooser = forms.button(
        	parent=self.GetWin(),
        	value=self.onoff,
        	callback=self.set_onoff,
        	label="Acq/Tra",
        	choices=[0,1],
        	labels=['Tracking','Acquisition'],
        )
        self.Add(self._onoff_chooser)
        self.wxgui_numbersink2_0_0 = numbersink2.number_sink_f(
        	self.GetWin(),
        	unit="Units",
        	minval=-100,
        	maxval=100,
        	factor=1.0,
        	decimal_places=10,
        	ref_level=0,
        	sample_rate=samp_rate/N,
        	number_rate=15,
        	average=False,
        	avg_alpha=0.001,
        	label="EsN0dB Estimate",
        	peak_hold=False,
        	show_gauge=True,
        )
        self.Add(self.wxgui_numbersink2_0_0.win)
        self.chopper_correlator_0 = chopper_correlator(
            N=N,
            filtertaps=numpy.conjugate(ts[::-1]),
        )
        self.cdma_myselector_0 = cdma.myselector(gr.sizeof_gr_complex*1, gr.sizeof_char*1, onoff, ts, 0.5*(peak/var), 0.001)
        self.blocks_vector_source_x_0 = blocks.vector_source_c(ts, True, 1, "")
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((0.5/N, ))
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, (N0/2)**0.5, 0)
        self.amp_var_est_1 = amp_var_est(
            alpha=0.1,
        )
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
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.wxgui_numbersink2_0_0, 0))
        self.connect((self.chopper_correlator_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.cdma_myselector_0, 0), (self.chopper_correlator_0, 1))
        self.connect((self.blocks_add_xx_0_0, 0), (self.chopper_correlator_0, 0))
        self.connect((self.chopper_correlator_0, 0), (self.amp_var_est_1, 0))
        self.connect((self.amp_var_est_1, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.amp_var_est_1, 1), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_add_xx_0_0, 0), (self.cdma_myselector_0, 0))


# QT sink close method reimplementation

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N
        self.set_ts(2*numpy.random.randint(0,2,self.N)-1+0j)
        self.set_var(self.N+self.N0)
        self.blocks_multiply_const_vxx_1.set_k((0.5/self.N, ))
        self.chopper_correlator_0.set_N(self.N)

    def get_EsN0dB(self):
        return self.EsN0dB

    def set_EsN0dB(self, EsN0dB):
        self.EsN0dB = EsN0dB
        self.set_N0(10**(-self.EsN0dB/10))
        self._EsN0dB_slider.set_value(self.EsN0dB)
        self._EsN0dB_text_box.set_value(self.EsN0dB)

    def get_ts(self):
        return self.ts

    def set_ts(self, ts):
        self.ts = ts
        self.set_peak(abs(sum(self.ts*numpy.conjugate(self.ts)))**2)
        self.chopper_correlator_0.set_filtertaps(numpy.conjugate(self.ts[::-1]))

    def get_N0(self):
        return self.N0

    def set_N0(self, N0):
        self.N0 = N0
        self.set_var(self.N+self.N0)
        self.analog_noise_source_x_0.set_amplitude((self.N0/2)**0.5)

    def get_var(self):
        return self.var

    def set_var(self, var):
        self.var = var

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_peak(self):
        return self.peak

    def set_peak(self, peak):
        self.peak = peak

    def get_onoff(self):
        return self.onoff

    def set_onoff(self, onoff):
        self.onoff = onoff
        print "Locking..."
        self.stop()
        self.wait()
        print "Locked"
        self.cdma_myselector_0.set_onoff(self.onoff)
        print "Unlocking..."
        self.start()
        print "Unlocked"
        self._onoff_chooser.set_value(self.onoff)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = timing_test()
    tb.Start(True)
    tb.Wait()

