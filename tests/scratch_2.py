import csv

# with open('test_data/basecall_files/seq_sums/sum_combined.txt', 'r') as src_file:
#     csv_reader = csv.reader(src_file, delimiter='\t')
#     for i, line in enumerate(csv_reader):
#         print(line)

y = ['filename', 'read_id', 'run_id', 'channel', 'start_time', 'duration', 'num_events', 'passes_filtering', 'template_start', 'num_events_template', 'template_duration', 'num_called_template', 'sequence_length_template', 'mean_qscore_template', 'strand_score_template', 'calibration_strand_genome_template', 'calibration_strand_identity_template', 'calibration_strand_accuracy_template', 'calibration_strand_speed_bps_template', 'barcode_arrangement', 'barcode_score', 'barcode_full_arrangement', 'front_score', 'rear_score', 'front_begin_index', 'front_foundseq_length', 'rear_end_index', 'rear_foundseq_length', 'kit', 'variant']

b = [['filename', 'read_id', 'run_id', 'channel', 'start_time', 'duration', 'num_events', 'passes_filtering', 'template_start', 'num_events_template', 'template_duration', 'num_called_template', 'sequence_length_template', 'mean_qscore_template', 'strand_score_template', 'calibration_strand_genome_template', 'calibration_strand_identity_template', 'calibration_strand_accuracy_template', 'calibration_strand_speed_bps_template', 'barcode_arrangement', 'barcode_score', 'barcode_full_arrangement', 'front_score', 'rear_score', 'front_begin_index', 'front_foundseq_length', 'rear_end_indexrear_foundseq_length', 'kit', 'variant']]
if y in b:
    print('hi')