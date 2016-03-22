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
      unsigned long d_winsize;        // size of the block window
      unsigned long d_cycsize;        // size of a complete cycle, say 4096

      unsigned long d_count_pktsent;  // number of packets sent from the tx
      unsigned long d_count_errs;     // number of error packets in the current window
      unsigned long d_curnum;         // number of packets received in the current window
      unsigned long d_prev;           // the index of the last packet in service
      float d_erate;                  // error rate result
      std::string d_pkt_num_tag;      // tag name for the packet index

      void print(pmt::pmt_t msg);
      void errCal(pmt::pmt_t msg);

     public:
      pac_err_cal_impl(unsigned long winsize, unsigned long cycsize, std::string pkt_num_tag);
      ~pac_err_cal_impl();

      void set_winsize(unsigned long winsize) {d_winsize = winsize;}
      void set_cycsize(unsigned long cycsize) {d_cycsize = cycsize;}
      void set_pkt_num_tag(std::string pkt_num_tag) {d_pkt_num_tag = pkt_num_tag;}
    };

  } // namespace cdma
} // namespace gr

#endif /* INCLUDED_CDMA_PAC_ERR_CAL_IMPL_H */

