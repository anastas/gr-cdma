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

#ifndef INCLUDED_CDMA_AMP_VAR_EST_IMPL_H
#define INCLUDED_CDMA_AMP_VAR_EST_IMPL_H

#include <cdma/amp_var_est.h>

namespace gr {
  namespace cdma {

    class amp_var_est_impl : public amp_var_est
    {
     private:
//-------------------------CODE HERE------------------------------
      float d_alpha;
      float pre0;//previous output of filter 0
      float pre1;//previous output of filter 1
//----------------------------------------------------------------

     public:
//-------------------------CODE HERE------------------------------
      float alpha() const { return d_alpha; }
      void set_alpha(float alpha) {d_alpha = alpha;}

      amp_var_est_impl(float alpha);
//----------------------------------------------------------------
      ~amp_var_est_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace cdma
} // namespace gr

#endif /* INCLUDED_CDMA_AMP_VAR_EST_IMPL_H */

