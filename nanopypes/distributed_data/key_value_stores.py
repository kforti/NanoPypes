from .partition_data import *

### kwargs = input_path, partitions, batch_size
partition_handler = {"ont_directories_single_read_fast5": partition_ont_seq_data,
                    }

### kwargs = input_data, save_path, task_name
extract_functions_handler = {"extract_partitioned_directories": extract_partitioned_directories,
                             "extract_sams": sam_to_bam,
                             "extract_porechop_demultiplex": porechop_demultiplexed_data,
                             "extract_fastqs": extract_ont_fastqs,
                             }

### kwargs = batches, save_path
merge_functions_handler = {"merge_bams": merge_bams}


function_keys = {
            "albacore_basecall":
                {
                    "partition": "extract_partitioned_directories",
                    "merge": ""
                },
            "minimap2_splice-map":
                {
                    "no_prev": "",
                    "albacore_basecall": "extract_fastqs",
                    "porechop_demultiplex": "extract_porechop_demultiplex",
                    "merge": "",
                },
            "porechop_demultiplex":
                {
                    "no_prev": "",
                    "albacore_basecall": "extract_partitioned_directories",
                },
            "samtools_sam_to_bam":
                {
                    "no_prev": "",
                    "minimap2_splice-map": "extract_sams",
                    "merge": "merge_bams",
                },
            "samtools_merge_bams":
                {
                    "no_prev": "",
                    "samtools_sam_to_bam": "merge_bams"
                },

        }
