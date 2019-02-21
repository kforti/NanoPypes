import csv



with open('test_data/basecall_files/seq_sums/sum_combined.txt', 'r') as src_file:
    csv_reader = csv.reader(src_file, delimiter='\t')
    for i, line in enumerate(csv_reader):
        print(line)