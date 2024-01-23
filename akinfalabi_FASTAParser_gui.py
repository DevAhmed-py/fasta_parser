#! /usr/bin/env python3

### Author: Ahmed Tijani Akinfalabi
### Date: 2024-01-19
### Name: FASTA-Parser 
### Description: Test Examination 2, Task 2

import sys, os, re
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.messagebox as mbox
from guibaseclass import GuiBaseClass
from scrolled import Scrolled


class FastaParserGui(GuiBaseClass):

    def __init__(self,root):
        super().__init__(root)

        self.lastdir = None  # Last opened file directory
        self.filetypes = [('Fasta Files', '*.fasta'), ('Text Files', '*.txt'), ('All Files', '*.*')]

        fmenu = self.getMenu('File')
        fmenu.insert_command(0,label = "Open File ...", underline = 0,command = self.fileOpen)
        # fmenu.insert_command(1, label = "Save File ...", underline = 0, command = self.fileSave)
        
        frame = self.getFrame()
        frame.pack(side="top",fill= "both")

        # Create ttk.Entry for entering FASTA ID
        self.seq_id = ttk.Entry(frame)
        self.seq_id.insert(0, "Please enter your sequence ID")
        # self.seq_id.grid(row=0, column=0, padx=5, pady=5)
        self.seq_id.pack(side="left",pady=10, fill="both",expand=True)
        
        # Buttons 
        # I could use lambda function to pass self.file into the function but the result will be displayed in the terminal.
        get_n_button = ttk.Button(frame, text = "--get-n", command = self.get_n_gui)
        # get_n_button.pack(side="top", pady=10,fill= "both", expand=True)
        get_n_button.pack(pady=10,fill= "both", expand=True)        # without side

        get_seq_button = ttk.Button(frame, text = "--get-seq", command = self.get_seq_gui)
        get_seq_button.pack(pady=10,fill="both",expand=True)

        grep_seq_button=ttk.Button(frame, text = "--grep-seq", command = self.search_seq_gui)
        # grep_seq_button.pack(side="bottom",pady=10,fill="both",expand=True)
        grep_seq_button.pack(pady=10,fill="both",expand=True)       # without side
        

        # Create a ScrolledText widget for displaying the sequence text
        # self.text = tk.Text(frame, wrap = "none")
        # Scrolled(self.text)


        # Text widget with scrollbar on the left side
        self.text = tk.Text(frame, wrap= "word")
        self.text.pack(side="left", fill="both", expand=True)

        scrollbar_text = tk.Scrollbar(frame, command=self.text.yview)
        scrollbar_text.pack(side="left", fill="y")
        self.text.config(yscrollcommand=scrollbar_text.set)

        # # Text widget with scrollbar on the right side
        # self.text2 = tk.Text(frame, wrap="word")
        # self.text2.pack(side="right", fill="both", expand=True)

        # scrollbar_text2 = tk.Scrollbar(frame, command=self.text2.yview)
        # scrollbar_text2.pack(side="right", fill="y")
        # self.text2.config(yscrollcommand=scrollbar_text2.set)

                
    def fileOpen(self):
        if self.lastdir is not None:
            initialdir = self.lastdir
        else:
            initialdir = os.getcwd()

        self.file = fd.askopenfilename(initialdir = initialdir, title = "Select a Fasta file", filetypes=self.filetypes)
        
        # self.message(self.file)
        if os.path.isfile(self.file):
            with open(self.file, "r") as file:
                content = file.read()
                self.text.delete('1.0', 'end')
                self.text.insert('1.0', content)

    def get_n_gui(self):
        with open(self.file, "r") as fasta_file:
            pattern = re.compile(r'(\w+\|\w+\|\w+)')
            header_id = None
            seq = None
            self.text.delete('1.0', 'end')      # Delete the text field
                        
            for line in fasta_file:
                if line.startswith(">"):
                    if header_id is not None:
                        self.text.insert('1.0', f'{header_id} \t {seq} \n' )
                    header_id = pattern.findall(line)[0] if pattern.findall(line) else "Unknown"
                    seq = 0
                elif not line.startswith(">"):
                    seq += len(line.strip())

        self.text.insert('1.0', f'{header_id} \t {seq} \n')

    def get_seq_gui(self):
        indicator = False
        id = self.seq_id.get()
        self.text.delete('1.0', 'end')

        with open(self.file, "r") as fasta_file:
            if "*" not in id:
                for line in fasta_file:
                    if indicator and line.startswith(">"):
                        break
                    if re.search('^>\S+' + id, line):
                        indicator = True
                    if indicator:
                        self.text.insert('1.0', line[-1])
                if not indicator:
                    self.text.insert('1.0', "This file does not contain your ID!")
            
            elif "*" in id:
                # extract the ID, and then the search for the line ^> 
                # re.search(f"^>[^\s]*{id}",line)
                pass  # Implementation for handling wildcard ID goes here


    def search_seq_gui(self):
        stats = {}  # A hash table containing the header_id and their sequences
        header_id = None
        seq_lines = []
        id = self.seq_id.get()
        
        with open(self.file, 'r') as fasta_file:
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
                self.text.delete('1.0', 'end')
                self.text.insert('1.0', val)
                
    
    def help(self):
        print("\nUsage: python3 script.py --help | --get-seq | --grep-seq |--get-n  ?[PATTERN|ID]? [FILE] | --gui")
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
            if sys.argv[1] not in ['--get-seq', '--grep-seq', '--get-n', '--gui']:
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
    root   = tk.Tk()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--gui":
            fasta_class = FastaParserGui(root)
            root.geometry('500x400')
            root.title("FASTA Parser App")
            fasta_class.fileOpen()
            fasta_class.mainLoop()

        # after importing
        # else:
        #     fastaParser2.main(sys.argv)
        
        else:
            fasta_class = FastaParserGui(root)
            fasta_class.main(sys.argv)
