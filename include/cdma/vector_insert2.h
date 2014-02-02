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


#ifndef INCLUDED_CDMA_VECTOR_INSERT2_H
#define INCLUDED_CDMA_VECTOR_INSERT2_H

#include <cdma/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace cdma {

    /*!
     * \brief <+description of block+>
     * \ingroup cdma
     *
     */
    class CDMA_API vector_insert2 : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<vector_insert2> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of cdma::vector_insert2.
       *
       * To avoid accidental use of raw pointers, cdma::vector_insert2's
       * constructor is in a private implementation
       * class. cdma::vector_insert2::make is the public interface for
       * creating new instances.
       */
      static sptr make(const std::vector< gr_complex > data, int periodicity, int offset);
    };

  } // namespace cdma
} // namespace gr

#endif /* INCLUDED_CDMA_VECTOR_INSERT2_H */

