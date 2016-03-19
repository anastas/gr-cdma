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
#include "pac_err_cal_impl.h"
#include <cstdio>
#include <iostream>
//#include <stdio>


namespace gr {
  namespace cdma {

    pac_err_cal::sptr
    pac_err_cal::make(int winsize, int cycsize)
    {
      return gnuradio::get_initial_sptr
        (new pac_err_cal_impl(winsize, cycsize));
    }

    /*
     * The private constructor
     */
    pac_err_cal_impl::pac_err_cal_impl(int winsize, int cycsize)
      : gr::block("pac_err_cal",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(0, 0, 0))
    {
      d_winsize = winsize;
      d_cycsize = cycsize;
      d_count_errs = 0;
      d_count_pktsent = 0;
      d_curnum = 0;

      d_first = 0;
      d_prev = -1;
      d_erate = 0;

      message_port_register_in(pmt::mp("print"));
      set_msg_handler(pmt::mp("print"), boost::bind(&pac_err_cal_impl::print, this, _1));

      message_port_register_in(pmt::mp("errCal"));
      set_msg_handler(pmt::mp("errCal"), boost::bind(&pac_err_cal_impl::errCal, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    pac_err_cal_impl::~pac_err_cal_impl()
    {
    }


    void
    pac_err_cal_impl::print(pmt::pmt_t msg)
    {
      std::cout << "******* MESSAGE DEBUG PRINT ********\n";
      pmt::print(msg);
      //std::cout << pmt::write_string(msg) << '\n';
      std::cout << "************************************\n";
    }

    void
    pac_err_cal_impl::errCal(pmt::pmt_t msg)
    {
      
      pmt::pmt_t key0 = pmt::intern("cdma_packet_num");
      if (pmt::dict_has_key (msg, key0))
      {

        pmt::pmt_t not_found;
        pmt::pmt_t val0 = pmt::dict_ref(msg,key0,not_found);
        int val = pmt::to_uint64(val0);

        d_curnum = d_curnum + 1; // # of packets stocked in the current window + 1

        //increment errs and packets sent
        if (val <= d_prev) // a new cycle starts while the window hasn't been filled up
        {
          d_count_errs = d_count_errs + d_cycsize + val - d_prev - 1;
          d_count_pktsent = d_count_pktsent + d_cycsize + val - d_prev;

        }
        else
        {
          d_count_errs = d_count_errs + val - d_prev - 1;
          d_count_pktsent = d_count_pktsent + val - d_prev;
        }

        //terminate the window
        if (d_curnum >= d_winsize)
        {
          d_erate = (float) d_count_errs / d_count_pktsent; // key calculation
          
          //std::cout << "E-RATE: " << d_erate << "\t\t E-#: " << d_count_errs << "\t\t TAIL: " << val << "\t\t HEAD: " << d_first << "\n";          
          std::cout << "E-RATE: " << d_erate << "\n";
          d_curnum = 0;
          d_count_errs = 0;
          d_count_pktsent = 0;
        }
        else if (d_curnum == 1)
        {
          d_first = val;
        }

        d_prev = val;     
      }
    }

  } /* namespace cdma */
} /* namespace gr */

