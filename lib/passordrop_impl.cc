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
#include "passordrop_impl.h"
#include <stdio.h>

namespace gr {
  namespace cdma {

    passordrop::sptr
    passordrop::make(size_t itemsize)
    {
      return gnuradio::get_initial_sptr
        (new passordrop_impl(itemsize));
    }

    /*
     * The private constructor
     */
    passordrop_impl::passordrop_impl(size_t itemsize)
      : gr::block("passordrop",
              gr::io_signature::make2(2, 2, itemsize,sizeof(char)),
              gr::io_signature::make(1, 1, itemsize)),
      d_itemsize(itemsize)
    {}

    /*
     * Our virtual destructor.
     */
    passordrop_impl::~passordrop_impl()
    {
    }

    void
    passordrop_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
        ninput_items_required[0] = noutput_items;
        ninput_items_required[1] = noutput_items;
    }

    int
    passordrop_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        const char *in = (const char *) input_items[0];
        const char *control = (const char *) input_items[1];
        char *out = (char *) output_items[0];

        // Do <+signal processing+>
        // Tell runtime system how many input items we consumed on
        // each input stream.
        int n=0;
        for(int i=0;i<noutput_items;i++) {
          //printf("control[%d]=%d\n",i,control[i]);
          if(control[i]==1) {
            memcpy(out,in+i*d_itemsize,d_itemsize);
            out += d_itemsize;
            n++;
          }
        }
        consume_each (noutput_items);

        // Tell runtime system how many output items we produced.
        //printf("nout=%d, n=%d\n",noutput_items,n);
        return n;
    }

  } /* namespace cdma */
} /* namespace gr */

