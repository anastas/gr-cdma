#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2013 <+YOU OR YOUR COMPANY+>.
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

from gnuradio import gr, blocks, filter
import cdma

class myselector(gr.hier_block2):
    """
    docstring for block myselector
    """
    def __init__(self, item_size_in, item_size_out, onoff,ts,factor,alpha):
        gr.hier_block2.__init__(self,
            "myselector",
            gr.io_signature(1,1, item_size_in),  # Input signature
            gr.io_signature(1,1, item_size_out), # Output signature
        )

        self.item_size_in = item_size_in
        self.item_size_out = item_size_out
        self.onoff=onoff

        #print self.item_size_in, self.item_size_out, self.onoff
     
        # Define blocks and connect them

        # This is the BIG block
        self.A=cdma.timing_estimator_hier(ts,factor,alpha)
        #self.Ab=blocks.multiply_const_cc(2.0+0j)
        #self.Ab=filter.interp_fir_filter_ccc(1,ts)
        #self.A1=blocks.complex_to_mag_squared()
        #self.Ae=blocks.float_to_char()
        #self.Ae=blocks.complex_to_mag_squared()
        #self.connect(self.Ab, self.A1, self.Ae)
        #self.connect(self.Ab, self.Ae)

        # This is the SMALL block
        self.Ob=blocks.multiply_const_cc(0.0)
        self.O1=blocks.complex_to_mag_squared()
        self.Oe=blocks.float_to_char()
        #self.Oe=blocks.complex_to_mag_squared()
        self.connect(self.Ob, self.O1, self.Oe)
        #self.connect(self.Ob, self.Oe)

        # null sources/sinks for connecting inactive block
        self.nso=blocks.null_source(item_size_in)
        self.h=blocks.head(item_size_in, 0)
        self.connect(self.nso, self.h)

        self.nsi=blocks.null_sink(item_size_out)

        if self.onoff==0:
          self._connect_off()
        else:
          self._connect_on()


    def _disconnect_on(self):
        """
        Disconnect from the on position
        """
        print "Start disconnecting on"
        self.disconnect(self, self.A)
        self.disconnect(self.A,self)
        self.disconnect(self.h,self.Ob)
        self.disconnect(self.Oe,self.nsi)
        print "Stop disconnecting on"

    def _disconnect_off(self):
        """
        Disconnect from the off position
        """
        print "Start disconnecting off"
        self.disconnect(self, self.Ob)
        self.disconnect(self.Oe,self)
        self.disconnect(self.h,self.A)
        self.disconnect(self.A,self.nsi)
        print "Stop disconnecting off"

    def _connect_on(self):
        """
        Connect to the on position
        """
        print "Start connecting on"
        self.connect(self, self.A)
        self.connect(self.A,self)
        self.connect(self.h,self.Ob)
        self.connect(self.Oe,self.nsi)
        print "Stop connecting on"

    def _connect_off(self):
        """
        Connect to the off position
        """
        print "Start connecting off"
        self.connect(self, self.Ob)
        self.connect(self.Oe,self)
        self.connect(self.h,self.A)
        self.connect(self.A,self.nsi)
        print "Stop connecting off"


    def set_onoff(self, onoff):
        """
        Retsructure block
        """
        if self.onoff != onoff:
            print "Starting restructuring from ", self.onoff, " to ", onoff
            #print "Locking..."
            #self.lock()
            #self.stop()
            #self.wait()
            #print "Locked"
            if self.onoff==0:
              self._disconnect_off()
              self.onoff = 1
              self._connect_on()
            else:
              self._disconnect_on()
              self.onoff = 0
              self._connect_off()
            #print "Unlocking..."
            #self.unlock()
            #self.start()
            #print "Unlocked"
            print "Ending restructuring from ", 1-onoff, " to ", onoff

