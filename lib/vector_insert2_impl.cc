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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "vector_insert2_impl.h"

namespace gr {
  namespace cdma {

    vector_insert2::sptr
    vector_insert2::make(const std::vector< gr_complex > data, int periodicity, int offset)
    {
      return gnuradio::get_initial_sptr
        (new vector_insert2_impl(data, periodicity, offset));
    }

    /*
     * The private constructor
     */
    vector_insert2_impl::vector_insert2_impl(const std::vector< gr_complex > data, int periodicity, int offset)
      : gr::block("vector_insert2",
              gr::io_signature::make(1, 1, sizeof (gr_complex)),
              gr::io_signature::make(1, 1, sizeof (gr_complex))),
      d_data(data),
      d_offset(offset),
      d_periodicity(periodicity)
    {
      assert(offset >=0);
      assert(offset <= periodicity);
      vector_insert2_impl::set_output_multiple( periodicity + data.size() );
    }

    /*
     * Our virtual destructor.
     */
    vector_insert2_impl::~vector_insert2_impl()
    {
    }

    void
    vector_insert2_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = (noutput_items / (d_periodicity + d_data.size()) ) * d_periodicity;
    }

    int
    vector_insert2_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        const gr_complex *in = (const gr_complex *) input_items[0];
        gr_complex *out = (gr_complex *) output_items[0];

        int p_out=d_periodicity + d_data.size();
        assert(noutput_items%p_out==0);


        // Do <+signal processing+>
        int k=noutput_items/p_out;
        for (int i=0;i<k;i++) {
          //printf("nout=%d  i=%d, out of k=%d\n",noutput_items,i,k);
          memcpy(out+i*p_out,in+i*d_periodicity,d_offset*sizeof(gr_complex));
          memcpy(out+i*p_out+d_offset,&d_data[0],d_data.size()*sizeof(gr_complex));
          memcpy(out+i*p_out+d_offset+d_data.size(),in+i*d_periodicity+d_offset,(d_periodicity-d_offset)*sizeof(gr_complex));
        }


        // Tell runtime system how many input items we consumed on
        // each input stream.
        consume_each ((noutput_items/p_out)*d_periodicity);

        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace cdma */
} /* namespace gr */

