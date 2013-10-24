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
    chopper::make(int lengtho, int lengthi, size_t itemsize)
    {
      return gnuradio::get_initial_sptr
        (new chopper_impl(lengtho, lengthi,itemsize));
    }

    /*
     * The private constructor
     */
    chopper_impl::chopper_impl(int lengtho, int lengthi, size_t itemsize)
      : gr::block("chopper",
                      gr::io_signature::make2(2, 2, itemsize*sizeof(char),sizeof (char)),
                      gr::io_signature::make(1, 1, itemsize*sizeof(char))),
      d_itemsize(itemsize),
      d_lengtho(lengtho),
      d_lengthi(lengthi),
      d_found(false)
    {
      assert(d_lengtho>=d_lengthi);
      set_output_multiple(d_lengtho);
    }

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
        const char *in_data = (const char *) input_items[0];
        const char *in_flag = (const char *) input_items[1];
        char *out = (char *) output_items[0];
        bool found;
        int i,ni,no,n;

        ni=std::min(ninput_items[0],ninput_items[1]);
        //no=noutput_items;
        //n=std::min(ni,no); 
        //printf("ni=%d, no=%d, n=%d\n",ni,no,n);

        // Do <+signal processing+>
        if(d_found==false) {
          for(i=0;i<ni;i++) {
            if (in_flag[i]!=0) {
              d_found=true;
              consume_each(i);
              //printf("Found flag at i=%d,     consumed=%d\n",i,i);
              return 0;  
            }
          }
        }

        // if you get here a flag was found

        memcpy(out,in_data,d_itemsize*d_lengtho);
        //printf("Copying No  and consuming Ni\n");
        consume_each(d_lengthi);
        d_found=false;
        return d_lengtho;

    } //work

  } /* namespace cdma */
} /* namespace gr */

