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

#ifndef INCLUDED_CDMA_PAC_ERR_CAL_IMPL_H
#define INCLUDED_CDMA_PAC_ERR_CAL_IMPL_H

#include <cdma/pac_err_cal.h>
#include <gnuradio/block.h>
#include <gnuradio/thread/thread.h>
#include <pmt/pmt.h>

namespace gr {
  namespace cdma {

    class pac_err_cal_impl : public pac_err_cal
    {
     private:
      int d_winsize;        // size of the block window
      int d_cycsize;        // size of a complete cycle, say 4096

      int d_first;          // index of the first received packet in the current window
      int d_count_pktsent;  // number of packets sent from the tx
      int d_count_errs;     // number of error packets in the current window
      int d_curnum;         // number of packets received in the current window
      int d_prev;           // the index of the last packet in service
      float d_erate;        // error rate result

      void print(pmt::pmt_t msg);
      void errCal(pmt::pmt_t msg);

     public:
      pac_err_cal_impl(int winsize, int cycsize);
      ~pac_err_cal_impl();

      void set_winsize(int winsize) {d_winsize = winsize;}
      void set_cycsize(int cycsize) {d_cycsize = cycsize;}

      /*
      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
      //*/
    };

  } // namespace cdma
} // namespace gr

#endif /* INCLUDED_CDMA_PAC_ERR_CAL_IMPL_H */

