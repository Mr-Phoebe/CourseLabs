#!/usr/bin/python
# -*- coding: UTF-8 -*-

## Imports

import sys
from pyspark import SparkConf, SparkContext



## Module Constants
APP_NAME = "My Spark Application"
a_total_documents = None

## Closure Functions

## Main functionality

def task_1to4 (wet_file_name):
    import gzip
    import warc
    import os
    import re
    from collections import Counter


    LOCAL_DIR = '/tmp/'

    if not os.path.exists(LOCAL_DIR):
        os.makedirs(LOCAL_DIR)

    wet_file_name = wet_file_name.replace('/', '_')
    HDFS_EXE = '/root/hadoop/bin/hdfs dfs'
    REG_VALID_WORD = re.compile(r"^[\'\-]*[\"]*[a-zA-Z\'\-]*[\"]*[\'\-]*$") #REG_VALID_WORD

    hdfs_wet_dir = b_hdfs_wet_dir.value
    cmd = HDFS_EXE + ' -get ' + hdfs_wet_dir + '/' +wet_file_name + ' ' + LOCAL_DIR + wet_file_name
    print ('hdfs_get:', cmd)
    os.system(cmd)

    gzip_fobj = gzip.open(LOCAL_DIR + wet_file_name, 'r')
    warc_fobj = warc.WARCFile(fileobj=gzip_fobj, compress=False)

    record = None
    stop_words = b_stop_words.value
    ret = []
    total_doc = 0
    record = warc_fobj.read_record()
    while record:
        if 'WARC-Type' in record \
            and record['WARC-Type'] == 'conversion' \
                and record['Content-Length'] != '0':

            docid = record['WARC-Record-ID']
            payload = record.payload.read()
            tokens = payload.split()
            total_tokens = 0
            mp = {}
            for token in tokens:
                # Step 2
                if REG_VALID_WORD.match(token):
                    # Step 3
                    token = token.strip("\"-\' ")
                    token = token.lower()
                    if len(token):
                        total_tokens += 1
                        # Step 5
                        if token in stop_words:
                            continue
                        if (token, docid) in mp:
                            mp[(token, docid)] += 1
                        else:
                            mp[(token, docid)] = 1
            # Step 4
            if total_tokens > 10:
                total_doc += 1
                ret.extend(mp.items())
        try:
            record = warc_fobj.read_record()
        except:
            pass

    global a_total_documents
    a_total_documents += total_doc
    os.system('rm -rf' + LOCAL_DIR + wet_file_name)
    return ret

