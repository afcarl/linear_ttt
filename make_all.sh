
#Format: python makejobs.py <experiment_name> <trials>
python makejobs.py naive 30
python makejobs.py "horizontal tiles" 30
python makejobs.py "verticle tiles" 30
python makejobs.py "diagonal tiles" 30
python makejobs.py "all line tiles" 30
python makejobs.py "random 5 tiles" 30
python makejobs.py "random 10 tiles" 30
python makejobs.py "random 16 tiles" 30
python makejobs.py "random 20 tiles" 30
python makejobs.py "random 25 tiles" 30
python makejobs.py "random 30 tiles" 30
python makejobs.py "random 50 tiles" 30
python makejobs.py "kanerva 15 features and 0 threshold" 30
python makejobs.py "kanerva 30 features and 0 threshold" 30
python makejobs.py "kanerva 45 features and 0 threshold" 30
python makejobs.py "kanerva 60 features and 0 threshold" 30
python makejobs.py "kanerva 75 features and 0 threshold" 30
python makejobs.py "kanerva 100 features and 0 threshold" 30
python makejobs.py "kanerva 15 features and 1 threshold" 30
python makejobs.py "kanerva 30 features and 1 threshold" 30
python makejobs.py "kanerva 45 features and 1 threshold" 30
python makejobs.py "kanerva 60 features and 1 threshold" 30
python makejobs.py "kanerva 75 features and 1 threshold" 30
python makejobs.py "kanerva 100 features and 1 threshold" 30
python makejobs.py "kanerva 15 features and 2 threshold" 30
python makejobs.py "kanerva 30 features and 2 threshold" 30
python makejobs.py "kanerva 45 features and 2 threshold" 30
python makejobs.py "kanerva 60 features and 2 threshold" 30
python makejobs.py "kanerva 75 features and 2 threshold" 30
python makejobs.py "kanerva 100 features and 2 threshold" 30
python makejobs.py "kanerva 15 features and 3 threshold" 30
python makejobs.py "kanerva 30 features and 3 threshold" 30
python makejobs.py "kanerva 45 features and 3 threshold" 30
python makejobs.py "kanerva 60 features and 3 threshold" 30
python makejobs.py "kanerva 75 features and 3 threshold" 30
python makejobs.py "kanerva 100 features and 3 threshold" 30

condor_submit naive/jobs
condor_submit horizontal_tiles/jobs
condor_submit verticle_tiles/jobs
condor_submit diagonal_tiles/jobs
condor_submit all_line_tiles/jobs
condor_submit random_5_tiles/jobs
condor_submit random_10_tiles/jobs
condor_submit random_16_tiles/jobs
condor_submit random_20_tiles/jobs
condor_submit random_25_tiles/jobs
condor_submit random_30_tiles/jobs
condor_submit random_50_tiles/jobs
condor_submit kanerva_15_features_and_0_threshold/jobs
condor_submit kanerva_30_features_and_0_threshold/jobs
condor_submit kanerva_45_features_and_0_threshold/jobs
condor_submit kanerva_60_features_and_0_threshold/jobs
condor_submit kanerva_75_features_and_0_threshold/jobs
condor_submit kanerva_100_features_and_0_threshold/jobs
condor_submit kanerva_15_features_and_1_threshold/jobs
condor_submit kanerva_30_features_and_1_threshold/jobs
condor_submit kanerva_45_features_and_1_threshold/jobs
condor_submit kanerva_60_features_and_1_threshold/jobs
condor_submit kanerva_75_features_and_1_threshold/jobs
condor_submit kanerva_100_features_and_1_threshold/jobs
condor_submit kanerva_15_features_and_2_threshold/jobs
condor_submit kanerva_30_features_and_2_threshold/jobs
condor_submit kanerva_45_features_and_2_threshold/jobs
condor_submit kanerva_60_features_and_2_threshold/jobs
condor_submit kanerva_75_features_and_2_threshold/jobs
condor_submit kanerva_100_features_and_2_threshold/jobs
condor_submit kanerva_15_features_and_3_threshold/jobs
condor_submit kanerva_30_features_and_3_threshold/jobs
condor_submit kanerva_45_features_and_3_threshold/jobs
condor_submit kanerva_60_features_and_3_threshold/jobs
condor_submit kanerva_75_features_and_3_threshold/jobs
condor_submit kanerva_100_features_and_3_threshold/jobs
