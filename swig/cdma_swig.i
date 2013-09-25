/* -*- c++ -*- */

#define CDMA_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "cdma_swig_doc.i"

%{
#include "cdma/chopper.h"
#include "cdma/vector_insert2.h"
%}


%include "cdma/chopper.h"
GR_SWIG_BLOCK_MAGIC2(cdma, chopper);

%include "cdma/vector_insert2.h"
GR_SWIG_BLOCK_MAGIC2(cdma, vector_insert2);
