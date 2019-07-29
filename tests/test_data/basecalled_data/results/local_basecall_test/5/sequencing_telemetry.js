[{"tracking_id": {"asic_id": "484243955", "asic_id_eeprom": "2595130", "asic_temp": "32.509274", "asic_version": "IA02D", "auto_update": "0", "auto_update_source": "https://mirror.oxfordnanoportal.com/software/MinKNOW/", "bream_is_standard": "0", "device_id": "MN27234", "device_type": "minion", "exp_script_name": "d7c38672c0c2d88fce4cc94277787fa3cd2f5bc9-346b21aa2f245c8a22cb68987cd5a2ca66990dad", "exp_script_purpose": "sequencing_run", "exp_start_time": "2018-11-08T19:37:33Z", "flow_cell_id": "FAK30311", "heatsink_temp": "33.031250", "hostname": "imac.ad.umassmed.edu", "installation_type": "nc", "local_firmware_file": "1", "operating_system": "Darwin 17.7.0", "protocol_run_id": "15ba4f35-c665-4e92-bc9a-92e69aff5e97", "protocols_version": "1.15.10.16", "run_id": "557afda1f1ddd31678d0c6378228345cc1b6bfa5", "sample_id": "test", "usb_config": "firm_1.2.3_ware#rbt_4.5.6_rbt#ctrl#USB3", "version": "1.15.4", "msg_id": "e8f73cb7-5e2f-4b57-a109-2dceacf6c203"}, "software": {"name": "albacore-basecalling", "version": "2.3.3", "analysis": "1d_basecalling"}, "context_tags": {"experiment_duration_set": "360", "experiment_type": "lambda_burn_in", "fast5_output_fastq_in_hdf": "1", "fast5_raw": "1", "fast5_reads_per_folder": "4000", "fastq_enabled": "1", "fastq_reads_per_file": "4000", "filename": "imac_ad_umassmed_edu_20181108_fak30311_mn27234_sequencing_run_test_61366", "flowcell_type": "flo-min106", "kit_classification": "none", "local_basecalling": "1", "local_bc_comp_model": "", "local_bc_temp_model": "template_r9.4_450bps_5mer_raw.jsn", "sample_frequency": "4000", "sequencing_kit": "sqk-lsk109", "user_filename_input": "test"}, "segment_type": "albacore-acquisition", "segment_number": 1, "segment_duration": 60, "aggregation": "cumulative", "latest_run_time": 745.90325, "run_id": "557afda1f1ddd31678d0c6378228345cc1b6bfa5", "read_count": 20, "albacore_opts": {"list_workflows": false, "worker_threads": 1, "resume": "", "flowcell": "FLO-MIN106", "kit": "SQK-LSK109", "barcoding": false, "align_ref": null, "config": "r94_450bps_linear.cfg", "debug": false, "recursive": false, "files_per_batch_folder": 4000, "output_format": "fastq", "reads_per_fastq_batch": 1000, "disable_filtering": false, "disable_pings": false, "logfile": "pipeline.log", "summfile": "sequencing_summary.txt", "cfgfile": "configuration.cfg"}, "albacore_analysis_id": "293e5d0c-1112-4863-b728-041fe34672df", "reads_per_channel_dist": [{"channel": 274, "count": 1}, {"channel": 474, "count": 1}, {"channel": 181, "count": 1}, {"channel": 463, "count": 1}, {"channel": 276, "count": 1}, {"channel": 27, "count": 1}, {"channel": 18, "count": 1}, {"channel": 384, "count": 1}, {"channel": 119, "count": 2}, {"channel": 486, "count": 1}, {"channel": 59, "count": 1}, {"channel": 135, "count": 1}, {"channel": 160, "count": 2}, {"channel": 420, "count": 1}, {"channel": 508, "count": 1}, {"channel": 313, "count": 1}, {"channel": 490, "count": 1}, {"channel": 170, "count": 1}], "channel_count": 18, "levels_sums": {"open_pore_level_sum": 4611.285675048828, "count": 20}, "segmentation": {"component_index": 0}, "basecall_1d": {"exit_status_dist": {"pass": 20}, "component_index": 1, "seq_len_bases_sum_temp": 110800, "read_len_events_sum_temp": 227140, "qscore_sum_temp": {"sum": 203.35699999999997, "count": 20, "mean": 10.167849999999998}, "qscore_dist_temp": [{"mean_qscore": 8.0, "count": 2}, {"mean_qscore": 10.5, "count": 5}, {"mean_qscore": 9.0, "count": 2}, {"mean_qscore": 10.0, "count": 6}, {"mean_qscore": 8.5, "count": 1}, {"mean_qscore": 11.0, "count": 1}, {"mean_qscore": 11.5, "count": 2}, {"mean_qscore": 9.5, "count": 1}], "speed_events_per_second_dist_temp": [{"speed": 799, "count": 17}, {"speed": 800, "count": 3}], "speed_bases_per_second_dist_temp": [{"speed": 372, "count": 1}, {"speed": 370, "count": 1}, {"speed": 380, "count": 1}, {"speed": 428, "count": 1}, {"speed": 426, "count": 2}, {"speed": 366, "count": 1}, {"speed": 412, "count": 1}, {"speed": 386, "count": 1}, {"speed": 362, "count": 2}, {"speed": 424, "count": 1}, {"speed": 384, "count": 1}, {"speed": 408, "count": 1}, {"speed": 394, "count": 1}, {"speed": 354, "count": 1}, {"speed": 378, "count": 1}, {"speed": 350, "count": 1}, {"speed": 382, "count": 1}, {"speed": 314, "count": 1}], "seq_len_events_dist_temp": [{"length": 5000, "count": 2}, {"length": 10000, "count": 2}, {"length": 34000, "count": 1}, {"length": 3000, "count": 2}, {"length": 8000, "count": 1}, {"length": 39000, "count": 1}, {"length": 9000, "count": 1}, {"length": 4000, "count": 1}, {"length": 28000, "count": 1}, {"length": 11000, "count": 1}, {"length": 17000, "count": 1}, {"length": 22000, "count": 1}, {"length": 2000, "count": 1}, {"length": 7000, "count": 1}, {"length": 1000, "count": 2}, {"length": 0, "count": 1}], "seq_len_bases_dist_temp": [{"length": 2000, "count": 3}, {"length": 5000, "count": 3}, {"length": 16000, "count": 1}, {"length": 1000, "count": 2}, {"length": 4000, "count": 2}, {"length": 18000, "count": 1}, {"length": 14000, "count": 1}, {"length": 9000, "count": 1}, {"length": 10000, "count": 1}, {"length": 0, "count": 4}, {"length": 3000, "count": 1}], "strand_median_pa": {"sum": 1759.4211349487305, "count": 20, "mean": 87.97105674743652}, "strand_sd_pa": {"sum": 79.9041736125946, "count": 20, "mean": 3.9952086806297302}}},{"tracking_id": {"asic_id": "484243955", "asic_id_eeprom": "2595130", "asic_temp": "32.509274", "asic_version": "IA02D", "auto_update": "0", "auto_update_source": "https://mirror.oxfordnanoportal.com/software/MinKNOW/", "bream_is_standard": "0", "device_id": "MN27234", "device_type": "minion", "exp_script_name": "d7c38672c0c2d88fce4cc94277787fa3cd2f5bc9-346b21aa2f245c8a22cb68987cd5a2ca66990dad", "exp_script_purpose": "sequencing_run", "exp_start_time": "2018-11-08T19:37:33Z", "flow_cell_id": "FAK30311", "heatsink_temp": "33.031250", "hostname": "imac.ad.umassmed.edu", "installation_type": "nc", "local_firmware_file": "1", "operating_system": "Darwin 17.7.0", "protocol_run_id": "15ba4f35-c665-4e92-bc9a-92e69aff5e97", "protocols_version": "1.15.10.16", "run_id": "557afda1f1ddd31678d0c6378228345cc1b6bfa5", "sample_id": "test", "usb_config": "firm_1.2.3_ware#rbt_4.5.6_rbt#ctrl#USB3", "version": "1.15.4", "msg_id": "60903a70-a228-4a39-a9ca-35614cecfc17"}, "software": {"name": "albacore-basecalling", "version": "2.3.3", "analysis": "1d_basecalling"}, "context_tags": {"experiment_duration_set": "360", "experiment_type": "lambda_burn_in", "fast5_output_fastq_in_hdf": "1", "fast5_raw": "1", "fast5_reads_per_folder": "4000", "fastq_enabled": "1", "fastq_reads_per_file": "4000", "filename": "imac_ad_umassmed_edu_20181108_fak30311_mn27234_sequencing_run_test_61366", "flowcell_type": "flo-min106", "kit_classification": "none", "local_basecalling": "1", "local_bc_comp_model": "", "local_bc_temp_model": "template_r9.4_450bps_5mer_raw.jsn", "sample_frequency": "4000", "sequencing_kit": "sqk-lsk109", "user_filename_input": "test"}, "segment_type": "albacore-acquisition", "segment_number": 1, "segment_duration": 60, "aggregation": "segment", "latest_run_time": 745.90325, "run_id": "557afda1f1ddd31678d0c6378228345cc1b6bfa5", "read_count": 20, "albacore_opts": {"list_workflows": false, "worker_threads": 1, "resume": "", "flowcell": "FLO-MIN106", "kit": "SQK-LSK109", "barcoding": false, "align_ref": null, "config": "r94_450bps_linear.cfg", "debug": false, "recursive": false, "files_per_batch_folder": 4000, "output_format": "fastq", "reads_per_fastq_batch": 1000, "disable_filtering": false, "disable_pings": false, "logfile": "pipeline.log", "summfile": "sequencing_summary.txt", "cfgfile": "configuration.cfg"}, "albacore_analysis_id": "293e5d0c-1112-4863-b728-041fe34672df", "reads_per_channel_dist": [{"channel": 274, "count": 1}, {"channel": 474, "count": 1}, {"channel": 181, "count": 1}, {"channel": 463, "count": 1}, {"channel": 276, "count": 1}, {"channel": 27, "count": 1}, {"channel": 18, "count": 1}, {"channel": 384, "count": 1}, {"channel": 119, "count": 2}, {"channel": 486, "count": 1}, {"channel": 59, "count": 1}, {"channel": 135, "count": 1}, {"channel": 160, "count": 2}, {"channel": 420, "count": 1}, {"channel": 508, "count": 1}, {"channel": 313, "count": 1}, {"channel": 490, "count": 1}, {"channel": 170, "count": 1}], "channel_count": 18, "levels_sums": {"open_pore_level_sum": 4611.285675048828, "count": 20}, "segmentation": {"component_index": 0}, "basecall_1d": {"exit_status_dist": {"pass": 20}, "component_index": 1, "seq_len_bases_sum_temp": 110800, "read_len_events_sum_temp": 227140, "qscore_sum_temp": {"sum": 203.35699999999997, "count": 20, "mean": 10.167849999999998}, "qscore_dist_temp": [{"mean_qscore": 8.0, "count": 2}, {"mean_qscore": 10.5, "count": 5}, {"mean_qscore": 9.0, "count": 2}, {"mean_qscore": 10.0, "count": 6}, {"mean_qscore": 8.5, "count": 1}, {"mean_qscore": 11.0, "count": 1}, {"mean_qscore": 11.5, "count": 2}, {"mean_qscore": 9.5, "count": 1}], "speed_events_per_second_dist_temp": [{"speed": 799, "count": 17}, {"speed": 800, "count": 3}], "speed_bases_per_second_dist_temp": [{"speed": 372, "count": 1}, {"speed": 370, "count": 1}, {"speed": 380, "count": 1}, {"speed": 428, "count": 1}, {"speed": 426, "count": 2}, {"speed": 366, "count": 1}, {"speed": 412, "count": 1}, {"speed": 386, "count": 1}, {"speed": 362, "count": 2}, {"speed": 424, "count": 1}, {"speed": 384, "count": 1}, {"speed": 408, "count": 1}, {"speed": 394, "count": 1}, {"speed": 354, "count": 1}, {"speed": 378, "count": 1}, {"speed": 350, "count": 1}, {"speed": 382, "count": 1}, {"speed": 314, "count": 1}], "seq_len_events_dist_temp": [{"length": 5000, "count": 2}, {"length": 10000, "count": 2}, {"length": 34000, "count": 1}, {"length": 3000, "count": 2}, {"length": 8000, "count": 1}, {"length": 39000, "count": 1}, {"length": 9000, "count": 1}, {"length": 4000, "count": 1}, {"length": 28000, "count": 1}, {"length": 11000, "count": 1}, {"length": 17000, "count": 1}, {"length": 22000, "count": 1}, {"length": 2000, "count": 1}, {"length": 7000, "count": 1}, {"length": 1000, "count": 2}, {"length": 0, "count": 1}], "seq_len_bases_dist_temp": [{"length": 2000, "count": 3}, {"length": 5000, "count": 3}, {"length": 16000, "count": 1}, {"length": 1000, "count": 2}, {"length": 4000, "count": 2}, {"length": 18000, "count": 1}, {"length": 14000, "count": 1}, {"length": 9000, "count": 1}, {"length": 10000, "count": 1}, {"length": 0, "count": 4}, {"length": 3000, "count": 1}], "strand_median_pa": {"sum": 1759.4211349487305, "count": 20, "mean": 87.97105674743652}, "strand_sd_pa": {"sum": 79.9041736125946, "count": 20, "mean": 3.9952086806297302}}}]