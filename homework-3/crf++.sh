crf_learn template data/example_datasets_msra/train.txt model >> model_out.txt
crf_test data/example_datasets_msra/test.txt -m model >> output.txt
perl conlleval.pl -d '\t' < output.txt