#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: CDMA Tx/Rx
# Description: Example of a CDMA Transmitter/Receiver
# Generated: Tue Sep 24 16:48:52 2013
##################################################

execfile("/home/anastasl/.grc_gnuradio/rx_cdma_hier.py")
execfile("/home/anastasl/.grc_gnuradio/tx_cdma_hier.py")
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.digital.utils import tagged_streams
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import cdma_parameters
import numpy
import wx

class txrx_cdma(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="CDMA Tx/Rx")

        ##################################################
        # Variables
        ##################################################
        self.training_percent = training_percent = cdma_parameters.training_percent
        self.raw_payload_bytes_per_frame = raw_payload_bytes_per_frame = cdma_parameters.raw_payload_bytes_per_frame
        self.chips_per_symbol = chips_per_symbol = cdma_parameters.chips_per_symbol
        self.symbols_per_sec = symbols_per_sec = cdma_parameters.symbols_per_sec
        self.raw_payload = raw_payload = map(int,numpy.random.randint(0,256,raw_payload_bytes_per_frame))
        self.raw_bytes_per_sec = raw_bytes_per_sec = cdma_parameters.raw_bytes_per_sec
        self.length_tag_name = length_tag_name = cdma_parameters.length_tag_name
        self.int_f = int_f = 0
        self.int_dB = int_dB = -100
        self.header_formatter = header_formatter = cdma_parameters.header_formatter
        self.df_Hz = df_Hz = 0
        self.chips_per_sec = chips_per_sec = cdma_parameters.chips_per_sec
        self.EsN0dBest = EsN0dBest = 40
        self.EsN0dB = EsN0dB = 40
        self.Es = Es = chips_per_symbol*(1-training_percent/100.0)

        ##################################################
        # Blocks
        ##################################################
        self.notebook = self.notebook = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.notebook.AddPage(grc_wxgui.Panel(self.notebook), "0")
        self.notebook.AddPage(grc_wxgui.Panel(self.notebook), "1")
        self.notebook.AddPage(grc_wxgui.Panel(self.notebook), "2")
        self.notebook.AddPage(grc_wxgui.Panel(self.notebook), "3")
        self.GridAdd(self.notebook, 0, 0, 1, 1)
        _int_f_sizer = wx.BoxSizer(wx.VERTICAL)
        self._int_f_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_int_f_sizer,
        	value=self.int_f,
        	callback=self.set_int_f,
        	label="int_f",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._int_f_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_int_f_sizer,
        	value=self.int_f,
        	callback=self.set_int_f,
        	minimum=-chips_per_sec/2,
        	maximum=chips_per_sec/2,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_int_f_sizer)
        _int_dB_sizer = wx.BoxSizer(wx.VERTICAL)
        self._int_dB_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_int_dB_sizer,
        	value=self.int_dB,
        	callback=self.set_int_dB,
        	label="int_dB",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._int_dB_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_int_dB_sizer,
        	value=self.int_dB,
        	callback=self.set_int_dB,
        	minimum=-100,
        	maximum=100,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_int_dB_sizer)
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
        	minimum=-10e3,
        	maximum=10e3,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_df_Hz_sizer, 3, 0, 1, 1)
        _EsN0dBest_sizer = wx.BoxSizer(wx.VERTICAL)
        self._EsN0dBest_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_EsN0dBest_sizer,
        	value=self.EsN0dBest,
        	callback=self.set_EsN0dBest,
        	label="EsN0dBest",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._EsN0dBest_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_EsN0dBest_sizer,
        	value=self.EsN0dBest,
        	callback=self.set_EsN0dBest,
        	minimum=-20,
        	maximum=80,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_EsN0dBest_sizer, 4, 0, 1, 1)
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
        self.GridAdd(_EsN0dB_sizer, 2, 0, 1, 1)
        self.wxgui_scopesink2_1_0_0_0_1_0_0 = scopesink2.scope_sink_c(
        	self.notebook.GetPage(1).GetWin(),
        	title="pll_reference",
        	sample_rate=symbols_per_sec,
        	v_scale=0.5,
        	v_offset=0,
        	t_scale=0.5,
        	ac_couple=False,
        	xy_mode=True,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.notebook.GetPage(1).Add(self.wxgui_scopesink2_1_0_0_0_1_0_0.win)
        self.wxgui_scopesink2_1_0_0_0_0 = scopesink2.scope_sink_c(
        	self.notebook.GetPage(3).GetWin(),
        	title="payload_freq_corrected",
        	sample_rate=symbols_per_sec,
        	v_scale=5,
        	v_offset=0,
        	t_scale=5,
        	ac_couple=False,
        	xy_mode=True,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.notebook.GetPage(3).Add(self.wxgui_scopesink2_1_0_0_0_0.win)
        self.wxgui_scopesink2_1_0_0_0 = scopesink2.scope_sink_c(
        	self.notebook.GetPage(2).GetWin(),
        	title="header_freq_corrected",
        	sample_rate=symbols_per_sec,
        	v_scale=5,
        	v_offset=0,
        	t_scale=5,
        	ac_couple=False,
        	xy_mode=True,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.notebook.GetPage(2).Add(self.wxgui_scopesink2_1_0_0_0.win)
        self.wxgui_fftsink2_0_0_0 = fftsink2.fft_sink_c(
        	self.notebook.GetPage(0).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=chips_per_sec,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=None,
        	title="Raw data",
        	peak_hold=False,
        )
        self.notebook.GetPage(0).Add(self.wxgui_fftsink2_0_0_0.win)
        self.tx_cdma_hier_1 = tx_cdma_hier()
        self.rx_cdma_hier_0 = rx_cdma_hier(
            EsN0dBest=10,
        )
        self.digital_packet_headerparser_b_0 = digital.packet_headerparser_b(header_formatter.formatter())
        self.byte_rate = blocks.throttle(gr.sizeof_char*1, raw_bytes_per_sec)
        self.blocks_vector_source_x_0 = blocks.vector_source_b(raw_payload, True, 1, tagged_streams.make_lengthtags((raw_payload_bytes_per_frame,), (0,), length_tag_name))
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_null_sink_1_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(chips_per_sec, analog.GR_COS_WAVE, int_f, (10**(int_dB/10))**0.5, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(chips_per_sec, analog.GR_COS_WAVE, df_Hz, 1, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, ( (Es/10**(EsN0dB/10.0)/2) * chips_per_symbol)**0.5, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_source_x_0, 0), (self.byte_rate, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_add_xx_0_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_add_xx_0_0, 2))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.byte_rate, 0), (self.tx_cdma_hier_1, 0))
        self.connect((self.tx_cdma_hier_1, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.wxgui_fftsink2_0_0_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.rx_cdma_hier_0, 0))
        self.connect((self.rx_cdma_hier_0, 3), (self.wxgui_scopesink2_1_0_0_0_0, 0))
        self.connect((self.rx_cdma_hier_0, 2), (self.wxgui_scopesink2_1_0_0_0, 0))
        self.connect((self.rx_cdma_hier_0, 4), (self.wxgui_scopesink2_1_0_0_0_1_0_0, 0))
        self.connect((self.rx_cdma_hier_0, 0), (self.digital_packet_headerparser_b_0, 0))
        self.connect((self.rx_cdma_hier_0, 1), (self.blocks_null_sink_1_0, 0))

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.digital_packet_headerparser_b_0, "header_data", self.blocks_message_debug_0, "print")

