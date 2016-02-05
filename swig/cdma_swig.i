/* -*- c++ -*- */

#define CDMA_API
#define DIGITAL_API
%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "cdma_swig_doc.i"

%{
#include "cdma/chopper.h"
#include "cdma/vector_insert2.h"
#include "cdma/flag_gen.h"
#include "cdma/packet_header2.h"
#include "cdma/packet_headerparser_b2.h"
#include "gnuradio/digital/packet_header_default.h"
#include "cdma/amp_var_est.h"

%}
%include "gnuradio/digital/packet_header_default.h"
%include "cdma/packet_header2.h"

%include "cdma/packet_headerparser_b2.h"
GR_SWIG_BLOCK_MAGIC2(cdma, packet_headerparser_b2);

%include "cdma/chopper.h"
GR_SWIG_BLOCK_MAGIC2(cdma, chopper);

%include "cdma/vector_insert2.h"
GR_SWIG_BLOCK_MAGIC2(cdma, vector_insert2);


%include "cdma/flag_gen.h"
GR_SWIG_BLOCK_MAGIC2(cdma, flag_gen);

// Properly package up non-block objects
%include "packet_header.i"
%include "cdma/amp_var_est.h"
GR_SWIG_BLOCK_MAGIC2(cdma, amp_var_est);
