import os

combined_reads = []
for path, subdirs, reads in os.walk('test_data'):
    combined_reads.extend([read for read in reads if read != []])
combined_reads.sort()
print(combined_reads)
