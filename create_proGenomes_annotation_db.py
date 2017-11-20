#!/usr/bin/env python3
"""
Create annotations from proGenomes protein fasta.
"""
__author__ = "Fredrik Boulund"
__date_ = "2017"

from sys import argv, exit
import re
import argparse
import json


def parse_args():

    parser = argparse.ArgumentParser(description="Create annotation db for proGenomes protein fasta")
    parser.add_argument("fastafile", 
            help="proGenomes protein fasta file.")
    parser.add_argument("-o", "--outfile", metavar="FILENAME", 
            default="annotations.json", 
            help="Output filename [%(default)s].")

    if len(argv) < 2:
        parser.print_help()
        exit(1)

    return parser.parse_args()


def parse_annotation_info(line, regex): 
    match = regex.findall(line)
    if match:
        entries = dict((k, v) for k, v in match)
        entries["sequence"] = line.split(maxsplit=1)[0][1:]
        return entries
    return "Error: "+line


def parse_fasta(fastafile):
    with open(fastafile) as f:
        for line in f:
            if line.startswith(">"):
                yield line[:-4] # all lines in proGenomes protein fasta end with four unnecessary chars: ' />\n'
    

def main(fastafile, outfile):
    # Regex, snagged from SO and slightly modified: 
    # https://stackoverflow.com/questions/33991032/how-to-parse-a-string-with-key-value-pairs-separated-by-spaces
    #  ([^\s=]+)                         A key (any non-whitespace except =)
    #           =                        followed by =
    #            ((?:[^\s=]+(?:\s|$))*)  Any number of repetitions of a string
    #                                    without = followed by either whitespace
    #                                    or the end of the input
    regex_string = r'([^\s=]+)=((?:[^\s=]+(?:\s|$))*)'
    regex = re.compile(regex_string)

    annotation_info = [parse_annotation_info(header_line, regex) for header_line in parse_fasta(fastafile)]
    with open(outfile, "w") as outf:
        json.dump(annotation_info, outf)
        

if __name__ == "__main__":
    options = parse_args()
    main(options.fastafile, options.outfile)
