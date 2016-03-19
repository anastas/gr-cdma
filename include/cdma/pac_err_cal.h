/* -*- c++ -*- */
/* 
 * Copyright 2016 <+YOU OR YOUR COMPANY+>.
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


#ifndef INCLUDED_CDMA_PAC_ERR_CAL_H
#define INCLUDED_CDMA_PAC_ERR_CAL_H

#include <cdma/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace cdma {

    /*!
     * \brief <+description of block+>
     * \ingroup cdma
     *
     */
    class CDMA_API pac_err_cal : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<pac_err_cal> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of cdma::pac_err_cal.
       *
       * To avoid accidental use of raw pointers, cdma::pac_err_cal's
       * constructor is in a private implementation
       * class. cdma::pac_err_cal::make is the public interface for
       * creating new instances.
       */
      static sptr make(int winsize, int cycsize);

      virtual void set_winsize(int k) = 0;
      virtual void set_cycsize(int t) = 0;

    };

  } // namespace cdma
} // namespace gr

#endif /* INCLUDED_CDMA_PAC_ERR_CAL_H */

