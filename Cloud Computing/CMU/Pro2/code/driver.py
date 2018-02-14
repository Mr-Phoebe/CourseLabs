#!/usr/bin/python
# -*- coding: UTF-8 -*-

## Imports

import sys
from pyspark import SparkConf, SparkContext



## Module Constants
APP_NAME = "My Spark Application"


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
    REG_VALID_WORD = re.compile(r'''^[\'\-]*["]*[a-zA-Z\'\-]*["]*[\'\-]*$''') #REG_VALID_WORD
    REG_NORM_WORD = re.compile(r'''^[^a-zA-z]*|[^a-zA-Z]*$''')               #REG_NORM_WORD

    hdfs_wet_dir = b_hdfs_wet_dir.value
    cmd = HDFS_EXE + ' -get ' + hdfs_wet_dir + '/' +wet_file_name + ' ' + LOCAL_DIR + wet_file_name
    print ('hdfs_get:', cmd)
    os.system(cmd)

    gzip_fobj = gzip.open(LOCAL_DIR + wet_file_name, 'r')
    warc_fobj = warc.WARCFile(fileobj=gzip_fobj, compress=False)

    record = None
    stop_words = b_stop_words.value
    ret = []

    def processSingleToken(token, doc_id):                      #processSingleToken(token,doc_id)
        # 2. Drop all invalid English Words
        if REG_VALID_WORD.match(token) == None:
            return None
        # 3. Standardize valid tokens
        token = REG_NORM_WORD.sub('', token)
        token = token.lower()
        if len(token):
            return (token, doc_id)
        else:
            return None

    record = warc_fobj.read_record()
    while record:
        if 'WARC-Type' in record \
            and record['WARC-Type'] == 'conversion' \
                and record['Content-Length'] != '0':

            docid = record['WARC-Record-ID']
            payload = record.payload.read()
            tokens = payload.split()
            token_id_pairs = [processSingleToken(x, docid) for x in tokens]
            token_id_pairs = filter(None, token_id_pairs)
            if len(token_id_pairs) > 10:
                # 5.1 Remove stop words
                token_id_pairs = [x for x in token_id_pairs if x[0] not in stop_words]
                token_id_count_pairs = Counter(token_id_pairs).items()
                ret.extend(token_id_count_pairs)
        try:
            record = warc_fobj.read_record()
        except:
            pass

    os.system('rm -rf' + LOCAL_DIR + wet_file_name)
    return ret
                                                         #filterDfInvalidTokens
def filterDfInvalidTokens(element):
    # element: (token, doc_freq)
    freq = element[1]
    doc_number = bd_doc_number.value
    threshold = b_low_freq_threshold.value
    if freq >= threshold and float(freq) / doc_number < 0.9:
        return False
    return True

if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    sc = SparkContext(conf=conf)

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
    f.close()

    with open(wet_path_file, 'r') as f:
        for line in f:
            paths_list.append(line.strip())
    f.close()

    print ('stop_words.size() = ', len(stop_words))
    b_stop_words = sc.broadcast(stop_words)
    b_hdfs_wet_dir = sc.broadcast(hdfs_wet_dir)
    b_low_freq_threshold = sc.broadcast(low_freq_threshold)


    paths_rdd = sc.parallelize(paths_list, core_count)
    print ("paths_rdd read done!!")
    token_docid_count_pairs = paths_rdd.flatMap(task_1to4).repartition(core_count)
    token_docid_count_pairs.persist()

    # Get document frequency
    tk_df_pairs = token_docid_count_pairs.map(lambda x: (x[0][0], 1)).reduceByKey(lambda x, y: x + y).collect()

    # Get total document number
    doc_number = token_docid_count_pairs.map(lambda x: (x[0][1], 1)).reduceByKey(lambda x, y: 1).count()
    bd_doc_number = sc.broadcast(doc_number)

    # Get step 56 invalid words
    invalid_words = set(dict(filter(filterDfInvalidTokens, tk_df_pairs)).keys())      #df_invalid_tokens
    b_invalid_words = sc.broadcast(invalid_words)    #b_df_invalid_tokens

    # Get tokens after step 56
    token_docid_count_pairs = token_docid_count_pairs.filter(lambda x: x[0][0] not in b_invalid_words.value).repartition(core_count)
    token_docid_count_pairs.persist()

    # Get term frequency
    term_freq_pairs = dict(token_docid_count_pairs.map(lambda x: (x[0][0], x[1])).reduceByKey(lambda x, y: x + y).collect())
    # Get final doc frequency
    doc_freq_pairs = dict(filter(lambda x: x[0] not in invalid_words, tk_df_pairs))

    print '-----term_freq------done!'
    print len(term_freq_pairs)
    print '-----term_freq------end'

    print '\n'

    print '-----doc_freq-------begin'
    print len(doc_freq_pairs)
    print '-----doc_freq-------done!'

    print '\n'

    # Get Number of Words
    number_of_words = len(doc_freq_pairs)
    # Get Number of Documents
    number_of_documents = token_docid_count_pairs.map(lambda x: (x[0][1], 1)).reduceByKey(lambda x, y: 1).count()
    # Get Number of Tokens
    number_of_tokens = token_docid_count_pairs.map(lambda x: x[1]).sum()

    print ('words, doc, token', number_of_words, number_of_documents, number_of_tokens)

    # Get Document Length
    doclen_list = token_docid_count_pairs.map(lambda x: (x[0][1], x[1]))\
                                    .reduceByKey(lambda x, y: x+y)\
                                    .values().collect()
    doclen_list.sort()
    print ('doclen_list:', len(doclen_list), type(doclen_list))

    max_doclen = doclen_list[-1]
    min_doclen = doclen_list[0]
    avg_doclen = int(sum(doclen_list) / float(len(doclen_list)))
    print ('max', max_doclen, 'min', min_doclen, 'avg', avg_doclen)

    words = term_freq_pairs.keys()
    words.sort()
    id_word_list = list(map(lambda x: (x, words[x]), range(len(words))))

    # I/O
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
    f.close()
    print ('Completed statistics!')

    # Get 'dictionary' file
    word_id_map = {}
    with open(output_dir + 'dictionary', 'w') as f:
        for (id, word) in id_word_list:
            f.write('{0}\t{1}\n'.format(word, id))
            word_id_map[word] = id
    print ('Completed dictionary!')

    b_word_id_map = sc.broadcast(word_id_map)

    with open(output_dir + 'frequency', 'w') as f:
        for (id, word) in id_word_list:
            f.write('{0}\t{1}\t{2}\n'.format(word, term_freq_pairs[word], doc_freq_pairs[word]))
    print ('Completed frequency!')

    # Get Corpus
    docid_wordandfreq_pairs = token_docid_count_pairs.map(lambda x: (x[0][1], '{0}:{1}'.format(b_word_id_map.value[x[0][0]], x[1])))\
                                .reduceByKey(lambda x, y: x + '\t'+ y)\
                                .map(lambda x: (None, x[1]))\
                                .saveAsHadoopFile(CORPUS_PATH, 'org.apache.hadoop.mapred.TextOutputFormat')
    print ('Completed Corpus!')

