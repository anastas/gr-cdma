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


#ifndef INCLUDED_CDMA_SWITCHED_PEAK_DETECTOR_FB_H
#define INCLUDED_CDMA_SWITCHED_PEAK_DETECTOR_FB_H

#include <cdma/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace cdma {

    /*!
     * \brief <+description of block+>
     * \ingroup cdma
     *
     */
    class CDMA_API switched_peak_detector_fb : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<switched_peak_detector_fb> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of cdma::switched_peak_detector_fb.
       *
       * To avoid accidental use of raw pointers, cdma::switched_peak_detector_fb's
       * constructor is in a private implementation
       * class. cdma::switched_peak_detector_fb::make is the public interface for
       * creating new instances.
       */
      static sptr make(float threshold_factor_rise = 0.25,
                       float threshold_factor_fall = 0.40,
                       int look_ahead = 10,
                       float alpha = 0.001,
                       int on = 1);

      virtual void set_threshold_factor_rise(float thr) = 0;
      virtual void set_threshold_factor_fall(float thr) = 0;
      virtual void set_look_ahead(int look) = 0;
      virtual void set_alpha(float alpha) = 0;
      virtual void set_on(int on) = 0;
      virtual float threshold_factor_rise() = 0;
      virtual float threshold_factor_fall() = 0;
      virtual int look_ahead() = 0;
      virtual float alpha() = 0;
      virtual int on() = 0;
    };


  } // namespace cdma
} // namespace gr

#endif /* INCLUDED_CDMA_SWITCHED_PEAK_DETECTOR_FB_H */

