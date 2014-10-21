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

#ifndef INCLUDED_CDMA_PACKET_HEADER2_H
#define INCLUDED_CDMA_PACKET_HEADER2_H

#include <gnuradio/tags.h>
#include <cdma/api.h>
//#include <cdma/packet_header.h>
#include <gnuradio/digital/packet_header_default.h>
//#include <boost/enable_shared_from_this.hpp>
//#include <boost/crc.hpp>

namespace gr {
  namespace cdma {

    /*!
     * \brief Default header formatter for digital packet transmission.
     * \ingroup packet_operators_blk
     *
     * \details
     * For bursty/packetized digital transmission, packets are usually prepended
     * with a packet header, containing the number of bytes etc.
     * This class is not a block, but a tool to create these packet header.
     *
     * This is a default packet header (see header_formatter()) for a description
     * on the header format). To create other header, derive packet header creator
     * classes from this function.
     *
     * gr::digital::packet_headergenerator_bb uses header generators derived from
     * this class to create packet headers from data streams.
     */
    class CDMA_API packet_header2 : virtual public gr::digital::packet_header_default
    {
     public:
      typedef boost::shared_ptr<packet_header2> sptr;

      packet_header2(
		      long header_len,
		      const std::string &len_tag_key="packet_len",
		      const std::string &num_tag_key="packet_num",
		      int bits_per_byte=1,
                      int tcm_type=1,
		      const std::string &tcm_type_key="tcm_type");
      ~packet_header2();

      void set_tcm_type(int tcm_type){d_tcm_type = tcm_type; };

      //pmt::pmt_t len_tag_key() { return d_len_tag_key; };

      /*!
       * \brief Encodes the header information in the given tags into bits and places them into \p out
       *
       * Uses the following header format:
       * Bits 0-11: The packet length (what was stored in the tag with key \p len_tag_key)
       * Bits 12-15: The trellis coded modulation type
       * Bits 16-27: The header number (counts up everytime this function is called)
       * Bit 28-35: 8-Bit CRC
       * All other bits: Are set to zero
       *
       * If the header length is smaller than 36, bits are simply left out. For this
       * reason, they always start with the LSB.
       *
       * However, it is recommended to stay above 36 Bits, in order to have a working
       * CRC.
       */
      bool header_formatter(
	  long packet_len,
	  unsigned char *out,
	  const std::vector<tag_t> &tags=std::vector<tag_t>()
      );

      /*!
       * \brief Inverse function to header_formatter().
       *
       * Reads the bit stream in \p header and writes a corresponding tag into \p tags.
       */
      bool header_parser(
	const unsigned char *header,
	std::vector<tag_t> &tags);

      static sptr make(
		      long header_len,
		      const std::string &len_tag_key="packet_len",
		      const std::string &num_tag_key="packet_num",
		      int bits_per_byte=1,
                      int tcm_type=1,
		      const std::string &tcm_tag_key="tcm_type");

    protected:
      pmt::pmt_t d_tcm_tag_key;
      int d_tcm_type;

    };

  } // namespace cdma
} // namespace gr

#endif /* INCLUDED_CDMA_PACKET_HEADER2_H */

