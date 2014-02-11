/* -*- c++ -*- */
/* 
 * Copyright 2013 Achilleas Anastasopoulos, Zhe Feng.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */


#ifndef INCLUDED_CDMA_CHOPPER_H
#define INCLUDED_CDMA_CHOPPER_H

#include <cdma/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace cdma {

    /*!
     * \brief Chop the input data stream according to the flags in the input control stream.
     * \ingroup cdma
     *
     * \details
     * When flag is detected  in the control stream, the chopper start to chop. 
     * The chopper outputs a copy of length_out items from the input stream to the output stream per chop.\n
     * The chopper consumes length_in items from the input and control streams.\n
     * Typically the flags are periodic and length_out>=length_in. Therefore, there exist three cases.\n
     * Case 1: period <= length_in <= length_out \n
     * For example, with length_in=4, length_out=5, period=3, the input and output streams will look like \n
     * input:----->abcdefghijklmn...\n
     * flags:----->10010010010010... (period=3)\n
     * outputs:-->abcdeghijkmn...\n
     * \n
     * Case 2: length_in <= period <= length_out \n
     * For example, with length_in=4, length_out=6, period=5, the input and output streams will look like \n
     * input:----->abcdefghijklmn...\n
     * flags:----->100001000010000... (period=5)\n
     * outputs:-->abcdeffghijkklmnop...\n
     * \n
     * Case 3: length_in <=length_out <= period \n
     * For example, with length_in=4, length_out=6, period=7, the input and output streams will look like \n
     * input:----->abcdefghijklmnopqrst...\n
     * flags:----->100000010000001000000...(periold=7) \n
     * outputs:-->abcdefhijklmonqrst...\n
     *
     */
    class CDMA_API chopper : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<chopper> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of cdma::chopper.
       *
       * To avoid accidental use of raw pointers, cdma::chopper's
       * constructor is in a private implementation
       * class. cdma::chopper::make is the public interface for
       * creating new instances.
       *
       * \param vector_length size of input item in data stream
       * \param length_in number of items chopper consumes per chop.
       * \param length_out number of items chopper outputs per chop. Typically length out>=length in.
       */

      static sptr make(int length_out, int length_in, size_t vector_length);
    };

  } // namespace cdma
} // namespace gr

#endif /* INCLUDED_CDMA_CHOPPER_H */

