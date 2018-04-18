#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
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

import numpy
from gnuradio import gr

class pi_controller(gr.sync_block):
    """
    docstring for block pi_controller
    """
    def __init__(self, Kp, Ki, reset):
        gr.sync_block.__init__(self,
            name="pi_controller",
            in_sig=[numpy.float32],
            out_sig=[numpy.float32])
        self.Kp = Kp
        self.Ki = Ki
        self.reset = reset
        self.ff_taps = numpy.array([Kp + Ki, -Kp], float)
        self.x = numpy.zeros(2, float)
        self.y = numpy.zeros(2, float)


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out0 = output_items[0]

        if (self.reset != 0):
            self.x[:] = 0
            self.y[:] = 0
            out0[:] = 0
        else:
            for i in range(len(in0)):
                self.x[1] = self.x[0]
                self.x[0] = in0[i]
                self.y[1] = self.y[0]
                self.y[0] = self.y[1] + numpy.sum(self.x * self.ff_taps)
                out0[i] = self.y[0]

        return len(output_items[0])

    def get_Kp(self):
        return self.Kp

    def set_Kp(self, Kp):
        self.Kp = Kp
        self.ff_taps = numpy.array([self.Kp + self.Ki, -self.Kp], float)

    def get_Ki(self):
        return self.Kp

    def set_Ki(self, Ki):
        self.Ki = Ki
        self.ff_taps = numpy.array([self.Kp + self.Ki, -self.Kp], float)

    def get_reset(self):
        return self.reset

    def set_reset(self, reset):
        self.reset = reset

