/* -*- c++ -*- */
/* 
 * Copyright 2013 <+YOU OR YOUR COMPANY+>.
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


#ifndef INCLUDED_CDMA_FLAG_GEN_H
#define INCLUDED_CDMA_FLAG_GEN_H

#include <cdma/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace cdma {

    /*!
     * \brief This block either passes through the input stream (assumed to be zeros or ones) when its internal state is acq=1, or it outputs a stream of zeros with periodic ones (with given period) when its internal state is acq=0.
     * \ingroup cdma
     *
     * \details
     * The purpose of this block is to be used right after the timing/frequency acquisition block.
     * The timing/frequency acquisition block outputs a stream of 0s and 1s, with 1s indicating the 
     * begining of a cdma frame.\n
     * When the system is in acquisition mode (acq=1), the flag_gen block just passes through its 
     * input stream, which comes from the timing/frequency acquisition block.\n
     * When the system is in tracking mode (acq=0), the timing/frequency acquisition block is 
     * not supposed to produce any meaningful output flags. 
     * In this case, the flag_gen block produces periodical flags (with given period equal 
     * to the frame length) starting from the last flag produced by the timing/frequency 
     * acquisition block, in order to provide timing information for the remaining of the system.\n
     *
     * For example, when period is 4 the input and output streams will look like:\n
     * acq:------>111111000000000...\n
     * input:---->010100000000000...\n
     * output:-->010100010001000...\n
     * where the first 1 in the input and output is for example due to a false acquisition.
     */
    class CDMA_API flag_gen : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<flag_gen> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of cdma::flag_gen.
       *
       * To avoid accidental use of raw pointers, cdma::flag_gen's
       * constructor is in a private implementation
       * class. cdma::flag_gen::make is the public interface for
       * creating new instances.
       *
       * \param acq the mode selector. Takes values {0, 1}. 
       * \param period the period of output flags when acq=0.  
       */
      static sptr make(int period, int acq);
      virtual void set_acq (int acq) = 0;
    };

  } // namespace cdma
} // namespace gr

#endif /* INCLUDED_CDMA_FLAG_GEN_H */

