data_path=$1
names_file=$2
stop_words_file=$3
low_freq_threshold=$4
core_count=$5
output_directory=$6

echo $data_path
echo $names_file
echo $stop_words_file
echo $low_freq_threshold
echo $core_count
echo $output_directory

BASEDIR=$(dirname "$0")
code_path=${BASEDIR}/driver.py
echo "$code_path"

/root/spark/bin/spark-submit --conf spark.driver.maxResultSize=32G --driver-memory 10G --executor-memory 10G --driver-cores $core_count $code_path $data_path $names_file $stop_words_file $low_freq_threshold $output_directory $core_count
