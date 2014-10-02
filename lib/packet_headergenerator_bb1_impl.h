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

#ifndef INCLUDED_CDMA_PACKET_HEADERGENERATOR_BB1_IMPL_H
#define INCLUDED_CDMA_PACKET_HEADERGENERATOR_BB1_IMPL_H

#include <cdma/packet_headergenerator_bb1.h>

namespace gr {
  namespace cdma {

    class packet_headergenerator_bb1_impl : public packet_headergenerator_bb1
    {
     private:
      gr::cdma::packet_header::sptr d_formatter;

     public:
      packet_headergenerator_bb1_impl(
	  const packet_header::sptr &header_formatter,
	  const std::string &len_tag_key
      );
      ~packet_headergenerator_bb1_impl();

      void set_header_formatter(const packet_header::sptr &header_formatter){d_formatter=header_formatter;}
      void remove_length_tags(const std::vector<std::vector<tag_t> > &tags) {};
      int calculate_output_stream_length(const gr_vector_int &ninput_items) { return d_formatter->header_len(); };

      int work(int noutput_items,
	  gr_vector_int &ninput_items,
	  gr_vector_const_void_star &input_items,
	  gr_vector_void_star &output_items);
    };

  } // namespace cdma
} // namespace gr

#endif /* INCLUDED_CDMA_PACKET_HEADERGENERATOR_BB1_IMPL_H */

