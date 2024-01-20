#! /usr/bin/env python3

### Author: Ahmed Tijani Akinfalabi
### Date: 2024-01-19
### Name: FASTA-Parser 
### Description: Test Examination 2, Task 2

import sys, os, re

class FastaParser:
    def help(self):
        print("\nUsage: python3 script.py --help | --get-seq | --grep-seq |--get-n  ?[PATTERN|ID]? [FILE]")
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

    def get_n(self, file):
        with open(file, "r") as file:
            pattern = re.compile(r'(\w+\|\w+\|\w+)')
            header_id = None
            seq = None

            for line in file:
                if line.startswith(">"):
                    if header_id is not None:
                        print(f'{header_id} \t {seq}')
                    header_id = pattern.findall(line)[0] if pattern.findall(line) else "Unknown"
                    seq = 0
                elif not line.startswith(">"):
                    seq += len(line.strip())

            print(f'{header_id} \t {seq}')

    def get_seq(self, file, id=''):
        indicator = False
        with open(file, "r") as fasta_file:
            if "*" not in id:
                for line in fasta_file:
                    if indicator and line.startswith(">"):
                        break
                    if re.search('^>\S+' + id, line):
                        indicator = True
                    if indicator:
                        print(line)

                if not indicator:
                    print("This file does not contain your ID!")
            elif "*" in id:
                pass  # Implementation for handling wildcard ID goes here

    def search_seq(self, file, id=''):
        stats = {}  # A hash table containing the header_id and their sequences

        with open(file, 'r') as fasta_file:
            header_id = None
            seq_lines = []

            for line in fasta_file:
                if re.search('^>sp\|(\w+)\|(\w+)', line):
                    if header_id and seq_lines:
                        stats[header_id.group()] = ''.join(seq_lines)
                        seq_lines = []

                    header_id = re.match('^>(\S+)', line)

                elif re.search('(?:(?!>)[A-Z])+', line):
                    seq_match = re.match('(?:(?!>)[A-Z])+', line)
                    if seq_match:
                        seq = seq_match.group()
                        seq_lines.append(seq)

            if header_id and seq_lines:
                stats[header_id.group(1)] = ''.join(seq_lines)

        for key, val in stats.items():
            if re.search(rf'^>\S+{re.escape(id)}', key, re.IGNORECASE):
                print(val)

    def main(self, argv):
        if len(sys.argv) < 2 or sys.argv[1] == "--help":
            self.help()
        else:
            if sys.argv[1] not in ['--get-seq', '--grep-seq', '--get-n']:
                print("Wrong argument! Valid arguments are --help | --get-seq | --grep-seq |--get-n")
            elif sys.argv[1] == '--get-seq':
                if os.path.isfile(argv[3]) and argv[3].endswith('fasta'):
                    id_arg = sys.argv[2] if re.search('[A-Z_]+', sys.argv[2]) else None
                    self.get_seq(argv[3], id_arg)
                else:
                    print(f'File `{argv[3]}` does not exist or is not a fasta file')
            elif sys.argv[1] == '--grep-seq':
                if os.path.isfile(argv[3]) and argv[3].endswith('fasta'):
                    id_arg = sys.argv[2] if re.search('[A-Z_]+', sys.argv[2]) else None
                    self.search_seq(argv[3], id_arg)
                else:
                    print(f'File `{argv[3]}` does not exist or is not a fasta file')
            elif sys.argv[1] == '--get-n':
                if os.path.isfile(argv[2]) and argv[2].endswith('fasta'):
                    self.get_n(argv[2])
                else:
                    print(f'File `{argv[2]}` does not exist or is not a fasta file')

if __name__ == "__main__":
    fasta_parser = FastaParser()
    fasta_parser.main(sys.argv)
