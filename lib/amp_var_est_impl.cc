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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "amp_var_est_impl.h"
//-------------------------CODE HERE------------------------------
//#include <volk/volk.h>
//#include <gnuradio/filter/iir_filter.h>
//#include <gnuradio/filter/api.h>
#include <gnuradio/gr_complex.h>
//----------------------------------------------------------------

namespace gr {
  namespace cdma {

    amp_var_est::sptr
    amp_var_est::make(float alpha)
    {
      return gnuradio::get_initial_sptr
        (new amp_var_est_impl(alpha));
    }

    /*
     * The private constructor
     */
//-------------------------CODE HERE------------------------------
    amp_var_est_impl::amp_var_est_impl(float alpha)
      : gr::sync_block("amp_var_est",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make2(2, 2, sizeof(float),sizeof(float)))
    {
			d_alpha = alpha;
			pre0 = 0;
			pre1 = 0;
		}
//----------------------------------------------------------------
    /*
     * Our virtual destructor.
     */
    amp_var_est_impl::~amp_var_est_impl()
    {
    }

    int
    amp_var_est_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
//-------------------------CODE HERE------------------------------
      const gr_complex *in = (const gr_complex *) input_items[0];
      float *out0 = (float *) output_items[0];//signal amplitude
      float *out1 = (float *) output_items[1];//noise vaiance
			int no = noutput_items;

      // Do <+signal processing+>

			for(int k=0;k<no;k++) {
        float x=in[k].real();
			  float tmp=x*x;
			  pre0 = d_alpha*tmp + (1-d_alpha)*pre0;

        pre1=d_alpha*x + (1-d_alpha)*pre1;
			  tmp = pre1*pre1;

				out0[k] = tmp;
			  out1[k] = pre0 - tmp;
			}

      // Tell runtime system how many output items we produced.
      return noutput_items;
//----------------------------------------------------------------
    }

		void
		amp_var_est_impl::setup_rpc()
		{
			#ifdef GR_CTRLPORT
      add_rpc_variable(
				rpcbasic_sptr(new rpcbasic_register_get<amp_var_est, float>(
		alias(), "alpha",
	  &amp_var_est::alpha,
	  pmt::mp(0.0f), pmt::mp(1.0f), pmt::mp(0.0f),
	  "", "Get value of alpha", RPC_PRIVLVL_MIN, DISPTIME | DISPOPTSTRIP)));

      add_rpc_variable(
        rpcbasic_sptr(new rpcbasic_register_set<amp_var_est, float>(
	  alias(), "alpha",
	  &amp_var_est::set_alpha,
	  pmt::mp(0.0f), pmt::mp(1.0f), pmt::mp(0.0f),
	  "", "Set value of alpha", RPC_PRIVLVL_MIN, DISPNULL)));
		#endif /* GR_CTRLPORT */
		}

  } /* namespace cdma */
} /* namespace gr */

