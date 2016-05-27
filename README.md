gr-cdma
=======

This is the gr-cdma out-of-tree package.
To use the cdma blocks, the Python namespaces
is in 'cdma', which is imported as:

    import cdma

See the Doxygen documentation for details about the blocks available
in this package. A quick listing of the details can be found in Python
after importing by using:

    help(cdma)

For the impatient:

1) Download gr-cdma from github
> git clone https://github.com/anastas/gr-cdma.git

2) Edit the file gr-cdma/python/cdma_parameters.py
and set the prefix variable with your gr-cdma trunk directory.

Note: this is your git directory prefix not the installation prefix!

prefix="YOUR_PREFIX_HERE/gr-cdma"  # put the prefix of your gr-cdma trunk

2) Build the package
> mkdir build_cdma

> cd build_cdma

> cmake -DENABLE_DOXYGEN=ON "PATH TO YOUR gr-cdma TRUNK" 

> make

> sudo make install

> sudo ldconfig


3) compile hierarchical blocks and play with built in apps
> cd gr-cdma/apps

> gnuradio-companion &

In the gnuradio-companion environment

-- For each of the blocks listed below, open them into gnuradio-companion and compile each one (using the button in GRC that looks like a sphere and a pyramid with an arrow between them) and then reload each time (using the button that looks like a circular arrow)

"cdma_tx_hier.grc", 

"chopper_correlator.grc", 

"cdma_rx_hier.grc", 

-- Reload all blocks in grc

-- Load the application "cdma_txrx.grc" and have fun

Experiment with manual acq/tra, auto acq/tra, changing freq and timing offset, SNR, etc

-- Once you understand this you can also build the adaptive modulation/coding version of this app

-- For each of the blocks listed below, open them into gnuradio-companion and compile each one (using the button in GRC that looks like a sphere and a pyramid with an arrow between them) and then reload each time (using the button that looks like a circular arrow)

"cdma_tx_hier1.grc", 

"cdma_rx_hier1.grc" 

-- Load the application "cdma_txrx1.grc" and have fun

Experiment with manual acq/tra, auto acq/tra, changing freq and timing offset, SNR, modulation/coding type, etc

-- If you have 2 USRPs load the cdma_tx.grc and cdma_rx.grc and enjoy real-time CDMA transmission. Careful: if you are using USRPs then you need to design your PHY layer parameters carefully for the environment or operation (e.g., number of filters in the frequency acquisition block, etc)
You can also use the cdma_tx.grc and cdma_rx.grc by writting
and reading to a fifo (first do > mkfifo /tmp/cdma.fifo)

This module has been tested with gnuradio 3.7.10
