#! /usr/bin/env python3

### Author: Ahmed Tijani Akinfalabi
### Date: 2024-01-19
### Name: FASTA-Parser 
### Description: Test Examination 2, Task 1

import sys, os

def help(argv):
    print(f"\nUsage: {argv[0]} --help | --get-seq | --grep-seq |--get-n  ?[PATTERN|ID]? [FILE]")
    print("""FASTA-Parser by Ahmed Tijani Akinfalabi, 2024
Extract information from FASTA sequence files
-------------------------------------------
Mandatory arguments are:
    FILE - one FASTA file
Optional arguments are (either --help, --get-n or ---get-seq or --grep-seq):
    --help              - display this help page
    --get-n             - show sequence lengths for all sequence IDs
    --get-seq  ID       - show the sequence for a given sequence ID 
    --grep-seq PATTERN  - search the sequences for a given amino acid (regex) pattern \n
          """)

def get_n():
    print('getting n')

def get_seq():
    print('seq getting')

def search_seq():
    print('seq search starting')

def main(argv):
    if (len(sys.argv)) < 2 or sys.argv[1] == "--help":
        help(argv)
       
    else:
        #print('entering else block')
        if not sys.argv[1] in ['--get-seq', '--grep-seq', '--get-n']:
            # print('entering the check for the first argv')
            print("Wrong argument! Valid arguments are --help | --get-seq | --grep-seq |--get-n")
          
        for file in sys.argv[2:]:
            #print('entering loop block')
            if sys.argv[1] == '--get-seq':
                if os.path.isfile(file) and file.split('.')[-1] == 'fasta':
                    get_seq()      
                else:
                    print(f'File `{file}` does not exist')
            elif sys.argv[1] == '--grep-seq':
                if os.path.isfile(file) and file.split('.')[-1] == 'fasta':
                    search_seq()      
                else:
                    print(f'File `{file}` does not exist')
            elif sys.argv[1] == '--get-n':
                if os.path.isfile(file) and file.split('.')[-1] == 'fasta':
                    get_n()     
                else:
                    print(f'File `{file}` does not exist')

if __name__ == "__main__":
    main(sys.argv)
