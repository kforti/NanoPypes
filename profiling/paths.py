from pathlib import PosixPath


PATHS = {'run6': ['/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/37', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1114', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/131', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/19', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/503', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/487', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/510', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/382', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/198', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/525', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/156', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/491', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/441', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/280', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/204', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/402', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1013', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/17', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/46', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/132', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1104', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/334', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/183', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/161', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/103', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1108', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/366', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/228', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/267', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/195', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/515', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1087', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/468', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/164', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/300', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1098', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/444', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1065', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/291', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1092', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/370', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/484', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1012', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/144', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/113', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/116', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/225', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/235', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/234', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1110'], 'run1': ['/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/37', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1114', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/131', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/19', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/503'], 'run2': ['/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/37', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1114', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/131', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/19', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/503', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/487', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/510', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/382', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/198', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/525'], 'run3': ['/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/37', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1114', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/131', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/19', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/503', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/487', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/510', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/382', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/198', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/525', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/156', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/491', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/441', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/280', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/204', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/402', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1013', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/17', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/46', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/132'], 'run5': ['/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/37', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1114', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/131', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/19', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/503', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/487', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/510', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/382', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/198', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/525', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/156', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/491', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/441', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/280', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/204', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/402', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1013', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/17', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/46', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/132', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1104', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/334', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/183', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/161', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/103', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1108', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/366', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/228', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/267', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/195', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/515', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1087', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/468', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/164', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/300', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1098', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/444', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1065', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/291', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1092'], 'run4': ['/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/37', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1114', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/131', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/19', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/503', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/487', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/510', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/382', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/198', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/525', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/156', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/491', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/441', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/280', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/204', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/402', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1013', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/17', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/46', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/132', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1104', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/334', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/183', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/161', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/103', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/1108', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/366', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/228', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/267', '/project/umw_athma_pai/raw/minion/20190220_1525_ERCC/fast5/pass/195']}

    #{'run6': [PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/37'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1114'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/131'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/19'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/503'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/487'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/510'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/382'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/198'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/525'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/156'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/491'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/441'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/280'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/204'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/402'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1013'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/17'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/46'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/132'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1104'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/334'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/183'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/161'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/103'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1108'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/366'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/228'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/267'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/195'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/515'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1087'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/468'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/164'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/300'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1098'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/444'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1065'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/291'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1092'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/370'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/484'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1012'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/144'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/113'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/116'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/225'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/235'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/234'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1110')], 'run1': [PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/37'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1114'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/131'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/19'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/503')], 'run2': [PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/37'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1114'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/131'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/19'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/503'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/487'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/510'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/382'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/198'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/525')], 'run3': [PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/37'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1114'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/131'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/19'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/503'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/487'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/510'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/382'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/198'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/525'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/156'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/491'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/441'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/280'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/204'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/402'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1013'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/17'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/46'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/132')], 'run5': [PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/37'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1114'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/131'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/19'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/503'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/487'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/510'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/382'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/198'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/525'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/156'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/491'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/441'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/280'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/204'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/402'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1013'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/17'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/46'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/132'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1104'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/334'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/183'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/161'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/103'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1108'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/366'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/228'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/267'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/195'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/515'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1087'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/468'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/164'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/300'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1098'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/444'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1065'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/291'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1092')], 'run4': [PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/37'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1114'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/131'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/19'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/503'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/487'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/510'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/382'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/198'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/525'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/156'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/491'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/441'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/280'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/204'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/402'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1013'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/17'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/46'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/132'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1104'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/334'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/183'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/161'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/103'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/1108'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/366'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/228'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/267'), PosixPath('/project/umw_athma_pai/kevin/data/minion_ercc_labeled/20190220_1525_ERCC/fast5/pass/195')]}
