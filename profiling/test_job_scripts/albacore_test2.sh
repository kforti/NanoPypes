#!/bin/bash
#BSUB -J albacore_test2.sh
#BSUB -q short
#BSUB -P /project/umw_athma_pai
#BSUB -n 10
#BSUB -R "span[hosts=1]"
#BSUB -W 03:00
#BSUB -R "rusage[mem=20480]"
read_fast5_basecaller.py --flowcell FLO-MIN106 --kit SQK-LSK109 --output_format fastq -r --save_path /project/umw_athma_pai/kevin/data/Albacore_tests/albacore_test2.sh --worker_threads 10 --input /project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/albacore_test --reads_per_fastq_batch 1000
