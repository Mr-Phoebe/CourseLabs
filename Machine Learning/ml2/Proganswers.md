# Proganswers

Name: Haonan Wu
Number: N18859539

## a

### i

The class is 1.

### ii

| correct| predicted | predicted |
|:--:|:-:|:-:|
| | 1 | 0 |
|1  | 209 | 64|
|0  |134 |93 |

### iii

Accuracy = $60.4\%$
True positive rate = $60.9\%$
False positive rate = $40.7\%$


### iv

The class is 1.

### v

| correct| predicted | predicted |
|:--:|:-:|:-:|
| | 1 | 0 |
|1  | 212 | 61|
|0  |136 |91 |

### vi

Accuracy = $60.6\%$
True positive rate = $60.9\%$
False positive rate = $40.1\%$

### vii

Accuracy = $60.6\%$

### viii

| correct| predicted | predicted |
|:--:|:-:|:-:|
| | 1 | 0 |
|1  | 273 | 0|
|0  |227 |0 |


## b

The distance function is based on key words. But not the meaning of the real sentences.

So it the tokens' number is pretty large. It is more likely that the commend sentences have different meanings but have similar key words.

So the classification result will become worse.

## c

### i

| k| Accuracy |
|:--:|:-:|
| 3| 0.660 |
|7 | 0.658 |
|99|0.612 |

### ii

| correct| predicted | predicted |
|:--:|:-:|:-:|
| | 1 | 0 |
|1  | 212 | 61|
|0  |144 |83 |

Accuracy = $59\%$


## d

### i

We can use Jaccard Distance:

$$J(X, Y) = 1 - {|X\bigcap Y| \over |X\bigcup Y|}$$

X and Y are the sets of tokens.

### ii 

Because it take the joins of sets into consideration. The distance will be more reasonable while be used to manage the similarity of two sets.

### iii

| correct| predicted | predicted |
|:--:|:-:|:-:|
| | 1 | 0 |
|1  | 206 | 67|
|0  |112 |115 |


### iv

Accuracy = $63.6\%$
True positive rate = $64.8\%$
False positive rate = $36.8\%$

### iii

| correct| predicted | predicted |
|:--:|:-:|:-:|
| | 1 | 0 |
|1  | 220 | 53|
|0  |113 |114 |


### iv

Accuracy = $66.6\%$
True positive rate = $66.1\%$
False positive rate = $31.7\%$

### v

Yes. My distance function is better than first distance function.


