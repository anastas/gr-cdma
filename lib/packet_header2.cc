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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <string.h>
#include <cdma/packet_header2.h>

namespace gr {
  namespace cdma {

    packet_header2::sptr
    packet_header2::make(
		    long header_len,
		    const std::string &len_tag_key,
		    const std::string &num_tag_key,
		    int bits_per_byte,
                    int tcm_type,
	            const std::string &tcm_tag_key)
    {
      return packet_header2::sptr(new packet_header2(header_len, len_tag_key, num_tag_key, bits_per_byte,tcm_type, tcm_tag_key));
    }

    packet_header2::packet_header2(
	            long header_len,
		    const std::string &len_tag_key,
		    const std::string &num_tag_key,
		    int bits_per_byte,
                    int tcm_type,
	            const std::string &tcm_tag_key
    ): gr::digital::packet_header_default(
          header_len,
	  len_tag_key,
	  num_tag_key,
	  bits_per_byte),
	d_tcm_type(tcm_type),
        d_tcm_tag_key(pmt::string_to_symbol(tcm_tag_key))
	{

	}


    packet_header2::~packet_header2()
    {
    }

    bool packet_header2::header_formatter(
	long packet_len,
        unsigned char *out,
	const std::vector<tag_t> &tags
    )
    {
      packet_len &= 0x0FFF;
      d_crc_impl.reset();
      d_crc_impl.process_bytes((void const *) &packet_len, 2);
      d_crc_impl.process_bytes((void const *) &d_tcm_type, 4);
      d_crc_impl.process_bytes((void const *) &d_header_number, 2);
      unsigned char crc = d_crc_impl();

      memset(out, 0x00, d_header_len);
      int k = 0; // Position in out
      for (int i = 0; i < 12 && k < d_header_len; i += d_bits_per_byte, k++) {
	out[k] = (unsigned char) ((packet_len >> i) & d_mask);
      }
      for (int i = 0; i < 4 && k < d_header_len; i += d_bits_per_byte, k++) {
	out[k] = (unsigned char) ((d_tcm_type >> i) & d_mask);
      }
      for (int i = 0; i < 12 && k < d_header_len; i += d_bits_per_byte, k++) {
	out[k] = (unsigned char) ((d_header_number >> i) & d_mask);
      }
      for (int i = 0; i < 8 && k < d_header_len; i += d_bits_per_byte, k++) {
	out[k] = (unsigned char) ((crc >> i) & d_mask);
      }
      d_header_number++;
      d_header_number &= 0x0FFF;

      return true;
    }

    bool packet_header2::header_parser(
	const unsigned char *in,
	std::vector<tag_t> &tags)
    {
      unsigned header_len = 0;
      int tcm_type = 0;
      unsigned header_num = 0;
      tag_t tag;

      int k = 0; // Position in "in"
      for (int i = 0; i < 12 && k < d_header_len; i += d_bits_per_byte, k++) {
	header_len |= (((int) in[k]) & d_mask) << i;
      }
      tag.key = d_len_tag_key;
      tag.value = pmt::from_long(header_len);
      tags.push_back(tag);
      if (k >= d_header_len) {
	return true;
      }
      for (int i = 0; i < 4 && k < d_header_len; i += d_bits_per_byte, k++) {
	tcm_type |= (((int) in[k]) & d_mask) << i;
      }
      tag.key = d_tcm_tag_key;
      tag.value = pmt::from_long(tcm_type);
      tags.push_back(tag);

      if (d_num_tag_key == pmt::PMT_NIL) {
	k += 12;
      } else {
	for (int i = 0; i < 12 && k < d_header_len; i += d_bits_per_byte, k++) {
	  header_num |= (((int) in[k]) & d_mask) << i;
	}
	tag.key = d_num_tag_key;
	tag.value = pmt::from_long(header_num);
	tags.push_back(tag);
      }
      if (k >= d_header_len) {
	return true;
      }

      d_crc_impl.reset();
      d_crc_impl.process_bytes((void const *) &header_len, 2);
      d_crc_impl.process_bytes((void const *) &tcm_type, 4);
      d_crc_impl.process_bytes((void const *) &header_num, 2);
      unsigned char crc_calcd = d_crc_impl();
      for (int i = 0; i < 8 && k < d_header_len; i += d_bits_per_byte, k++) {
	  if ( (((int) in[k]) & d_mask) != (((int) crc_calcd >> i) & d_mask) ) {
	    return false;
	  }
      }

      return true;
    }

  } /* namespace cdma */
} /* namespace gr */

