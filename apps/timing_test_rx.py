#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Timing Test Rx
# Generated: Thu Dec 12 15:34:03 2013
##################################################

execfile("/home/anastas/.grc_gnuradio/amp_var_est3_hier.py")
execfile("/home/anastas/.grc_gnuradio/chopper_correlator.py")
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import cdma
import cdma.timing_parameters as tp
import numpy
import threading
import time
import wx

class timing_test_rx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Timing Test Rx")

        ##################################################
        # Variables
        ##################################################
        self.epsilon = epsilon = 1e-12
        self.N0est = N0est = 1e-2
        self.Esest = Esest = 1
        self.EsN0dBthreshold = EsN0dBthreshold = 10
        self.EsN0dBest = EsN0dBest = 10*numpy.log10(Esest/(N0est+epsilon)+epsilon)
        self.ts = ts = tp.ts
        self.symbol_rate = symbol_rate = tp.symbol_rate
        self.pulse = pulse = numpy.array((1, 1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, -1, 1))+0j
        self.onoff_manual = onoff_manual = 1
        self.onoff_auto = onoff_auto = 0 if EsN0dBest>EsN0dBthreshold else 1
        self.manual = manual = 1
        self.Q = Q = 15
        self.N = N = tp.N
        self.total = total = numpy.convolve(pulse, numpy.kron(ts,(1,)+(Q-1)*(0,))[:(N-1)*Q+1:])
        self.onoff = onoff = onoff_auto if manual==0 else onoff_manual
        self.n_filt = n_filt = 21
        self.freq_acq_est = freq_acq_est = 0
        self.df = df = symbol_rate/N/2
        self.variable_static_text_0 = variable_static_text_0 = 'Acquisition' if onoff==1 else 'Tracking'
        self.total1 = total1 = (0+0j,) if onoff==0 else total
        self.samp_rate = samp_rate = symbol_rate*Q
        self.peak_o_var = peak_o_var = N*Q/2
        self.freqs = freqs = [(2*k-n_filt+1)*df/2 for k in range(n_filt)]
        self.freq_est_acq = freq_est_acq = freq_acq_est
        self.acq_threshold_dB = acq_threshold_dB = -10
        self.EsN0dB_est = EsN0dB_est = EsN0dBest

        ##################################################
        # Blocks
        ##################################################
        self.blocks_probe_signal_n0 = blocks.probe_signal_f()
        self.blocks_probe_signal_amp = blocks.probe_signal_f()
        self.blocks_probe_freq = blocks.probe_signal_f()
        _acq_threshold_dB_sizer = wx.BoxSizer(wx.VERTICAL)
        self._acq_threshold_dB_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_acq_threshold_dB_sizer,
        	value=self.acq_threshold_dB,
        	callback=self.set_acq_threshold_dB,
        	label="acq_threshold_dB",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._acq_threshold_dB_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_acq_threshold_dB_sizer,
        	value=self.acq_threshold_dB,
        	callback=self.set_acq_threshold_dB,
        	minimum=-20,
        	maximum=10,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_acq_threshold_dB_sizer)
        self.wxgui_scopesink2_1_0 = scopesink2.scope_sink_c(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=symbol_rate,
        	v_scale=Q/10.0,
        	v_offset=0,
        	t_scale=Q/10.0,
        	ac_couple=False,
        	xy_mode=True,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.Add(self.wxgui_scopesink2_1_0.win)
        self._variable_static_text_0_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.variable_static_text_0,
        	callback=self.set_variable_static_text_0,
        	label="Acq/Tra Status",
        	converter=forms.str_converter(),
        )
        self.Add(self._variable_static_text_0_static_text)
        self._onoff_manual_chooser = forms.button(
        	parent=self.GetWin(),
        	value=self.onoff_manual,
        	callback=self.set_onoff_manual,
        	label="Manual Acq/Tra",
        	choices=[0,1],
        	labels=['Tracking','Acquisition'],
        )
        self.Add(self._onoff_manual_chooser)
        self._manual_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.manual,
        	callback=self.set_manual,
        	label="Manual/Auto",
        	choices=[0,1],
        	labels=['Auto','Manual'],
        	style=wx.RA_HORIZONTAL,
        )
        self.Add(self._manual_chooser)
        self.freq_timing_estimator_hier_0 = cdma.freq_timing_estimator_hier(
            ts=total1,
            factor=10**(acq_threshold_dB/10)*(peak_o_var),
            alpha=0.01,
            samp_rate=samp_rate,
            freqs=freqs,
        )
        self._freq_est_acq_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.freq_est_acq,
        	callback=self.set_freq_est_acq,
        	label='freq_est_acq',
        	converter=forms.float_converter(),
        )
        self.Add(self._freq_est_acq_static_text)
        def _freq_acq_est_probe():
        	while True:
        		val = self.blocks_probe_freq.level()
        		try: self.set_freq_acq_est(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(10))
        _freq_acq_est_thread = threading.Thread(target=_freq_acq_est_probe)
        _freq_acq_est_thread.daemon = True
        _freq_acq_est_thread.start()
        self.chopper_correlator_1 = chopper_correlator(
            N=N,
            ts=ts,
            Q=Q,
            pulse=pulse,
        )
        self.cdma_flag_gen_0 = cdma.flag_gen(N*Q, onoff)
        self.blocks_vco_c_0 = blocks.vco_c(samp_rate, 2*numpy.pi, 1)
        self.blocks_null_sink_0_2 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0_0_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((2.0, ))
        self.blocks_multiply_conjugate_cc_1 = blocks.multiply_conjugate_cc(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, "/tmp/timing.fifo", False)
        self.amp_var_est3_hier_0 = amp_var_est3_hier(
            alpha=0.001,
        )
        def _N0est_probe():
        	while True:
        		val = self.blocks_probe_signal_n0.level()
        		try: self.set_N0est(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(10))
        _N0est_thread = threading.Thread(target=_N0est_probe)
        _N0est_thread.daemon = True
        _N0est_thread.start()
        def _Esest_probe():
        	while True:
        		val = self.blocks_probe_signal_amp.level()
        		try: self.set_Esest(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(10))
        _Esest_thread = threading.Thread(target=_Esest_probe)
        _Esest_thread.daemon = True
        _Esest_thread.start()
        self._EsN0dB_est_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.EsN0dB_est,
        	callback=self.set_EsN0dB_est,
        	label="EsN0dB_est",
        	converter=forms.float_converter(),
        )
        self.Add(self._EsN0dB_est_static_text)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.freq_timing_estimator_hier_0, 0))
        self.connect((self.freq_timing_estimator_hier_0, 0), (self.cdma_flag_gen_0, 0))
        self.connect((self.freq_timing_estimator_hier_0, 2), (self.blocks_null_sink_0_1, 0))
        self.connect((self.blocks_vco_c_0, 0), (self.blocks_multiply_conjugate_cc_1, 1))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_multiply_conjugate_cc_1, 0))
        self.connect((self.freq_timing_estimator_hier_0, 1), (self.blocks_vco_c_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_1, 0), (self.chopper_correlator_1, 0))
        self.connect((self.cdma_flag_gen_0, 0), (self.chopper_correlator_1, 1))
        self.connect((self.chopper_correlator_1, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.chopper_correlator_1, 1), (self.blocks_null_sink_0_0, 0))
        self.connect((self.chopper_correlator_1, 2), (self.blocks_null_sink_0_0_1, 0))
        self.connect((self.freq_timing_estimator_hier_0, 1), (self.blocks_probe_freq, 0))
        self.connect((self.chopper_correlator_1, 2), (self.amp_var_est3_hier_0, 0))
        self.connect((self.amp_var_est3_hier_0, 1), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.amp_var_est3_hier_0, 0), (self.blocks_probe_signal_amp, 0))
        self.connect((self.chopper_correlator_1, 3), (self.blocks_null_sink_0_2, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_probe_signal_n0, 0))
        self.connect((self.chopper_correlator_1, 2), (self.wxgui_scopesink2_1_0, 0))


