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


#ifndef INCLUDED_CDMA_FLAG_GEN_H
#define INCLUDED_CDMA_FLAG_GEN_H

#include <cdma/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace cdma {

    /*!
     * \brief <+description of block+>
     * \ingroup cdma
     *
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
       */
      static sptr make(int period, int onoff);
      virtual void set_onoff (int onoff) = 0;
    };

  } // namespace cdma
} // namespace gr

#endif /* INCLUDED_CDMA_FLAG_GEN_H */

