#! /usr/bin/env python3

### Author: Ahmed Tijani Akinfalabi
### Date: 2024-01-19
### Name: FASTA-Parser 
### Description: Test Examination 2, Task 2

import sys, os, re

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


def get_n(file):
    # Implement a –get-n function to display the sequence IDs and 
    # the length of the protein sequence for each ID as tabulated 
    # output.

    with open(file, "r") as file:
        pattern = re.compile(r'(\w+\|\w+\|\w+)')
        header_id = None
        seq = None

        for line in file:
            if line.startswith(">"):
                # If there was a previous sequence, print its ID and length
                if header_id != None:
                    print(f'{header_id} \t {seq}')
                    
                # Reset ID and sequence length for the new sequence
                header_id = pattern.findall(line)[0] if pattern.findall(line) else "Unknown"
                seq = 0

            elif not line.startswith(">"):
                # Accumulate the length of the sequence
                seq += len(line.strip())
                
        # Print the last sequence
        print(f'{header_id} \t {seq}')


def get_seq(file, id=''):
    # Write further a search function for a specific FASTA ID, 
    # called if –get-seq which displays the valid FASTA sequence 
    # for this ID including the header

    with open(file, "r") as fasta_file:
        indicator = False
        
        if "*" not in id:
            for line in fasta_file:
                if indicator and line.startswith(">"):
                    break
                if re.search('^>\S+'+id, line):
                    indicator = True
                if indicator:
                    print(line)
            
            if indicator == False:
                print("This file does not contain your ID!")
        elif "*" in id:
            # I'd implement this later
            # Hint: Don’t print the text inside of the function(s) 
            # but return the FASTA text to the function caller. 
            # Print it then outside of the function, so inside main.
            pass 
            # id = id.rstrip('*')
            # print(id)
            # for line in fasta_file:
            #     if indicator and line.startswith(">"):
            #         indicator=False
            #     if re.search(rf'^>\S+{id}\S+',line):
            #         indicator = True
            #     if indicator:
            #         print(line)

   
def search_seq(file, id=''):
    # Write further a search function for a specific FASTA ID, 
    # called if –get-seq which displays the valid FASTA sequence 
    # for this ID including the header

    stats = {}         # A hash table containing the header_id and their sequences

    with open(file, 'r') as fasta_file:
        header_id = None
        seq_lines = []

        for line in fasta_file:
            if re.search('^>sp\|(\w+)\|(\w+)', line):
                # If a new header is encountered, store the previous sequence (if any)
                if header_id and seq_lines:
                    stats[header_id.group()] = ''.join(seq_lines)
                    seq_lines = []

                header_id = re.match('^>(\S+)', line)
                # print(header_id.group())

            elif re.search('(?:(?!>)[A-Z])+', line):
                seq_match = re.match('(?:(?!>)[A-Z])+', line)
                if seq_match:
                    # Check to make sure re.match() is not returning None for some lines before accessing its group
                    seq = seq_match.group()
                    seq_lines.append(seq)

        # Capture the last sequence in case the file ends with a sequence
        if header_id and seq_lines:
            stats[header_id.group(1)] = ''.join(seq_lines)

    for key, val in stats.items():
        if re.search(rf'^>\S+{re.escape(id)}', key):
            print(val)
       
def main(argv):
    if (len(sys.argv)) < 2 or sys.argv[1] == "--help":
        help(argv)

    else:
        if not sys.argv[1] in ['--get-seq', '--grep-seq', '--get-n']:
            print("Wrong argument! Valid arguments are --help | --get-seq | --grep-seq |--get-n")

        elif sys.argv[1] == '--get-seq':
            if os.path.isfile(argv[3]) and argv[3].endswith('fasta'):
                id = sys.argv[2] if re.search('[A-Z_]+', sys.argv[2]) else None
                get_seq(sys.argv[3], id)
            else:
                print(f'File `{argv[3]}` does not exist or not a fasta file')
        elif sys.argv[1] == '--grep-seq':
            if os.path.isfile(argv[3]) and argv[3].endswith('fasta'):
                id = sys.argv[2] if re.search('[A-Z_]+', sys.argv[2]) else None
                search_seq(sys.argv[3], id) 
            else:
                print(f'File `{argv[3]}` does not exist or not a fasta file')
        elif sys.argv[1] == '--get-n':
            if os.path.isfile(argv[2]) and argv[2].endswith('fasta'):
                get_n(argv[2])
            else:
                print(f'File `{argv[2]}` does not exist or not a fasta file')

if __name__ == "__main__":
    main(sys.argv)
    

# Another approach of reading the file and extracting header and sequence
# with open(file, 'r') as fasta_file:
    #     header_id = None
    #     seq_lines = []

    #     for line in fasta_file:
    #         if re.search('^>sp\|(\w+)\|(\w+)', line):
    #             # If a new header is encountered, store the previous sequence (if any)
    #             if header_id and seq_lines:
    #                 stats[header_id.group()] = ''.join(seq_lines)
    #                 seq_lines = []

    #             header_id = re.match('^>(\S+)', line)
    #             # print(header_id.group())

    #         elif re.search('(?:(?!>)[A-Z])+', line):
    #             seq_match = re.match('(?:(?!>)[A-Z])+', line)
    #             if seq_match:
    #                 # Check to make sure re.match() is not returning None for some lines before accessing its group
    #                 seq = seq_match.group()
    #                 seq_lines.append(seq)

    #     # Capture the last sequence in case the file ends with a sequence
    #     if header_id and seq_lines:
    #         stats[header_id.group(1)] = ''.join(seq_lines)

    # for key, val in stats.items():
    #     print(f'{key} \t {len(val)}')



# Another approach for getting sequence

    # id_pattern = re.escape(id)  # Escape special characters in the ID for regex
    # is_wildcard = '*' in id

    # with open(file, "r") as fasta_file:
    #     indicator = False

    #     for line in fasta_file:
    #         if indicator and line.startswith(">"):
    #             break

    #         if is_wildcard:
    #             if re.search(rf'^>\S+{id_pattern}\S*', line):
    #                 indicator = True
    #         else:
    #             if re.search(rf'^>\S+{id_pattern}', line):
    #                 indicator = True

    #         if indicator:
    #             print(line)

    #     if not indicator or not id_pattern:
    #         print("This file does not contain your ID!")