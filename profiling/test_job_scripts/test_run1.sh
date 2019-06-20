#!/bin/bash
#BSUB -n 5
#BSUB -R "rusage[mem=10240]"
#BSUB -W 1:00
#BSUB -q short
#BSUB -R "span[hosts=1]"
#BSUB -o log_files/profile1_comp2.out
#BSUB -e log_files/profile1_comp2.err
#BSUB -K


read_fast5_basecaller.py --flowcell FLO-MIN106 --kit SQK-LSK109 --output_format fastq --save_path ../tests/test_data/profile_tests/comp2 --worker_threads 5 --input ../tests/test_data/minion_sample_raw_data/Experiment_01/sample_02_local/fast5/pass --reads_per_fastq_batch 1000 -r 
