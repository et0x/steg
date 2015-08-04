#!/usr/bin/python
import Image, sys, os
from optparse import OptionParser

# this is a unique binary pattern the decoding algorithm looks for to know to stop reading data
endstring = "01010101101010101111111100000000"

