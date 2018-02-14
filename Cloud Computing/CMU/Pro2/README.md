# Performance optimization for Apache Spark programs


We provide you with an automated tool named [spark-ec2-setup](https://github.com/CloudComputingCourse/spark-ec2-setup) that is able to launch and manage Spark clusters on AWS EC2. 

The `setup.sh` is my setup shell script.

---

We provide you with a script `get_WARC_dataset.sh` in the [starter package](https://github.com/CloudComputingCourse/719-p2-starter) to help download WET files and store them to HDFS. 

This script takes one parameter, which indicates how many files at the top of the path files should be downloaded. For example, if you want to download the first 50 files, you can use:

```
./get_WARC_dataset.sh 50
```

---

The `run.sh` in code folder.

- <data-path\>: path to a directory in the HDFS that stores the WET files to be;
- <names-file\>: path to a local file that contains the list of WET file names (one file per line) for you to process. Those files are stored under the <data-path\>;
- <stop-words-file\>: the path to a local file that contains the list of general stop words (one word per line). You may assume it contains less than 200 words;
- <low-freq-threshold\>: the low_freq threshold, a word should be removed if its document frequency is below this threshold;
- <core-count\>: total number of cores of all slave instances;
- <output-directory\>: the local directory to output your the computed statistics results. Please make sure your file names and format match the given reference output otherwise autograding could fail.