[{"tracking_id": {"asic_id": "484243955", "asic_id_eeprom": "2595130", "asic_temp": "32.509274", "asic_version": "IA02D", "auto_update": "0", "auto_update_source": "https://mirror.oxfordnanoportal.com/software/MinKNOW/", "bream_is_standard": "0", "device_id": "MN27234", "device_type": "minion", "exp_script_name": "d7c38672c0c2d88fce4cc94277787fa3cd2f5bc9-346b21aa2f245c8a22cb68987cd5a2ca66990dad", "exp_script_purpose": "sequencing_run", "exp_start_time": "2018-11-08T19:37:33Z", "flow_cell_id": "FAK30311", "heatsink_temp": "33.031250", "hostname": "imac.ad.umassmed.edu", "installation_type": "nc", "local_firmware_file": "1", "operating_system": "Darwin 17.7.0", "protocol_run_id": "15ba4f35-c665-4e92-bc9a-92e69aff5e97", "protocols_version": "1.15.10.16", "run_id": "557afda1f1ddd31678d0c6378228345cc1b6bfa5", "sample_id": "test", "usb_config": "firm_1.2.3_ware#rbt_4.5.6_rbt#ctrl#USB3", "version": "1.15.4", "msg_id": "b7831249-077a-40ee-99a4-d70b13bb9721"}, "software": {"name": "albacore-basecalling", "version": "2.3.4", "analysis": "1d_basecalling"}, "context_tags": {"experiment_duration_set": "360", "experiment_type": "lambda_burn_in", "fast5_output_fastq_in_hdf": "1", "fast5_raw": "1", "fast5_reads_per_folder": "4000", "fastq_enabled": "1", "fastq_reads_per_file": "4000", "filename": "imac_ad_umassmed_edu_20181108_fak30311_mn27234_sequencing_run_test_61366", "flowcell_type": "flo-min106", "kit_classification": "none", "local_basecalling": "1", "local_bc_comp_model": "", "local_bc_temp_model": "template_r9.4_450bps_5mer_raw.jsn", "sample_frequency": "4000", "sequencing_kit": "sqk-lsk109", "user_filename_input": "test"}, "segment_type": "albacore-acquisition", "segment_number": 1, "segment_duration": 60, "aggregation": "cumulative", "latest_run_time": 715.6465, "run_id": "557afda1f1ddd31678d0c6378228345cc1b6bfa5", "read_count": 20, "albacore_opts": {"list_workflows": false, "worker_threads": 3, "resume": "", "flowcell": "FLO-MIN106", "kit": "SQK-LSK109", "barcoding": false, "align_ref": null, "config": "r94_450bps_linear.cfg", "debug": false, "recursive": false, "files_per_batch_folder": 4000, "output_format": "fastq", "reads_per_fastq_batch": 1000, "disable_filtering": false, "disable_pings": false, "logfile": "pipeline.log", "summfile": "sequencing_summary.txt", "cfgfile": "configuration.cfg"}, "albacore_analysis_id": "ef7f2902-ce14-48f5-a7c2-a1308777bc53", "reads_per_channel_dist": [{"channel": 8, "count": 1}, {"channel": 261, "count": 2}, {"channel": 16, "count": 1}, {"channel": 240, "count": 1}, {"channel": 58, "count": 1}, {"channel": 223, "count": 1}, {"channel": 203, "count": 1}, {"channel": 343, "count": 1}, {"channel": 349, "count": 1}, {"channel": 75, "count": 1}, {"channel": 331, "count": 1}, {"channel": 213, "count": 1}, {"channel": 290, "count": 1}, {"channel": 165, "count": 1}, {"channel": 323, "count": 1}, {"channel": 166, "count": 1}, {"channel": 414, "count": 1}, {"channel": 406, "count": 1}, {"channel": 195, "count": 1}], "channel_count": 19, "levels_sums": {"open_pore_level_sum": 4351.0945110321045, "count": 20}, "segmentation": {"component_index": 0}, "basecall_1d": {"exit_status_dist": {"pass": 19, "fail:qscore_filter": 1}, "component_index": 1, "seq_len_bases_sum_temp": 79369, "read_len_events_sum_temp": 170220, "qscore_sum_temp": {"sum": 208.063, "count": 20, "mean": 10.40315}, "qscore_dist_temp": [{"mean_qscore": 10.5, "count": 5}, {"mean_qscore": 11.0, "count": 3}, {"mean_qscore": 11.5, "count": 3}, {"mean_qscore": 10.0, "count": 5}, {"mean_qscore": 6.5, "count": 1}, {"mean_qscore": 7.5, "count": 1}, {"mean_qscore": 9.5, "count": 2}], "speed_events_per_second_dist_temp": [{"speed": 799, "count": 18}, {"speed": 800, "count": 2}], "speed_bases_per_second_dist_temp": [{"speed": 330, "count": 1}, {"speed": 296, "count": 1}, {"speed": 358, "count": 1}, {"speed": 350, "count": 1}, {"speed": 470, "count": 1}, {"speed": 376, "count": 1}, {"speed": 430, "count": 1}, {"speed": 314, "count": 1}, {"speed": 282, "count": 1}, {"speed": 402, "count": 1}, {"speed": 326, "count": 1}, {"speed": 392, "count": 1}, {"speed": 384, "count": 1}, {"speed": 398, "count": 1}, {"speed": 372, "count": 1}, {"speed": 400, "count": 1}, {"speed": 480, "count": 1}, {"speed": 322, "count": 1}, {"speed": 382, "count": 1}, {"speed": 396, "count": 1}], "seq_len_events_dist_temp": [{"length": 8000, "count": 3}, {"length": 9000, "count": 2}, {"length": 12000, "count": 2}, {"length": 1000, "count": 3}, {"length": 5000, "count": 2}, {"length": 10000, "count": 1}, {"length": 0, "count": 2}, {"length": 7000, "count": 1}, {"length": 26000, "count": 1}, {"length": 4000, "count": 1}, {"length": 3000, "count": 1}, {"length": 29000, "count": 1}], "seq_len_bases_dist_temp": [{"length": 3000, "count": 6}, {"length": 5000, "count": 3}, {"length": 0, "count": 4}, {"length": 13000, "count": 1}, {"length": 2000, "count": 2}, {"length": 1000, "count": 2}, {"length": 4000, "count": 1}, {"length": 14000, "count": 1}], "strand_median_pa": {"sum": 1736.1313781738281, "count": 20, "mean": 86.8065689086914}, "strand_sd_pa": {"sum": 77.51721835136414, "count": 20, "mean": 3.8758609175682066}}},{"tracking_id": {"asic_id": "484243955", "asic_id_eeprom": "2595130", "asic_temp": "32.509274", "asic_version": "IA02D", "auto_update": "0", "auto_update_source": "https://mirror.oxfordnanoportal.com/software/MinKNOW/", "bream_is_standard": "0", "device_id": "MN27234", "device_type": "minion", "exp_script_name": "d7c38672c0c2d88fce4cc94277787fa3cd2f5bc9-346b21aa2f245c8a22cb68987cd5a2ca66990dad", "exp_script_purpose": "sequencing_run", "exp_start_time": "2018-11-08T19:37:33Z", "flow_cell_id": "FAK30311", "heatsink_temp": "33.031250", "hostname": "imac.ad.umassmed.edu", "installation_type": "nc", "local_firmware_file": "1", "operating_system": "Darwin 17.7.0", "protocol_run_id": "15ba4f35-c665-4e92-bc9a-92e69aff5e97", "protocols_version": "1.15.10.16", "run_id": "557afda1f1ddd31678d0c6378228345cc1b6bfa5", "sample_id": "test", "usb_config": "firm_1.2.3_ware#rbt_4.5.6_rbt#ctrl#USB3", "version": "1.15.4", "msg_id": "3dbabbc1-1bd0-4074-97c9-ec1c7befda05"}, "software": {"name": "albacore-basecalling", "version": "2.3.4", "analysis": "1d_basecalling"}, "context_tags": {"experiment_duration_set": "360", "experiment_type": "lambda_burn_in", "fast5_output_fastq_in_hdf": "1", "fast5_raw": "1", "fast5_reads_per_folder": "4000", "fastq_enabled": "1", "fastq_reads_per_file": "4000", "filename": "imac_ad_umassmed_edu_20181108_fak30311_mn27234_sequencing_run_test_61366", "flowcell_type": "flo-min106", "kit_classification": "none", "local_basecalling": "1", "local_bc_comp_model": "", "local_bc_temp_model": "template_r9.4_450bps_5mer_raw.jsn", "sample_frequency": "4000", "sequencing_kit": "sqk-lsk109", "user_filename_input": "test"}, "segment_type": "albacore-acquisition", "segment_number": 1, "segment_duration": 60, "aggregation": "segment", "latest_run_time": 715.6465, "run_id": "557afda1f1ddd31678d0c6378228345cc1b6bfa5", "read_count": 20, "albacore_opts": {"list_workflows": false, "worker_threads": 3, "resume": "", "flowcell": "FLO-MIN106", "kit": "SQK-LSK109", "barcoding": false, "align_ref": null, "config": "r94_450bps_linear.cfg", "debug": false, "recursive": false, "files_per_batch_folder": 4000, "output_format": "fastq", "reads_per_fastq_batch": 1000, "disable_filtering": false, "disable_pings": false, "logfile": "pipeline.log", "summfile": "sequencing_summary.txt", "cfgfile": "configuration.cfg"}, "albacore_analysis_id": "ef7f2902-ce14-48f5-a7c2-a1308777bc53", "reads_per_channel_dist": [{"channel": 8, "count": 1}, {"channel": 261, "count": 2}, {"channel": 16, "count": 1}, {"channel": 240, "count": 1}, {"channel": 58, "count": 1}, {"channel": 223, "count": 1}, {"channel": 203, "count": 1}, {"channel": 343, "count": 1}, {"channel": 349, "count": 1}, {"channel": 75, "count": 1}, {"channel": 331, "count": 1}, {"channel": 213, "count": 1}, {"channel": 290, "count": 1}, {"channel": 165, "count": 1}, {"channel": 323, "count": 1}, {"channel": 166, "count": 1}, {"channel": 414, "count": 1}, {"channel": 406, "count": 1}, {"channel": 195, "count": 1}], "channel_count": 19, "levels_sums": {"open_pore_level_sum": 4351.0945110321045, "count": 20}, "segmentation": {"component_index": 0}, "basecall_1d": {"exit_status_dist": {"pass": 19, "fail:qscore_filter": 1}, "component_index": 1, "seq_len_bases_sum_temp": 79369, "read_len_events_sum_temp": 170220, "qscore_sum_temp": {"sum": 208.063, "count": 20, "mean": 10.40315}, "qscore_dist_temp": [{"mean_qscore": 10.5, "count": 5}, {"mean_qscore": 11.0, "count": 3}, {"mean_qscore": 11.5, "count": 3}, {"mean_qscore": 10.0, "count": 5}, {"mean_qscore": 6.5, "count": 1}, {"mean_qscore": 7.5, "count": 1}, {"mean_qscore": 9.5, "count": 2}], "speed_events_per_second_dist_temp": [{"speed": 799, "count": 18}, {"speed": 800, "count": 2}], "speed_bases_per_second_dist_temp": [{"speed": 330, "count": 1}, {"speed": 296, "count": 1}, {"speed": 358, "count": 1}, {"speed": 350, "count": 1}, {"speed": 470, "count": 1}, {"speed": 376, "count": 1}, {"speed": 430, "count": 1}, {"speed": 314, "count": 1}, {"speed": 282, "count": 1}, {"speed": 402, "count": 1}, {"speed": 326, "count": 1}, {"speed": 392, "count": 1}, {"speed": 384, "count": 1}, {"speed": 398, "count": 1}, {"speed": 372, "count": 1}, {"speed": 400, "count": 1}, {"speed": 480, "count": 1}, {"speed": 322, "count": 1}, {"speed": 382, "count": 1}, {"speed": 396, "count": 1}], "seq_len_events_dist_temp": [{"length": 8000, "count": 3}, {"length": 9000, "count": 2}, {"length": 12000, "count": 2}, {"length": 1000, "count": 3}, {"length": 5000, "count": 2}, {"length": 10000, "count": 1}, {"length": 0, "count": 2}, {"length": 7000, "count": 1}, {"length": 26000, "count": 1}, {"length": 4000, "count": 1}, {"length": 3000, "count": 1}, {"length": 29000, "count": 1}], "seq_len_bases_dist_temp": [{"length": 3000, "count": 6}, {"length": 5000, "count": 3}, {"length": 0, "count": 4}, {"length": 13000, "count": 1}, {"length": 2000, "count": 2}, {"length": 1000, "count": 2}, {"length": 4000, "count": 1}, {"length": 14000, "count": 1}], "strand_median_pa": {"sum": 1736.1313781738281, "count": 20, "mean": 86.8065689086914}, "strand_sd_pa": {"sum": 77.51721835136414, "count": 20, "mean": 3.8758609175682066}}}]