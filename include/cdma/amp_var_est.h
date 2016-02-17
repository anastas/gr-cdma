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


#ifndef INCLUDED_CDMA_AMP_VAR_EST_H
#define INCLUDED_CDMA_AMP_VAR_EST_H

#include <cdma/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace cdma {

    /*!
     * \brief Assumes as input a constant complex signal with complex noise s[i]=(A+j B) + (wr[i]+j wi[i])
              Estimates the signal power on the real part A^2 and real noise variance sigma^2.
     * \ingroup cdma
     *
     * \details
     * First convert the input stream from complex type to real type, so r[i]=A + wr[i]. \n
     * Then split the stream into two branches: \n
	 * 1) Pass the first branch through a single-pole IIR filter (averaging), square the result,
     *    and obtain an estimate of the signal power A^2. \n
	 * 2) Square the second branch, pass the result through a single-pole IIR filter,
     *    subtract the estimated signal power and obtain an estimate of the noise power sigma^2.\n
	 * \n
	 * For the IIR filter, the parameter alpha controls the averaging length. See equation below: \n
	 * y[i] = (1-alpha)*y[i-1] + alpha*x[i]. \n
	 * \n
     */
    class CDMA_API amp_var_est : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<amp_var_est> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of cdma::amp_var_est.
       *
       * To avoid accidental use of raw pointers, cdma::amp_var_est's
       * constructor is in a private implementation
       * class. cdma::amp_var_est::make is the public interface for
       * creating new instances.
       */
//-------------------------CODE HERE------------------------------
      static sptr make(float alpha);
			
      virtual float alpha() const = 0;

      virtual void set_alpha(float k) = 0;
//----------------------------------------------------------------
    };

  } // namespace cdma
} // namespace gr

#endif /* INCLUDED_CDMA_AMP_VAR_EST_H */