# QT sink close method reimplementation

    def get_epsilon(self):
        return self.epsilon

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon
        self.set_EsN0dBest(10*numpy.log10(self.Esest/(self.N0est+self.epsilon)+self.epsilon))

    def get_N0est(self):
        return self.N0est

    def set_N0est(self, N0est):
        self.N0est = N0est
        self.set_EsN0dBest(10*numpy.log10(self.Esest/(self.N0est+self.epsilon)+self.epsilon))

    def get_Esest(self):
        return self.Esest

    def set_Esest(self, Esest):
        self.Esest = Esest
        self.set_EsN0dBest(10*numpy.log10(self.Esest/(self.N0est+self.epsilon)+self.epsilon))

    def get_EsN0dBthreshold(self):
        return self.EsN0dBthreshold

    def set_EsN0dBthreshold(self, EsN0dBthreshold):
        self.EsN0dBthreshold = EsN0dBthreshold
        self.set_onoff_auto(0 if self.EsN0dBest>self.EsN0dBthreshold else 1)

    def get_EsN0dBest(self):
        return self.EsN0dBest

    def set_EsN0dBest(self, EsN0dBest):
        self.EsN0dBest = EsN0dBest
        self.set_onoff_auto(0 if self.EsN0dBest>self.EsN0dBthreshold else 1)
        self.set_EsN0dB_est(self.EsN0dBest)

    def get_ts(self):
        return self.ts

    def set_ts(self, ts):
        self.ts = ts
        self.set_ts(tp.self.ts)
        self.set_total(numpy.convolve(self.pulse, numpy.kron(self.ts,(1,)+(self.Q-1)*(0,))[:(self.N-1)*self.Q+1:]))
        self.chopper_correlator_1.set_ts(self.ts)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_samp_rate(self.symbol_rate*self.Q)
        self.set_symbol_rate(tp.self.symbol_rate)
        self.set_df(self.symbol_rate/self.N/2)
        self.wxgui_scopesink2_1_0.set_sample_rate(self.symbol_rate)

    def get_pulse(self):
        return self.pulse

    def set_pulse(self, pulse):
        self.pulse = pulse
        self.set_total(numpy.convolve(self.pulse, numpy.kron(self.ts,(1,)+(self.Q-1)*(0,))[:(self.N-1)*self.Q+1:]))
        self.chopper_correlator_1.set_pulse(self.pulse)

    def get_onoff_manual(self):
        return self.onoff_manual

    def set_onoff_manual(self, onoff_manual):
        self.onoff_manual = onoff_manual
        self.set_onoff(self.onoff_auto if self.manual==0 else self.onoff_manual)
        self._onoff_manual_chooser.set_value(self.onoff_manual)

    def get_onoff_auto(self):
        return self.onoff_auto

    def set_onoff_auto(self, onoff_auto):
        self.onoff_auto = onoff_auto
        self.set_onoff(self.onoff_auto if self.manual==0 else self.onoff_manual)

    def get_manual(self):
        return self.manual

    def set_manual(self, manual):
        self.manual = manual
        self.set_onoff(self.onoff_auto if self.manual==0 else self.onoff_manual)
        self._manual_chooser.set_value(self.manual)

    def get_Q(self):
        return self.Q

    def set_Q(self, Q):
        self.Q = Q
        self.set_samp_rate(self.symbol_rate*self.Q)
        self.set_total(numpy.convolve(self.pulse, numpy.kron(self.ts,(1,)+(self.Q-1)*(0,))[:(self.N-1)*self.Q+1:]))
        self.set_peak_o_var(self.N*self.Q/2)
        self.chopper_correlator_1.set_Q(self.Q)

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N
        self.set_N(tp.self.N)
        self.set_df(self.symbol_rate/self.N/2)
        self.set_total(numpy.convolve(self.pulse, numpy.kron(self.ts,(1,)+(self.Q-1)*(0,))[:(self.N-1)*self.Q+1:]))
        self.set_peak_o_var(self.N*self.Q/2)
        self.chopper_correlator_1.set_N(self.N)

    def get_total(self):
        return self.total

    def set_total(self, total):
        self.total = total
        self.set_total1((0+0j,) if self.onoff==0 else self.total)

    def get_onoff(self):
        return self.onoff

    def set_onoff(self, onoff):
        self.onoff = onoff
        self.set_total1((0+0j,) if self.onoff==0 else self.total)
        self.cdma_flag_gen_0.set_onoff(self.onoff)
        self.set_variable_static_text_0('Acquisition' if self.onoff==1 else 'Tracking')

    def get_n_filt(self):
        return self.n_filt

    def set_n_filt(self, n_filt):
        self.n_filt = n_filt
        self.set_freqs([(2*k-self.n_filt+1)*self.df/2 for k in range(self.n_filt)])

    def get_freq_acq_est(self):
        return self.freq_acq_est

    def set_freq_acq_est(self, freq_acq_est):
        self.freq_acq_est = freq_acq_est
        self.set_freq_est_acq(self.freq_acq_est)

    def get_df(self):
        return self.df

    def set_df(self, df):
        self.df = df
        self.set_freqs([(2*k-self.n_filt+1)*self.df/2 for k in range(self.n_filt)])

    def get_variable_static_text_0(self):
        return self.variable_static_text_0

    def set_variable_static_text_0(self, variable_static_text_0):
        self.variable_static_text_0 = variable_static_text_0
        self._variable_static_text_0_static_text.set_value(self.variable_static_text_0)

    def get_total1(self):
        return self.total1

    def set_total1(self, total1):
        self.total1 = total1
        self.freq_timing_estimator_hier_0.set_ts(self.total1)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_timing_estimator_hier_0.set_samp_rate(self.samp_rate)

    def get_peak_o_var(self):
        return self.peak_o_var

    def set_peak_o_var(self, peak_o_var):
        self.peak_o_var = peak_o_var
        self.freq_timing_estimator_hier_0.set_factor(10**(self.acq_threshold_dB/10)*(self.peak_o_var))

    def get_freqs(self):
        return self.freqs

    def set_freqs(self, freqs):
        self.freqs = freqs
        self.freq_timing_estimator_hier_0.set_freqs(self.freqs)

    def get_freq_est_acq(self):
        return self.freq_est_acq

    def set_freq_est_acq(self, freq_est_acq):
        self.freq_est_acq = freq_est_acq
        self._freq_est_acq_static_text.set_value(self.freq_est_acq)

    def get_acq_threshold_dB(self):
        return self.acq_threshold_dB

    def set_acq_threshold_dB(self, acq_threshold_dB):
        self.acq_threshold_dB = acq_threshold_dB
        self.freq_timing_estimator_hier_0.set_factor(10**(self.acq_threshold_dB/10)*(self.peak_o_var))
        self._acq_threshold_dB_slider.set_value(self.acq_threshold_dB)
        self._acq_threshold_dB_text_box.set_value(self.acq_threshold_dB)

    def get_EsN0dB_est(self):
        return self.EsN0dB_est

    def set_EsN0dB_est(self, EsN0dB_est):
        self.EsN0dB_est = EsN0dB_est
        self._EsN0dB_est_static_text.set_value(self.EsN0dB_est)

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
    tb = timing_test_rx()
    tb.Start(True)
    tb.Wait()

