#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
#
#       run-intersect-coding genes.py
#==============================================================================
import argparse
import sys
import os
# Make utilities folder available
sys.path.append(os.path.abspath("../"))
from utilities.runner import sub_call
from utilities.io import list_files
from fnmatch import fnmatch
#==============================================================================
#Command line options==========================================================
#==============================================================================
parser = argparse.ArgumentParser()
parser.add_argument("input", type=str,
                    help="A vcf file (version 4.0 or 4.1) or folder of vcf files")
parser.add_argument("gtf", type=str,
                    help="A GTF file containing positional information for coding genes")
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()
#==============================================================================


def handle_input(input):
    """If a directory is passed return all the files in the directory and sub-
     directories in a list, if a file is provided return a list with one entry.
    """
    if os.path.isdir(input):
        return list_files(input)
    elif os.path.isfile(input):
        return [input]


def get_intersect_params(infile, gtf):

    a = infile
    b = gtf

    intersect_params = ["intersectBed", "-header",
                        "-a", a,
                        "-b", b,
                        '-wa', '-wb']

    return intersect_params


def main():

    # Filename pattern matches any file ending with _known.vcf
    fpattern = '*_noclusters.vcf'
    # fpattern = '*_known.vcf'
    infiles = [f for f in handle_input(args.input) if fnmatch(f, fpattern)]

    for infile in infiles:

        head, tail = os.path.split(infile)
        outfile = tail.split(".")[0]+"_coding"+".vcf"
        outfile = os.path.join(head, outfile)

        print "Filtering file: %s" % infile
        intersect_params = get_intersect_params(infile, args.gtf)

        with open(outfile, "w") as outfile:
            sub_call(intersect_params, stdout=outfile)


if __name__ == "__main__":
    main()
