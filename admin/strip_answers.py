# coding: utf-8

""" Strip the answer cells from an iPython notebook 'worksheet' """

from __future__ import division, print_function

__author__ = "adrn <adrn@astro.columbia.edu>"

# Standard library
import os, sys
from copy import deepcopy
import json
from argparse import ArgumentParser

def main(filename):
    with open(filename) as f:
        file_data = json.load(f)
        
    with_answers = deepcopy(file_data)
    without_answers = deepcopy(file_data)
    
    cells = without_answers['worksheets'][0]['cells']
    for cell in cells:
        if cell['cell_type'] == 'code':
            cell['input'] = []
    
    basename,ext = os.path.splitext(filename)
    
    with open("{0}_{1}{2}".format(basename, "with-answers", ext), 'w') as f:
        json.dump(with_answers, f)
    
    with open("{0}_{1}{2}".format(basename, "without-answers", ext), 'w') as f:
        json.dump(without_answers, f)
    
if __name__ == "__main__":
    parser = ArgumentParser(description="")
    parser.add_argument("-f", dest="file", default=None, required=True, type=str,
                    help="ipynb file to strip answers from")
    parser.add_argument("-i", dest="interactive", default=False, type=bool,
                    help="Ask about deleting each code cell")
    
    args = parser.parse_args()
    filename = args.file
    
    main(filename)