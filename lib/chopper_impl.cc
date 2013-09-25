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
#include "chopper_impl.h"
#include <stdio.h>

namespace gr {
  namespace cdma {

    chopper::sptr
    chopper::make(int length)
    {
      return gnuradio::get_initial_sptr
        (new chopper_impl(length));
    }

    /*
     * The private constructor
     */
    chopper_impl::chopper_impl(int length)
      : gr::block("chopper",
                      gr::io_signature::make2(2, 2, sizeof (gr_complex),sizeof (char)),
                      gr::io_signature::make(1, 1, sizeof (gr_complex))),
      d_length(length),
      d_remaining(0)
    {}

    /*
     * Our virtual destructor.
     */
    chopper_impl::~chopper_impl()
    {
    }

    void
    chopper_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        ninput_items_required[0] = noutput_items;
        ninput_items_required[1] = noutput_items;
    }

    int
    chopper_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        const gr_complex *in_data = (const gr_complex *) input_items[0];
        const char *in_flag = (const char *) input_items[1];
        gr_complex *out = (gr_complex *) output_items[0];
        bool found;
        int i,ni;

        ni=std::min(ninput_items[0],ninput_items[1]);


        // Do <+signal processing+>
        if(d_remaining==0) {
          found=false;
          for(i=0;i<ni;i++) {
            if (in_flag[i]!=0) {
              found=true;
              break;
            }
          }
          if(found==true) {
            //printf("Found flag at i=%d\n",i);
            int n=std::min(d_length,ni-i);
            n=std::min(n,noutput_items);
            memcpy(out,in_data+i,n*sizeof(gr_complex));
            consume_each (i+n);
            d_remaining=d_length-n;
            //printf("copied=%d, consumed=%d\n",n,i+n);
            return n;
          }
          else { // found==false
            //printf("Did not find flag \n");
            consume_each (ni);
            return 0;
          }
        }
        else { //d_remaining >0
          // copy as many items as you can to the output: min(ni,nout,d_remaining)
          int n=std::min(d_remaining,ni);
          n=std::min(n,noutput_items);
          //printf("n=%d\n",n);
          memcpy(out,in_data,n*sizeof(gr_complex));
          consume_each (n);
          d_remaining-=n;
          //printf("copied=%d, consumed=%d\n",n,n);
          return n;
        }

        printf("We should never get here\n");
    }

  } /* namespace cdma */
} /* namespace gr */

