#!/usr/bin/env python3

from Bio import SeqIO
from Bio.Seq import Seq
import os
from pathlib import Path
import logging
from joblib import Parallel, delayed


def preprocess_single_genome(filename):
    file = os.path.join(snakemake.input.assembly, filename)
    record_list = []
    if os.path.isdir(file): return
    with open(file, 'r') as infile:

        # Going through all the sequences from the input file
        sequences=[i for i in SeqIO.parse(infile, 'fasta')]
        for sequence in sequences:

            # Extracting the actual sequence and transforming it to string format
            data = sequence.seq
            s_data = str(data)
            s_result = ""

            for c in s_data:
                if c in {'A', 'C', 'G', 'T'}:
                    s_result = s_result + c
            
            
            record_list.append(Seq(s_result))


    # Writing our result to the output file
    if filename.endswith(".fna"): name = filename[:-4] + ".fasta"
    else: name = filename
    # Path(os.path.join(snakemake.output.report, name)).touch()
    with open(os.path.join(snakemake.output.report, name), 'w') as outfile:
        for i in range(len(record_list)):
            outfile.write('>Sequence{}\n'.format(i))
            outfile.write('{}\n'.format(record_list[i]))
    logging.info(f'File {counter} preprocessed')



logging.basicConfig(filename='preprocessing_all_genomes.log', level=logging.INFO)
logging.info('Logging initiated succesfully')
counter = 1

if not os.path.isdir(snakemake.output.report): os.mkdir(snakemake.output.report)
Parallel(n_jobs=28)(delayed(preprocess_single_genome)(filename) for filename in os.listdir(snakemake.input.assembly))

    