if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    sc = SparkContext(conf=conf)

    global a_total_documents
    a_total_documents = sc.accumulator(0)

    CORPUS_PATH = '/processed_corpus'

    hdfs_wet_dir = sys.argv[1]
    wet_path_file = sys.argv[2]
    stop_words_file = sys.argv[3]
    low_freq_threshold = int(sys.argv[4])
    output_dir = sys.argv[5]
    core_count = int(sys.argv[6]) * 4

    stop_words = set()
    paths_list = []
    # Get stop words
    with open(stop_words_file, 'r') as f:
        for line in f:
            stop_words.add(line.strip())

    with open(wet_path_file, 'r') as f:
        for line in f:
            paths_list.append(line.strip())

    print ('stop_words.size() = ', len(stop_words))
    b_stop_words = sc.broadcast(stop_words)
    b_hdfs_wet_dir = sc.broadcast(hdfs_wet_dir)
    b_low_freq_threshold = sc.broadcast(low_freq_threshold)


    paths_rdd = sc.parallelize(paths_list, core_count)
    print ("paths_rdd read done!!")

    # ((token, doc_id), count_per_doc)
    token_docid_count_rdd = paths_rdd.flatMap(task_1to4).repartition(core_count)
    token_docid_count_rdd.persist()
    print ("Enforcement action, ", token_docid_count_rdd.count())
    print ("Total document number is ", a_total_documents.value)

    b_total_documents = sc.broadcast(a_total_documents.value)

    # Get term frequency and document frequency
    # (token, (term_freq, doc_freq))
    tk_tf_df_rdd = token_docid_count_rdd.map(lambda x: (x[0][0], (x[1], 1))).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))

    # Get valid words set
    valid_words_set = set(tk_tf_df_rdd.filter(lambda x: (x[1][1] >= b_low_freq_threshold.value) \
                                                          and ((float(x[1][1]) / b_total_documents.value) < 0.9)).keys().collect())
    b_valid_words_set = sc.broadcast(valid_words_set)

    tk_tf_df_rdd = tk_tf_df_rdd.filter(lambda x: x[0] in b_valid_words_set.value)
    token_docid_count_rdd = token_docid_count_rdd.filter(lambda x: x[0][0] in b_valid_words_set.value)
    # token_docid_count_rdd.persist()

    tk_tf_df_loc = sorted(tk_tf_df_rdd.collect(), key=lambda x: x[0])
    id_word_list = list(map(lambda x: (x, tk_tf_df_loc[x][0]), range(len(tk_tf_df_loc))))

    # Get 'dictionary' file
    word_id_map = {}
    with open(output_dir + 'dictionary', 'w') as f:
        for (id, word) in id_word_list:
            f.write('{0}\t{1}\n'.format(word, id))
            word_id_map[word] = id
    print ('Completed dictionary!')
    b_word_id_map = sc.broadcast(word_id_map)

    # Get 'frequency' file
    tf_sum = 0
    with open(output_dir + 'frequency', 'w') as f:
        for e in tk_tf_df_loc:
            tf_sum += e[1][0]
            f.write('{0}\t{1}\t{2}\n'.format(e[0], e[1][0], e[1][1]))
    print ('Completed frequency!')

    # (doc_id, (corpus, total_len))
    doc_corpus_len_rdd = token_docid_count_rdd.map(lambda x: (x[0][1], ("{0}:{1}".format(b_word_id_map.value[x[0][0]], x[1]), x[1])))\
                                                .reduceByKey(lambda x, y: ('\t'.join([x[0], y[0]]), x[1] + y[1]))

    doclen_list = sorted(doc_corpus_len_rdd.map(lambda x: x[1][1]).collect())
    number_of_words = len(word_id_map)
    number_of_documents = len(doclen_list)
    number_of_tokens = tf_sum

    print ('words, doc, token', number_of_words, number_of_documents, number_of_tokens)

    max_doclen = doclen_list[-1]
    min_doclen = doclen_list[0]
    avg_doclen = int(sum(doclen_list) / float(len(doclen_list)))
    print ('max', max_doclen, 'min', min_doclen, 'avg', avg_doclen)

    # Get 'statistics' file
    with open(output_dir + 'statistics', 'w') as f:
        f.write('Number of Words: {0}\n'.format(number_of_words))
        f.write('Number of Documents: {0}\n'.format(number_of_documents))
        f.write('Number of Tokens: {0}\n'.format(number_of_tokens))
        f.write('Maximum Document Length: {0}\n'.format(max_doclen))
        f.write('Minimum Document Length: {0}\n'.format(min_doclen))
        f.write('Average Document Length: {0}\n'.format(avg_doclen))
        f.write('Document Length 10th percentile: {0}\n'.format(doclen_list[int(number_of_documents * 0.1)]))
        f.write('Document Length 30th percentile: {0}\n'.format(doclen_list[int(number_of_documents * 0.3)]))
        f.write('Document Length 50th percentile: {0}\n'.format(doclen_list[int(number_of_documents * 0.5)]))
        f.write('Document Length 70th percentile: {0}\n'.format(doclen_list[int(number_of_documents * 0.7)]))
        f.write('Document Length 90th percentile: {0}\n'.format(doclen_list[int(number_of_documents * 0.9)]))
        f.write('Document Length 99th percentile: {0}\n'.format(doclen_list[int(number_of_documents * 0.99)]))
    print ('Completed statistics!')

    # Get Corpus
    doc_corpus_len_rdd.map(lambda x: (None, x[1][0])) \
        .saveAsHadoopFile(CORPUS_PATH, 'org.apache.hadoop.mapred.TextOutputFormat')
    print ('Completed Corpus!')