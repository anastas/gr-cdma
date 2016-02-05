#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: cdma_txrx
# Author: Achilleas Anastasopoulos, Zhe Feng
# Generated: Thu Feb  4 13:29:33 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from cdma_rx_hier import cdma_rx_hier  # grc-generated hier_block
from cdma_tx_hier import cdma_tx_hier  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import channels
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.digital.utils import tagged_streams
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import cdma.cdma_parameters as cp
import numpy ; numpy.random.seed(666)
import threading
import time
import wx


class cdma_txrx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="cdma_txrx")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.N0est = N0est = 1.0
        self.Esest = Esest = 1e-2
        self.training_percent = training_percent = cp.training_percent
        self.EsN0dB_est = EsN0dB_est = 10*numpy.log10( cp.epsilon+ abs(Esest)/ (abs(N0est)+cp.epsilon) ) 
        self.symbol_rate = symbol_rate = 100e3
        self.chips_per_symbol = chips_per_symbol = cp.chips_per_symbol
        self.DataEsN0dBthreshold = DataEsN0dBthreshold = 10
        self.DataEsN0dB_est = DataEsN0dB_est = EsN0dB_est + 10*numpy.log10( 1.0-training_percent/100.0 ) 
        self.samp_rate = samp_rate = symbol_rate*chips_per_symbol
        self.onoff_manual = onoff_manual = 1
        self.onoff_auto = onoff_auto = 0 if DataEsN0dB_est>DataEsN0dBthreshold else 1
        self.manual = manual = 0
        self.payload_bytes_per_frame = payload_bytes_per_frame = cp.payload_bytes_per_frame
        self.onoff = onoff = onoff_auto if manual==0 else onoff_manual
        self.freq_acq_est = freq_acq_est = 0
        self.df = df = cp.df*samp_rate
        self.TrainingEsN0dB_est = TrainingEsN0dB_est = EsN0dB_est + 10*numpy.log10( training_percent/100.0 ) 
        self.EsN0dB = EsN0dB = 20
        self.Es = Es = 1
        self.variable_static_text = variable_static_text = 'Acquisition' if onoff==1 else 'Tracking'
        self.payload = payload = map(int,numpy.random.randint(0,256,payload_bytes_per_frame))
        self.freq_est_acq = freq_est_acq = freq_acq_est
        self.fmaxt = fmaxt = cp.freqs[-1]*samp_rate
        self.dft = dft = df
        self.df_Hz = df_Hz = 0
        self.delay = delay = 0
        self.acq_threshold_dB = acq_threshold_dB = -10
        self.TrainingEsN0dB = TrainingEsN0dB = TrainingEsN0dB_est
        self.N0 = N0 = 10**(-EsN0dB/10) * Es
        self.DataEsN0dB_estimated = DataEsN0dB_estimated = DataEsN0dB_est

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
        	minimum=(cp.freqs[0]*samp_rate)-1e-6,
        	maximum=cp.freqs[-1]*samp_rate,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_df_Hz_sizer, 1, 0, 1, 1)
        _delay_sizer = wx.BoxSizer(wx.VERTICAL)
        self._delay_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_delay_sizer,
        	value=self.delay,
        	callback=self.set_delay,
        	label="delay",
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._delay_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_delay_sizer,
        	value=self.delay,
        	callback=self.set_delay,
        	minimum=0,
        	maximum=100-1,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.GridAdd(_delay_sizer, 2, 0, 1, 1)
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
        	maximum=20,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_acq_threshold_dB_sizer, 6, 0, 1, 1)
        self._variable_static_text_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.variable_static_text,
        	callback=self.set_variable_static_text,
        	label="Ack/Tra Status",
        	converter=forms.str_converter(),
        )
        self.GridAdd(self._variable_static_text_static_text, 3, 0, 1, 1)
        self._onoff_manual_chooser = forms.button(
        	parent=self.GetWin(),
        	value=self.onoff_manual,
        	callback=self.set_onoff_manual,
        	label="Manual Acq/Tra",
        	choices=[0,1],
        	labels=['Tracking','Acquisition'],
        )
        self.GridAdd(self._onoff_manual_chooser, 4, 0, 1, 1)
        self._manual_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.manual,
        	callback=self.set_manual,
        	label="Manual/Auto",
        	choices=[0,1],
        	labels=['Auto','Manual'],
        	style=wx.RA_HORIZONTAL,
        )
        self.GridAdd(self._manual_chooser, 5, 0, 1, 1)
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
                try:
                    self.set_freq_acq_est(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _freq_acq_est_thread = threading.Thread(target=_freq_acq_est_probe)
        _freq_acq_est_thread.daemon = True
        _freq_acq_est_thread.start()
        self._fmaxt_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.fmaxt,
        	callback=self.set_fmaxt,
        	label="f_max (Hz)",
        	converter=forms.float_converter(),
        )
        self.Add(self._fmaxt_static_text)
        self._dft_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.dft,
        	callback=self.set_dft,
        	label="Deltaf (Hz)",
        	converter=forms.float_converter(),
        )
        self.Add(self._dft_static_text)
        self.channels_channel_model_0 = channels.channel_model(
        	noise_voltage=(chips_per_symbol*N0/2)**0.5,
        	frequency_offset=df_Hz/samp_rate,
        	epsilon=1.0,
        	taps=((delay)*(0,)+(1,)+(100-1-delay)*(0,)),
        	noise_seed=0,
        	block_tags=False
        )
        self.cdma_tx_hier_0 = cdma_tx_hier()
        self.cdma_rx_hier_0 = cdma_rx_hier(
            acq=onoff,
            acq_threshold_dB=acq_threshold_dB,
        )
        self.blocks_vector_source_x_0_1 = blocks.vector_source_b(payload, True, 1, tagged_streams.make_lengthtags((payload_bytes_per_frame,), (0,), cp.length_tag_name))
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_char*1, (symbol_rate*cp.bits_per_uncoded_symbol)/8,True)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_vff((samp_rate, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((Es**0.5, ))
        self._TrainingEsN0dB_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.TrainingEsN0dB,
        	callback=self.set_TrainingEsN0dB,
        	label="TrainingEsN0dB_est",
        	converter=forms.float_converter(),
        )
        self.Add(self._TrainingEsN0dB_static_text)
        def _N0est_probe():
            while True:
                val = self.blocks_probe_signal_n0.level()
                try:
                    self.set_N0est(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _N0est_thread = threading.Thread(target=_N0est_probe)
        _N0est_thread.daemon = True
        _N0est_thread.start()
        def _Esest_probe():
            while True:
                val = self.blocks_probe_signal_amp.level()
                try:
                    self.set_Esest(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _Esest_thread = threading.Thread(target=_Esest_probe)
        _Esest_thread.daemon = True
        _Esest_thread.start()
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
        self.GridAdd(_EsN0dB_sizer, 0, 0, 1, 1)
        _DataEsN0dBthreshold_sizer = wx.BoxSizer(wx.VERTICAL)
        self._DataEsN0dBthreshold_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_DataEsN0dBthreshold_sizer,
        	value=self.DataEsN0dBthreshold,
        	callback=self.set_DataEsN0dBthreshold,
        	label="DataEsN0dBthreshold",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._DataEsN0dBthreshold_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_DataEsN0dBthreshold_sizer,
        	value=self.DataEsN0dBthreshold,
        	callback=self.set_DataEsN0dBthreshold,
        	minimum=0,
        	maximum=20,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_DataEsN0dBthreshold_sizer, 7, 0, 1, 1)
        self._DataEsN0dB_estimated_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.DataEsN0dB_estimated,
        	callback=self.set_DataEsN0dB_estimated,
        	label="DataEsN0dB_est",
        	converter=forms.float_converter(),
        )
        self.Add(self._DataEsN0dB_estimated_static_text)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.channels_channel_model_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.blocks_probe_freq, 0))    
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_null_sink_0_0, 0))    
        self.connect((self.blocks_tag_gate_0, 0), (self.cdma_rx_hier_0, 0))    
        self.connect((self.blocks_throttle_0_0, 0), (self.cdma_tx_hier_0, 0))    
        self.connect((self.blocks_vector_source_x_0_1, 0), (self.blocks_throttle_0_0, 0))    
        self.connect((self.cdma_rx_hier_0, 3), (self.blocks_multiply_const_vxx_1_0, 0))    
        self.connect((self.cdma_rx_hier_0, 1), (self.blocks_null_sink_0, 0))    
        self.connect((self.cdma_rx_hier_0, 2), (self.blocks_probe_signal_amp, 0))    
        self.connect((self.cdma_rx_hier_0, 0), (self.blocks_probe_signal_n0, 0))    
        self.connect((self.cdma_tx_hier_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.channels_channel_model_0, 0), (self.blocks_tag_gate_0, 0))    

    def get_N0est(self):
        return self.N0est

    def set_N0est(self, N0est):
        self.N0est = N0est
        self.set_EsN0dB_est(10*numpy.log10( cp.epsilon+ abs(self.Esest)/ (abs(self.N0est)+cp.epsilon) ) )

    def get_Esest(self):
        return self.Esest

    def set_Esest(self, Esest):
        self.Esest = Esest
        self.set_EsN0dB_est(10*numpy.log10( cp.epsilon+ abs(self.Esest)/ (abs(self.N0est)+cp.epsilon) ) )

    def get_training_percent(self):
        return self.training_percent

    def set_training_percent(self, training_percent):
        self.training_percent = training_percent
        self.set_DataEsN0dB_est(self.EsN0dB_est + 10*numpy.log10( 1.0-self.training_percent/100.0 ) )
        self.set_TrainingEsN0dB_est(self.EsN0dB_est + 10*numpy.log10( self.training_percent/100.0 ) )
        self.set_training_percent(cp.self.training_percent)

    def get_EsN0dB_est(self):
        return self.EsN0dB_est

    def set_EsN0dB_est(self, EsN0dB_est):
        self.EsN0dB_est = EsN0dB_est
        self.set_DataEsN0dB_est(self.EsN0dB_est + 10*numpy.log10( 1.0-self.training_percent/100.0 ) )
        self.set_TrainingEsN0dB_est(self.EsN0dB_est + 10*numpy.log10( self.training_percent/100.0 ) )

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_samp_rate(self.symbol_rate*self.chips_per_symbol)
        self.blocks_throttle_0_0.set_sample_rate((self.symbol_rate*cp.bits_per_uncoded_symbol)/8)

    def get_chips_per_symbol(self):
        return self.chips_per_symbol

    def set_chips_per_symbol(self, chips_per_symbol):
        self.chips_per_symbol = chips_per_symbol
        self.set_chips_per_symbol(cp.self.chips_per_symbol)
        self.set_samp_rate(self.symbol_rate*self.chips_per_symbol)
        self.channels_channel_model_0.set_noise_voltage((self.chips_per_symbol*self.N0/2)**0.5)

    def get_DataEsN0dBthreshold(self):
        return self.DataEsN0dBthreshold

    def set_DataEsN0dBthreshold(self, DataEsN0dBthreshold):
        self.DataEsN0dBthreshold = DataEsN0dBthreshold
        self._DataEsN0dBthreshold_slider.set_value(self.DataEsN0dBthreshold)
        self._DataEsN0dBthreshold_text_box.set_value(self.DataEsN0dBthreshold)
        self.set_onoff_auto(0 if self.DataEsN0dB_est>self.DataEsN0dBthreshold else 1)

    def get_DataEsN0dB_est(self):
        return self.DataEsN0dB_est

    def set_DataEsN0dB_est(self, DataEsN0dB_est):
        self.DataEsN0dB_est = DataEsN0dB_est
        self.set_DataEsN0dB_estimated(self.DataEsN0dB_est)
        self.set_onoff_auto(0 if self.DataEsN0dB_est>self.DataEsN0dBthreshold else 1)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_df(cp.self.df*self.samp_rate)
        self.set_fmaxt(cp.freqs[-1]*self.samp_rate)
        self.blocks_multiply_const_vxx_1_0.set_k((self.samp_rate, ))
        self.channels_channel_model_0.set_frequency_offset(self.df_Hz/self.samp_rate)

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
        self._manual_chooser.set_value(self.manual)
        self.set_onoff(self.onoff_auto if self.manual==0 else self.onoff_manual)

    def get_payload_bytes_per_frame(self):
        return self.payload_bytes_per_frame

    def set_payload_bytes_per_frame(self, payload_bytes_per_frame):
        self.payload_bytes_per_frame = payload_bytes_per_frame
        self.set_payload(map(int,numpy.random.randint(0,256,self.payload_bytes_per_frame)))
        self.set_payload_bytes_per_frame(cp.self.payload_bytes_per_frame)
        self.blocks_vector_source_x_0_1.set_data(self.payload, tagged_streams.make_lengthtags((self.payload_bytes_per_frame,), (0,), cp.length_tag_name))

    def get_onoff(self):
        return self.onoff

    def set_onoff(self, onoff):
        self.onoff = onoff
        self.set_variable_static_text('Acquisition' if self.onoff==1 else 'Tracking')
        self.cdma_rx_hier_0.set_acq(self.onoff)

    def get_freq_acq_est(self):
        return self.freq_acq_est

    def set_freq_acq_est(self, freq_acq_est):
        self.freq_acq_est = freq_acq_est
        self.set_freq_est_acq(self.freq_acq_est)

    def get_df(self):
        return self.df

    def set_df(self, df):
        self.df = df
        self.set_df(cp.self.df*self.samp_rate)
        self.set_dft(self.df)

    def get_TrainingEsN0dB_est(self):
        return self.TrainingEsN0dB_est

    def set_TrainingEsN0dB_est(self, TrainingEsN0dB_est):
        self.TrainingEsN0dB_est = TrainingEsN0dB_est
        self.set_TrainingEsN0dB(self.TrainingEsN0dB_est)

    def get_EsN0dB(self):
        return self.EsN0dB

    def set_EsN0dB(self, EsN0dB):
        self.EsN0dB = EsN0dB
        self._EsN0dB_slider.set_value(self.EsN0dB)
        self._EsN0dB_text_box.set_value(self.EsN0dB)
        self.set_N0(10**(-self.EsN0dB/10) * self.Es)

    def get_Es(self):
        return self.Es

    def set_Es(self, Es):
        self.Es = Es
        self.set_N0(10**(-self.EsN0dB/10) * self.Es)
        self.blocks_multiply_const_vxx_1.set_k((self.Es**0.5, ))

    def get_variable_static_text(self):
        return self.variable_static_text

    def set_variable_static_text(self, variable_static_text):
        self.variable_static_text = variable_static_text
        self._variable_static_text_static_text.set_value(self.variable_static_text)

    def get_payload(self):
        return self.payload

    def set_payload(self, payload):
        self.payload = payload
        self.blocks_vector_source_x_0_1.set_data(self.payload, tagged_streams.make_lengthtags((self.payload_bytes_per_frame,), (0,), cp.length_tag_name))

    def get_freq_est_acq(self):
        return self.freq_est_acq

    def set_freq_est_acq(self, freq_est_acq):
        self.freq_est_acq = freq_est_acq
        self._freq_est_acq_static_text.set_value(self.freq_est_acq)

    def get_fmaxt(self):
        return self.fmaxt

    def set_fmaxt(self, fmaxt):
        self.fmaxt = fmaxt
        self._fmaxt_static_text.set_value(self.fmaxt)

    def get_dft(self):
        return self.dft

    def set_dft(self, dft):
        self.dft = dft
        self._dft_static_text.set_value(self.dft)

    def get_df_Hz(self):
        return self.df_Hz

    def set_df_Hz(self, df_Hz):
        self.df_Hz = df_Hz
        self._df_Hz_slider.set_value(self.df_Hz)
        self._df_Hz_text_box.set_value(self.df_Hz)
        self.channels_channel_model_0.set_frequency_offset(self.df_Hz/self.samp_rate)

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self._delay_slider.set_value(self.delay)
        self._delay_text_box.set_value(self.delay)
        self.channels_channel_model_0.set_taps(((self.delay)*(0,)+(1,)+(100-1-self.delay)*(0,)))

    def get_acq_threshold_dB(self):
        return self.acq_threshold_dB

    def set_acq_threshold_dB(self, acq_threshold_dB):
        self.acq_threshold_dB = acq_threshold_dB
        self._acq_threshold_dB_slider.set_value(self.acq_threshold_dB)
        self._acq_threshold_dB_text_box.set_value(self.acq_threshold_dB)
        self.cdma_rx_hier_0.set_acq_threshold_dB(self.acq_threshold_dB)

    def get_TrainingEsN0dB(self):
        return self.TrainingEsN0dB

    def set_TrainingEsN0dB(self, TrainingEsN0dB):
        self.TrainingEsN0dB = TrainingEsN0dB
        self._TrainingEsN0dB_static_text.set_value(self.TrainingEsN0dB)

    def get_N0(self):
        return self.N0

    def set_N0(self, N0):
        self.N0 = N0
        self.channels_channel_model_0.set_noise_voltage((self.chips_per_symbol*self.N0/2)**0.5)

    def get_DataEsN0dB_estimated(self):
        return self.DataEsN0dB_estimated

    def set_DataEsN0dB_estimated(self, DataEsN0dB_estimated):
        self.DataEsN0dB_estimated = DataEsN0dB_estimated
        self._DataEsN0dB_estimated_static_text.set_value(self.DataEsN0dB_estimated)


def main(top_block_cls=cdma_txrx, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
