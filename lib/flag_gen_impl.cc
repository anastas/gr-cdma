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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "flag_gen_impl.h"
#include <stdio.h>

namespace gr {
  namespace cdma {

    flag_gen::sptr
    flag_gen::make(int period, int onoff)
    {
      return gnuradio::get_initial_sptr
        (new flag_gen_impl(period, onoff));
    }

    /*
     * The private constructor
     */
    flag_gen_impl::flag_gen_impl(int period, int onoff)
      : gr::sync_block("flag_gen",
              gr::io_signature::make(1,1, sizeof(char)),
              gr::io_signature::make(1,1, sizeof(char))),
      d_period(period),
      d_onoff(onoff),
      d_counter(period)
    {}

    /*
     * Our virtual destructor.
     */
    flag_gen_impl::~flag_gen_impl()
    {
    }

    void flag_gen_impl::set_onoff(int onoff)
    {
      d_onoff=onoff;
    }


    int
    flag_gen_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        const char *in = (const char *) input_items[0];
        char *out = (char *) output_items[0];

        // Do <+signal processing+>
        for(int i=0;i<noutput_items;i++) {
          //printf("onoff=%d,     counter=%d\n",d_onoff,d_counter);
         d_counter--;

          if(d_onoff==1) { // Acquisition
            out[i]=in[i];
            if(in[i]==1) { // reset counter
              d_counter=d_period;
            }
          }
          else if (d_onoff==0) { // tracking
            if(d_counter==0) {
              out[i]=1;
            }
            else {
              out[i]=0;
            }
          }
          else {
            printf("Should not be here: onoff parameter != 0 or 1\n");
          } 

          if (d_counter==0) 
            d_counter=d_period;
        }

        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace cdma */
} /* namespace gr */

