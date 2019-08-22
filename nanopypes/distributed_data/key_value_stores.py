from .partition_data import *

### kwargs = input_path, partitions, batch_size
partition_functions_handler = {"ont_directories_single_read_fast5": partition_ont_seq_data,
                    }

### kwargs = input_data, save_path, task_name
extract_functions_handler = {"extract_partitioned_directories": extract_partitioned_directories,
                             }

### kwargs = batches, save_path
merge_functions_handler = {"sam_to_bam": sam_to_bam}


function_keys = {
            "albacore_basecall":
                {
                    "partition": {"ont_directories_single_read_fast5": "extract_partitioned_directories"},
                    "merge": ""
                },
            "minimap2_splice-map":
                {
                    "no_prev": "",
                    "albacore_basecall": "",
                    "porechop_demultiplex": "",
                    "merge": "",
                },
            "porechop_demultiplex":
                {
                    "no_prev": "",
                    "albacore_basecall": ""
                },
            "samtools_sam_to_bam":
                {
                    "no_prev": "",
                    "minimap2_splice-map": "",
                    "merge": "sam_to_bam",
                },
            "samtools_merge_bams":
                {
                    "no_prev": "",
                    "samtools_sam_to_bam": "sam_to_bam"
                },

        }
