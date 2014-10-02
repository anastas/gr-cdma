# Copyright 2011 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
install(FILES
    cdma_chopper.xml
    cdma_vector_insert2.xml
    cdma_freq_timing_estimator.xml
    cdma_message_probe.xml
    cdma_packet_headergenerator_bb1.xml
    cdma_packet_headergenerator_bb1_default.xml
    cdma_packet_headerparser_b2.xml
    cdma_packet_headerparser_b2_default.xml
    #cdma_myselector.xml
    cdma_flag_gen.xml
    cdma_kronecker_filter.xml
    cdma_freq_timing_estimator1.xml DESTINATION share/gnuradio/grc/blocks
)
