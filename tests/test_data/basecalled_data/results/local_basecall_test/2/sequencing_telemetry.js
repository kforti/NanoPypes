[{"tracking_id": {"asic_id": "484243955", "asic_id_eeprom": "2595130", "asic_temp": "32.509274", "asic_version": "IA02D", "auto_update": "0", "auto_update_source": "https://mirror.oxfordnanoportal.com/software/MinKNOW/", "bream_is_standard": "0", "device_id": "MN27234", "device_type": "minion", "exp_script_name": "d7c38672c0c2d88fce4cc94277787fa3cd2f5bc9-346b21aa2f245c8a22cb68987cd5a2ca66990dad", "exp_script_purpose": "sequencing_run", "exp_start_time": "2018-11-08T19:37:33Z", "flow_cell_id": "FAK30311", "heatsink_temp": "33.031250", "hostname": "imac.ad.umassmed.edu", "installation_type": "nc", "local_firmware_file": "1", "operating_system": "Darwin 17.7.0", "protocol_run_id": "15ba4f35-c665-4e92-bc9a-92e69aff5e97", "protocols_version": "1.15.10.16", "run_id": "557afda1f1ddd31678d0c6378228345cc1b6bfa5", "sample_id": "test", "usb_config": "firm_1.2.3_ware#rbt_4.5.6_rbt#ctrl#USB3", "version": "1.15.4", "msg_id": "7c68b738-a917-4d34-82ca-c5f8437bf235"}, "software": {"name": "albacore-basecalling", "version": "2.3.3", "analysis": "1d_basecalling"}, "context_tags": {"experiment_duration_set": "360", "experiment_type": "lambda_burn_in", "fast5_output_fastq_in_hdf": "1", "fast5_raw": "1", "fast5_reads_per_folder": "4000", "fastq_enabled": "1", "fastq_reads_per_file": "4000", "filename": "imac_ad_umassmed_edu_20181108_fak30311_mn27234_sequencing_run_test_61366", "flowcell_type": "flo-min106", "kit_classification": "none", "local_basecalling": "1", "local_bc_comp_model": "", "local_bc_temp_model": "template_r9.4_450bps_5mer_raw.jsn", "sample_frequency": "4000", "sequencing_kit": "sqk-lsk109", "user_filename_input": "test"}, "segment_type": "albacore-acquisition", "segment_number": 1, "segment_duration": 60, "aggregation": "cumulative", "latest_run_time": 740.87675, "run_id": "557afda1f1ddd31678d0c6378228345cc1b6bfa5", "read_count": 20, "albacore_opts": {"list_workflows": false, "worker_threads": 1, "resume": "", "flowcell": "FLO-MIN106", "kit": "SQK-LSK109", "barcoding": false, "align_ref": null, "config": "r94_450bps_linear.cfg", "debug": false, "recursive": false, "files_per_batch_folder": 4000, "output_format": "fastq", "reads_per_fastq_batch": 1000, "disable_filtering": false, "disable_pings": false, "logfile": "pipeline.log", "summfile": "sequencing_summary.txt", "cfgfile": "configuration.cfg"}, "albacore_analysis_id": "650d81df-151c-4538-bf4d-d5f984e19005", "reads_per_channel_dist": [{"channel": 191, "count": 1}, {"channel": 150, "count": 1}, {"channel": 205, "count": 1}, {"channel": 463, "count": 1}, {"channel": 331, "count": 1}, {"channel": 274, "count": 1}, {"channel": 253, "count": 1}, {"channel": 112, "count": 1}, {"channel": 59, "count": 1}, {"channel": 468, "count": 1}, {"channel": 323, "count": 1}, {"channel": 353, "count": 1}, {"channel": 221, "count": 1}, {"channel": 306, "count": 1}, {"channel": 263, "count": 1}, {"channel": 479, "count": 1}, {"channel": 86, "count": 1}, {"channel": 60, "count": 1}, {"channel": 101, "count": 1}, {"channel": 201, "count": 1}], "channel_count": 20, "levels_sums": {"open_pore_level_sum": 4603.79264831543, "count": 20}, "segmentation": {"component_index": 0}, "basecall_1d": {"exit_status_dist": {"pass": 20}, "component_index": 1, "seq_len_bases_sum_temp": 93488, "read_len_events_sum_temp": 193173, "qscore_sum_temp": {"sum": 204.46299999999997, "count": 20, "mean": 10.223149999999999}, "qscore_dist_temp": [{"mean_qscore": 9.5, "count": 1}, {"mean_qscore": 11.0, "count": 4}, {"mean_qscore": 9.0, "count": 3}, {"mean_qscore": 10.5, "count": 7}, {"mean_qscore": 8.5, "count": 1}, {"mean_qscore": 10.0, "count": 3}, {"mean_qscore": 7.0, "count": 1}], "speed_events_per_second_dist_temp": [{"speed": 799, "count": 17}, {"speed": 800, "count": 3}], "speed_bases_per_second_dist_temp": [{"speed": 402, "count": 1}, {"speed": 354, "count": 1}, {"speed": 384, "count": 2}, {"speed": 406, "count": 3}, {"speed": 370, "count": 1}, {"speed": 418, "count": 1}, {"speed": 278, "count": 1}, {"speed": 284, "count": 1}, {"speed": 364, "count": 1}, {"speed": 388, "count": 1}, {"speed": 424, "count": 1}, {"speed": 434, "count": 1}, {"speed": 368, "count": 1}, {"speed": 390, "count": 1}, {"speed": 348, "count": 1}, {"speed": 394, "count": 1}, {"speed": 342, "count": 1}], "seq_len_events_dist_temp": [{"length": 12000, "count": 3}, {"length": 8000, "count": 1}, {"length": 0, "count": 1}, {"length": 6000, "count": 4}, {"length": 4000, "count": 2}, {"length": 50000, "count": 1}, {"length": 5000, "count": 3}, {"length": 13000, "count": 1}, {"length": 18000, "count": 1}, {"length": 1000, "count": 1}, {"length": 7000, "count": 1}, {"length": 3000, "count": 1}], "seq_len_bases_dist_temp": [{"length": 6000, "count": 3}, {"length": 3000, "count": 6}, {"length": 0, "count": 2}, {"length": 2000, "count": 5}, {"length": 26000, "count": 1}, {"length": 4000, "count": 1}, {"length": 8000, "count": 1}, {"length": 1000, "count": 1}], "strand_median_pa": {"sum": 1734.4444885253906, "count": 20, "mean": 86.72222442626953}, "strand_sd_pa": {"sum": 80.20256567001343, "count": 20, "mean": 4.010128283500672}}},{"tracking_id": {"asic_id": "484243955", "asic_id_eeprom": "2595130", "asic_temp": "32.509274", "asic_version": "IA02D", "auto_update": "0", "auto_update_source": "https://mirror.oxfordnanoportal.com/software/MinKNOW/", "bream_is_standard": "0", "device_id": "MN27234", "device_type": "minion", "exp_script_name": "d7c38672c0c2d88fce4cc94277787fa3cd2f5bc9-346b21aa2f245c8a22cb68987cd5a2ca66990dad", "exp_script_purpose": "sequencing_run", "exp_start_time": "2018-11-08T19:37:33Z", "flow_cell_id": "FAK30311", "heatsink_temp": "33.031250", "hostname": "imac.ad.umassmed.edu", "installation_type": "nc", "local_firmware_file": "1", "operating_system": "Darwin 17.7.0", "protocol_run_id": "15ba4f35-c665-4e92-bc9a-92e69aff5e97", "protocols_version": "1.15.10.16", "run_id": "557afda1f1ddd31678d0c6378228345cc1b6bfa5", "sample_id": "test", "usb_config": "firm_1.2.3_ware#rbt_4.5.6_rbt#ctrl#USB3", "version": "1.15.4", "msg_id": "f0090868-cf69-439b-89fa-7d2598735d8e"}, "software": {"name": "albacore-basecalling", "version": "2.3.3", "analysis": "1d_basecalling"}, "context_tags": {"experiment_duration_set": "360", "experiment_type": "lambda_burn_in", "fast5_output_fastq_in_hdf": "1", "fast5_raw": "1", "fast5_reads_per_folder": "4000", "fastq_enabled": "1", "fastq_reads_per_file": "4000", "filename": "imac_ad_umassmed_edu_20181108_fak30311_mn27234_sequencing_run_test_61366", "flowcell_type": "flo-min106", "kit_classification": "none", "local_basecalling": "1", "local_bc_comp_model": "", "local_bc_temp_model": "template_r9.4_450bps_5mer_raw.jsn", "sample_frequency": "4000", "sequencing_kit": "sqk-lsk109", "user_filename_input": "test"}, "segment_type": "albacore-acquisition", "segment_number": 1, "segment_duration": 60, "aggregation": "segment", "latest_run_time": 740.87675, "run_id": "557afda1f1ddd31678d0c6378228345cc1b6bfa5", "read_count": 20, "albacore_opts": {"list_workflows": false, "worker_threads": 1, "resume": "", "flowcell": "FLO-MIN106", "kit": "SQK-LSK109", "barcoding": false, "align_ref": null, "config": "r94_450bps_linear.cfg", "debug": false, "recursive": false, "files_per_batch_folder": 4000, "output_format": "fastq", "reads_per_fastq_batch": 1000, "disable_filtering": false, "disable_pings": false, "logfile": "pipeline.log", "summfile": "sequencing_summary.txt", "cfgfile": "configuration.cfg"}, "albacore_analysis_id": "650d81df-151c-4538-bf4d-d5f984e19005", "reads_per_channel_dist": [{"channel": 191, "count": 1}, {"channel": 150, "count": 1}, {"channel": 205, "count": 1}, {"channel": 463, "count": 1}, {"channel": 331, "count": 1}, {"channel": 274, "count": 1}, {"channel": 253, "count": 1}, {"channel": 112, "count": 1}, {"channel": 59, "count": 1}, {"channel": 468, "count": 1}, {"channel": 323, "count": 1}, {"channel": 353, "count": 1}, {"channel": 221, "count": 1}, {"channel": 306, "count": 1}, {"channel": 263, "count": 1}, {"channel": 479, "count": 1}, {"channel": 86, "count": 1}, {"channel": 60, "count": 1}, {"channel": 101, "count": 1}, {"channel": 201, "count": 1}], "channel_count": 20, "levels_sums": {"open_pore_level_sum": 4603.79264831543, "count": 20}, "segmentation": {"component_index": 0}, "basecall_1d": {"exit_status_dist": {"pass": 20}, "component_index": 1, "seq_len_bases_sum_temp": 93488, "read_len_events_sum_temp": 193173, "qscore_sum_temp": {"sum": 204.46299999999997, "count": 20, "mean": 10.223149999999999}, "qscore_dist_temp": [{"mean_qscore": 9.5, "count": 1}, {"mean_qscore": 11.0, "count": 4}, {"mean_qscore": 9.0, "count": 3}, {"mean_qscore": 10.5, "count": 7}, {"mean_qscore": 8.5, "count": 1}, {"mean_qscore": 10.0, "count": 3}, {"mean_qscore": 7.0, "count": 1}], "speed_events_per_second_dist_temp": [{"speed": 799, "count": 17}, {"speed": 800, "count": 3}], "speed_bases_per_second_dist_temp": [{"speed": 402, "count": 1}, {"speed": 354, "count": 1}, {"speed": 384, "count": 2}, {"speed": 406, "count": 3}, {"speed": 370, "count": 1}, {"speed": 418, "count": 1}, {"speed": 278, "count": 1}, {"speed": 284, "count": 1}, {"speed": 364, "count": 1}, {"speed": 388, "count": 1}, {"speed": 424, "count": 1}, {"speed": 434, "count": 1}, {"speed": 368, "count": 1}, {"speed": 390, "count": 1}, {"speed": 348, "count": 1}, {"speed": 394, "count": 1}, {"speed": 342, "count": 1}], "seq_len_events_dist_temp": [{"length": 12000, "count": 3}, {"length": 8000, "count": 1}, {"length": 0, "count": 1}, {"length": 6000, "count": 4}, {"length": 4000, "count": 2}, {"length": 50000, "count": 1}, {"length": 5000, "count": 3}, {"length": 13000, "count": 1}, {"length": 18000, "count": 1}, {"length": 1000, "count": 1}, {"length": 7000, "count": 1}, {"length": 3000, "count": 1}], "seq_len_bases_dist_temp": [{"length": 6000, "count": 3}, {"length": 3000, "count": 6}, {"length": 0, "count": 2}, {"length": 2000, "count": 5}, {"length": 26000, "count": 1}, {"length": 4000, "count": 1}, {"length": 8000, "count": 1}, {"length": 1000, "count": 1}], "strand_median_pa": {"sum": 1734.4444885253906, "count": 20, "mean": 86.72222442626953}, "strand_sd_pa": {"sum": 80.20256567001343, "count": 20, "mean": 4.010128283500672}}}]