# QT sink close method reimplementation

    def get_training_percent(self):
        return self.training_percent

    def set_training_percent(self, training_percent):
        self.training_percent = training_percent
        self.set_training_percent(cdma_parameters.self.training_percent)
        self.set_Es(self.chips_per_symbol*(1-self.training_percent/100.0))

    def get_raw_payload_bytes_per_frame(self):
        return self.raw_payload_bytes_per_frame

    def set_raw_payload_bytes_per_frame(self, raw_payload_bytes_per_frame):
        self.raw_payload_bytes_per_frame = raw_payload_bytes_per_frame
        self.set_raw_payload(map(int,numpy.random.randint(0,256,self.raw_payload_bytes_per_frame)))
        self.set_raw_payload_bytes_per_frame(cdma_parameters.self.raw_payload_bytes_per_frame)

    def get_chips_per_symbol(self):
        return self.chips_per_symbol

    def set_chips_per_symbol(self, chips_per_symbol):
        self.chips_per_symbol = chips_per_symbol
        self.set_Es(self.chips_per_symbol*(1-self.training_percent/100.0))
        self.set_chips_per_symbol(cdma_parameters.self.chips_per_symbol)
        self.analog_noise_source_x_0.set_amplitude(( (self.Es/10**(self.EsN0dB/10.0)/2) * self.chips_per_symbol)**0.5)

    def get_symbols_per_sec(self):
        return self.symbols_per_sec

    def set_symbols_per_sec(self, symbols_per_sec):
        self.symbols_per_sec = symbols_per_sec
        self.set_symbols_per_sec(cdma_parameters.self.symbols_per_sec)
        self.wxgui_scopesink2_1_0_0_0_1_0_0.set_sample_rate(self.symbols_per_sec)
        self.wxgui_scopesink2_1_0_0_0.set_sample_rate(self.symbols_per_sec)
        self.wxgui_scopesink2_1_0_0_0_0.set_sample_rate(self.symbols_per_sec)

    def get_raw_payload(self):
        return self.raw_payload

    def set_raw_payload(self, raw_payload):
        self.raw_payload = raw_payload

    def get_raw_bytes_per_sec(self):
        return self.raw_bytes_per_sec

    def set_raw_bytes_per_sec(self, raw_bytes_per_sec):
        self.raw_bytes_per_sec = raw_bytes_per_sec
        self.set_raw_bytes_per_sec(cdma_parameters.self.raw_bytes_per_sec)
        self.byte_rate.set_sample_rate(self.raw_bytes_per_sec)

    def get_length_tag_name(self):
        return self.length_tag_name

    def set_length_tag_name(self, length_tag_name):
        self.length_tag_name = length_tag_name
        self.set_length_tag_name(cdma_parameters.self.length_tag_name)

    def get_int_f(self):
        return self.int_f

    def set_int_f(self, int_f):
        self.int_f = int_f
        self.analog_sig_source_x_0_0.set_frequency(self.int_f)
        self._int_f_slider.set_value(self.int_f)
        self._int_f_text_box.set_value(self.int_f)

    def get_int_dB(self):
        return self.int_dB

    def set_int_dB(self, int_dB):
        self.int_dB = int_dB
        self.analog_sig_source_x_0_0.set_amplitude((10**(self.int_dB/10))**0.5)
        self._int_dB_slider.set_value(self.int_dB)
        self._int_dB_text_box.set_value(self.int_dB)

    def get_header_formatter(self):
        return self.header_formatter

    def set_header_formatter(self, header_formatter):
        self.header_formatter = header_formatter
        self.set_header_formatter(cdma_parameters.self.header_formatter)

    def get_df_Hz(self):
        return self.df_Hz

    def set_df_Hz(self, df_Hz):
        self.df_Hz = df_Hz
        self.analog_sig_source_x_0.set_frequency(self.df_Hz)
        self._df_Hz_slider.set_value(self.df_Hz)
        self._df_Hz_text_box.set_value(self.df_Hz)

    def get_chips_per_sec(self):
        return self.chips_per_sec

    def set_chips_per_sec(self, chips_per_sec):
        self.chips_per_sec = chips_per_sec
        self.set_chips_per_sec(cdma_parameters.self.chips_per_sec)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.chips_per_sec)
        self.analog_sig_source_x_0.set_sampling_freq(self.chips_per_sec)
        self.wxgui_fftsink2_0_0_0.set_sample_rate(self.chips_per_sec)

    def get_EsN0dBest(self):
        return self.EsN0dBest

    def set_EsN0dBest(self, EsN0dBest):
        self.EsN0dBest = EsN0dBest
        self._EsN0dBest_slider.set_value(self.EsN0dBest)
        self._EsN0dBest_text_box.set_value(self.EsN0dBest)

    def get_EsN0dB(self):
        return self.EsN0dB

    def set_EsN0dB(self, EsN0dB):
        self.EsN0dB = EsN0dB
        self.analog_noise_source_x_0.set_amplitude(( (self.Es/10**(self.EsN0dB/10.0)/2) * self.chips_per_symbol)**0.5)
        self._EsN0dB_slider.set_value(self.EsN0dB)
        self._EsN0dB_text_box.set_value(self.EsN0dB)

    def get_Es(self):
        return self.Es

    def set_Es(self, Es):
        self.Es = Es
        self.analog_noise_source_x_0.set_amplitude(( (self.Es/10**(self.EsN0dB/10.0)/2) * self.chips_per_symbol)**0.5)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = txrx_cdma()
    tb.Start(True)
    tb.Wait()

