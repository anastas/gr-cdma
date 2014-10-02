/* -*- c++ -*- */
/* Copyright 2012 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_CDMA_PACKET_HEADERPARSER_B2_IMPL_H
#define INCLUDED_CDMA_PACKET_HEADERPARSER_B2_IMPL_H

#include <cdma/packet_headerparser_b2.h>

namespace gr {
  namespace cdma {

    class packet_headerparser_b2_impl : public packet_headerparser_b2
    {
    private:
      packet_header2::sptr d_header_formatter;

    public:
      packet_headerparser_b2_impl(const gr::cdma::packet_header2::sptr &header_formatter);
      ~packet_headerparser_b2_impl();

      int work(int noutput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);
    };

  } // namespace cdma
} // namespace gr

#endif /* INCLUDED_CDMA_PACKET_HEADERPARSER_B1_IMPL_H */

