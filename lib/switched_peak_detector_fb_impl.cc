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

#include <stdio.h>

#include <gnuradio/io_signature.h>
#include "switched_peak_detector_fb_impl.h"

namespace gr {
  namespace cdma {

    switched_peak_detector_fb::sptr
    switched_peak_detector_fb::make(float threshold_factor_rise,
                                    float threshold_factor_fall,
                                    int look_ahead, 
                                    float alpha,
                                    int on)
    {
      return gnuradio::get_initial_sptr
        (new switched_peak_detector_fb_impl(threshold_factor_rise,threshold_factor_fall,look_ahead,alpha,on));
    }

    /*
     * The private constructor
     */
    switched_peak_detector_fb_impl::switched_peak_detector_fb_impl(
      float threshold_factor_rise,
      float threshold_factor_fall,
      int look_ahead, 
      float alpha,
      int on)
      : gr::sync_block("switched_peak_detector_fb",
              gr::io_signature::make(1,1, sizeof(float)),
              gr::io_signature::make(1,1, sizeof(char))),
       d_threshold_factor_rise(threshold_factor_rise),
       d_threshold_factor_fall(threshold_factor_fall),
       d_look_ahead(look_ahead), 
       //d_look_ahead(10), 
       d_avg_alpha(alpha), 
       d_on(on),
       d_avg(0), 
       d_found(0),
       d_state(0)
    {}

    /*
     * Our virtual destructor.
     */
    switched_peak_detector_fb_impl::~switched_peak_detector_fb_impl()
    {
    }

    int
    switched_peak_detector_fb_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      float *iptr = (float*)input_items[0];
      char *optr = (char*)output_items[0];

      memset(optr, 0, noutput_items*sizeof(char));
      if (d_on==0) {
        return noutput_items; 
      }

      if(d_state==0) {
        for(int i=0;i < noutput_items;i++) {
          if(iptr[i] > d_avg*d_threshold_factor_rise) {
            //printf("CROSSED THRESHOLD... %d\n", d_look_ahead);
            d_state = 1;
            set_output_multiple(d_look_ahead);
            return i;
          }
          else {
            d_avg = (d_avg_alpha)*iptr[i] + (1-d_avg_alpha)*d_avg;
          }
        }
        return noutput_items;
      }
      else { // d_state==1
        if (noutput_items<d_look_ahead) {
         printf("SOMETHING IS WRONG: noutput_items %d < look_ahead %d\n",noutput_items,d_look_ahead);
         return 0;
        }
        float peak_val = -(float)INFINITY;
        int peak_ind = 0;
        for(int i=0;i<d_look_ahead;i++) {
          if(iptr[i] > peak_val) {
            peak_val = iptr[i];
            peak_ind = i;
            d_avg = (d_avg_alpha)*iptr[i] + (1-d_avg_alpha)*d_avg;
          }
        }
        optr[peak_ind] = 1;
        d_state=0;
        set_output_multiple(1);
        return d_look_ahead;
      }

/*
      float peak_val = -(float)INFINITY;
      int peak_ind = 0;
      unsigned char state = 0;
      int i = 0;
      int threshold_index=0;

      //printf("noutput_items %d\n",noutput_items);
      while(i < noutput_items) {
        if(state == 0) {  // below threshold
          if(iptr[i] > d_avg*d_threshold_factor_rise) {
            threshold_index=i;
            state = 1;
          }
          else {
            d_avg = (d_avg_alpha)*iptr[i] + (1-d_avg_alpha)*d_avg;
            i++;
          }
        }
        else if(state == 1) {  // above threshold, have not found peak
          //printf("Entered State 1: %f  i: %d  noutput_items: %d\n", iptr[i], i, noutput_items);
          if(iptr[i] > peak_val) {
            peak_val = iptr[i];
            peak_ind = i;
            d_avg = (d_avg_alpha)*iptr[i] + (1-d_avg_alpha)*d_avg;
            i++;
          }
          else if(iptr[i] > d_avg*d_threshold_factor_fall) {
            d_avg = (d_avg_alpha)*iptr[i] + (1-d_avg_alpha)*d_avg;
            i++;
          }
          else {
            optr[peak_ind] = 1;
            state = 0;
            peak_val = -(float)INFINITY;
            //printf("Leaving  State 1: Peak: %f  Peak Ind: %d   i: %d  noutput_items: %d\n",
            //peak_val, peak_ind, i, noutput_items);
          }
        }
      }
      if(state == 0) {
        //printf("Leave in State 0, produced %d\n",noutput_items);
        return noutput_items;
      }
      else {   // only return up to current peak
        //printf("Leave in State 1, only produced %d of %d\n",peak_ind+1,noutput_items);
        //printf("Leave in State 1, only produced %d of %d\n",threshold_index,noutput_items);
        return peak_ind+1;
        //return threshold_index;
      }
*/
    }

  } /* namespace cdma */
} /* namespace gr */

