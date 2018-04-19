#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <assert.h>
#include <sys/time.h>

#define NUM_BUCKETS 5     // Buckets in hash table
#define NUM_KEYS 100000   // Number of keys inserted per thread
int num_threads = 1;      // Number of threads (configurable)
int keys[NUM_KEYS];

// Part 1
pthread_mutex_t lock;
// Part 4
pthread_mutex_t mutexTable[NUM_BUCKETS];

typedef struct _bucket_entry {
    int key;
    int val;
    struct _bucket_entry *next;
} bucket_entry;

bucket_entry *table[NUM_BUCKETS];

void panic(char *msg) {
    printf("%s\n", msg);
    exit(1);
}

double now() {
    struct timeval tv;
    gettimeofday(&tv, 0);
    return tv.tv_sec + tv.tv_usec / 1000000.0;
}

// Inserts a key-value pair into the table
void insert(int key, int val) {
    int i = key % NUM_BUCKETS;

    bucket_entry *e = (bucket_entry *) malloc(sizeof(bucket_entry));
    if (!e) panic("No memory to allocate bucket!");

    pthread_mutex_lock(&mutexTable[i]);
    e->next = table[i];
    e->key = key;
    e->val = val;
    table[i] = e;
    pthread_mutex_unlock(&mutexTable[i]);
}

// Retrieves an entry from the hash table by key
// Returns NULL if the key isn't found in the table
bucket_entry * retrieve(int key) {
    bucket_entry *b;
    for (b = table[key % NUM_BUCKETS]; b != NULL; b = b->next) {
        if (b->key == key) return b;
    }
    return NULL;
}

void * put_phase(void *arg) {
    long tid = (long) arg;
    int key = 0;

    // If there are k threads, thread i inserts
    //      (i, i), (i+k, i), (i+k*2)
    for (key = tid ; key < NUM_KEYS; key += num_threads) {
        //pthread_mutex_lock(&lock);
        insert(keys[key], tid);
        //pthread_mutex_unlock(&lock);
    }

    pthread_exit(NULL);
}

void * get_phase(void *arg) {
    long tid = (long) arg;
    int key = 0;
    long lost = 0;

    for (key = tid ; key < NUM_KEYS; key += num_threads) {
        if (retrieve(keys[key]) == NULL) lost++;
    }
    printf("[thread %ld] %ld keys lost!\n", tid, lost);

    pthread_exit((void *)lost);
}

int main(int argc, char **argv) {
    long i;
    pthread_t *threads;
    double start, end;

    if (argc != 2) {
        panic("usage: ./parallel_hashtable <num_threads>");
    }
    if ((num_threads = atoi(argv[1])) <= 0) {
        panic("must enter a valid number of threads to run");
    }

    srandom(time(NULL));
    for (i = 0; i < NUM_KEYS; i++)
        keys[i] = random();

    //initialize mutexes
    for(i = 0; i < NUM_BUCKETS; i++){
    	pthread_mutex_init(&mutexTable[i], NULL);
    }

    // Initiatize the lock
    pthread_mutex_init(&lock, NULL);

    threads = (pthread_t *) malloc(sizeof(pthread_t)*num_threads);
    if (!threads) {
        panic("out of memory allocating thread handles");
    }

    // Insert keys in parallel
    start = now();
    for (i = 0; i < num_threads; i++) {
        pthread_create(&threads[i], NULL, put_phase, (void *)i);
    }
    
    // Barrier
    for (i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }
    end = now();
    
    printf("[main] Inserted %d keys in %f seconds\n", NUM_KEYS, end - start);
    
    // Reset the thread array
    memset(threads, 0, sizeof(pthread_t)*num_threads);

    // Retrieve keys in parallel
    start = now();
    for (i = 0; i < num_threads; i++) {
        pthread_create(&threads[i], NULL, get_phase, (void *)i);
    }

    // Collect count of lost keys
    long total_lost = 0;
    long *lost_keys = (long *) malloc(sizeof(long) * num_threads);
    for (i = 0; i < num_threads; i++) {
        pthread_join(threads[i], (void **)&lost_keys[i]);
        total_lost += lost_keys[i];
    }
    end = now();

    printf("[main] Retrieved %ld/%d keys in %f seconds\n", NUM_KEYS - total_lost, NUM_KEYS, end - start);

    return 0;
}


/*
Part 2: 
I do see a change in timing.
In some cases, mutex performs better than spin. 
Because it's better to put threads to sleep and swap immediately rather than to 
keep waiting until it gets released.  
At another point, around say 100 threads, the overhead of swaping might cost more 
time, which might explain why the time starts to go up again.

Mutex:   1 Threads = 10.8073 sec; 2 Threads = 6.4022 sec; 8 Threads = 3.5965 sec; 20 Threads = 3.3657 sec; 100 Threads = 5.0989 sec
Spinlock:1 Threads = 11.2287 sec; 2 Threads = 9.9378 sec; 8 Threads = 3.6722 sec; 20 Threads = 3.4111 sec; 100 Threads = 4.3071 sec

Part 3: 
Retrieving an item from the hash table does not require a lock. 
I thought it would because the unmodified program shows keys lost 
in the retrieval phase, but the truth appears to be that the insert 
is failing due to race conditions. Further evidence that supports 
this is that when I implemented the locks and mutexes, I only did so 
for the insertion part of the program. The retrieval still runs in 
parallel, and no keys are lost. I wonder if maybe that's because 
everything is done in more of less one step for the retrieval 
so no race conditions can occur.

*/