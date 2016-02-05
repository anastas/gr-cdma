#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: test_amp_var_est
# Generated: Thu Feb  4 13:26:54 2016
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

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import cdma
import wx


class test_amp_var_est(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="test_amp_var_est")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.no_am = no_am = 0
        self.alpha = alpha = 0.05

        ##################################################
        # Blocks
        ##################################################
        _no_am_sizer = wx.BoxSizer(wx.VERTICAL)
        self._no_am_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_no_am_sizer,
        	value=self.no_am,
        	callback=self.set_no_am,
        	label='no_am',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._no_am_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_no_am_sizer,
        	value=self.no_am,
        	callback=self.set_no_am,
        	minimum=0,
        	maximum=1,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_no_am_sizer)
        _alpha_sizer = wx.BoxSizer(wx.VERTICAL)
        self._alpha_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_alpha_sizer,
        	value=self.alpha,
        	callback=self.set_alpha,
        	label='alpha',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._alpha_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_alpha_sizer,
        	value=self.alpha,
        	callback=self.set_alpha,
        	minimum=0,
        	maximum=1,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_alpha_sizer)
        self.wxgui_scopesink2_0_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.Add(self.wxgui_scopesink2_0_0.win)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.Add(self.wxgui_scopesink2_0.win)
        self.cdma_amp_var_est_0 = cdma.amp_var_est(alpha)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, no_am, 0)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.cdma_amp_var_est_0, 0))    
        self.connect((self.cdma_amp_var_est_0, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.cdma_amp_var_est_0, 1), (self.wxgui_scopesink2_0_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_scopesink2_0_0.set_sample_rate(self.samp_rate)

    def get_no_am(self):
        return self.no_am

    def set_no_am(self, no_am):
        self.no_am = no_am
        self._no_am_slider.set_value(self.no_am)
        self._no_am_text_box.set_value(self.no_am)
        self.analog_noise_source_x_0.set_amplitude(self.no_am)

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.cdma_amp_var_est_0.set_alpha(self.alpha)
        self._alpha_slider.set_value(self.alpha)
        self._alpha_text_box.set_value(self.alpha)


def main(top_block_cls=test_amp_var_est, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
