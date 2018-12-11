# Income Prediction Report

Name: Haonan Wu
Number: N18859539

## 1 Machine Learning Model

1. Gradient Boosting Decision Tree
	- [Paper](http://statweb.stanford.edu/~jhf/ftp/stobst.pdf)
	- It features high efficiency and built-in mechanisms to handle categorical features and missing values.
	- It can handle non-linear transformation and feature crossing.
	- package: LightGBM
2. Linear Regression
	- package: sklearn 

## 2 Feature Engineering

### 2.1 idnum

While id is used to identify the records, so it makes no sense to the model.

While training the model, we will remove the id column.

### 2.2 age

We will remove the records whose age is less than 16.

### 2.3 workerclass

1. For the records with age equalling 16, I set their workerclass as "0" so that the model can tell the difference between these records and other "N/A". Because records with age equalling 16 is special for this feature, they have different meaning for other "N/A".
2. I apply one-hot encoding for this feature.

### 2.4 interestincome

Do nothing.

### 2.5 traveltimetowork & workarrivaltime

#### 2.5.1 workarrivaltime

Change workarrivaltime from categorical data to numerical float data.

- Using the centrial time of a range to represent this range.
	- For example, **12:02.5 A.M.** represents **12:00 A.M.** to **12:04 A.M.**.
- Using from a minute to **12:00 A.M.** to represents this minute.
	- For example, **2.5** represents **12:02.5 A.M.**.

#### 2.5.2 arrivalhour & arrival minute

Extract hours and minutes of workarrivaltime as two new numerical features.

#### 2.5.3 departure time

Use numerical workarrivaltime minus traveltimetowork. So that I get the departure time as a new numerical feature.

#### 2.5.4 has job

For the records with workclass equalling '?' and workarrivaltime equalling '?', I thing these records  didn't have job.

So I use a new feature to figure out whether this record has job or not.

#### 2.5.5 special case

For the records with workclass from '6' to '9', if their traveltimetowork or workarrivaltime is '?', I set them to 0.

### 2.6 vechicleoccupancy

Set every '?' to '0'.

Dupicate this feature, ans mark one of them as categorical feature, and the other as numerical feature.

### 2.7 meansoftransport

1. For the records with age equalling 16, I set their meansoftransport as "0" so that the model can tell the difference between these records and other "N/A". Because records with age equalling 16 is special for this feature, they have different meaning for other "N/A".
2. I apply one-hot encoding for this feature.

### 2.8 marital

Dupicate this feature, ans mark one of them as categorical feature, and the other as numerical feature.

### 2.9 schoolenrollment

Remap the feature.

Using two categorical features, join school and private school, instead of original feature.

Map 1(No, has not attended in the last 3 months) as join school = 0, private school = '2'

Map 2(Yes, public school or public college) as join school = 1, private school = '0'

Map 3(Yes, private school or college or home school) as join school = 1, private school = '1'

### 2.10 educationalattain

Dupicate this feature, ans mark one of them as categorical feature, and the other as numerical feature.

### 2.11 sex

Do nothing.

### 2.12 hoursworkperweek

Set '?' to '0'.

### 2.13 ancestryofparent

Apply **entity embeddings** in this feature.

### 2.14 degreefield

Fill the N/A data with "0000".

Apply **entity embeddings** in this feature.

#### 2.14.1 major

Extract the first two digits in degreefield to form a new categorical feature.

This feature represents the major of degree.

1100 GENERAL AGRICULTURE
1101 AGRICULTURE PRODUCTION AND MANAGEMENT
1102 AGRICULTURAL ECONOMICS
1103 ANIMAL SCIENCES
1104 FOOD SCIENCE
1105 PLANT SCIENCE AND AGRONOMY
1106 SOIL SCIENCE
1199 MISCELLANEOUS AGRICULTURE



1301 ENVIRONMENTAL SCIENCE
1302 FORESTRY
1303 NATURAL RESOURCES MANAGEMENT

We can notice that the first two digits of this feature represents more general field of the degree.

#### 2.14.2 miscellaneous

Add a new categorical feature.

If the last two digits equals to '99', this field is miscellaneous.

### 2.15 industryworkedin

Apply **entity embeddings** in this feature.

## 3 General Methods

### 3.1 Fill N/A numerical

Use the mean of other records to fill N/A.

### 3.2 Fill N/A categorical

For GBDT, the algorithm can handle the missing value automatically.

For linear regression, I fill these data with None.

### 3.3 Categorical Encoding

For different features, I use different methods to handle the encoding.

See the feature engineer for detail.

#### 3.3.1 One-hot Encoding

If the percentage frequency of a feature is smaller than a threshold, it will be transformed to a special value "Other".

For example, if we set the threshold 

|index|feature|
|:-:|:-:|
|0 | a|
|		1 | b|
|		2 | c|
|		3 | a|
|		4 | a|

will become

|index | feature\_is\_a |feature\_is\_other|
|:-:|:-:|:-:|
|0 | 1 | 0|
|		1 | 0 | 1|
|		2 | 0 | 1|
|		3 | 1 | 0|
|		4 | 1 | 0|

For each of these features, I simply apply 0.01 as threshold.

#### 3.3.2 Entity embedding

Entity embedding is learned by a neural network during the standard supervised training process. It can automatically learn the representation of categorical features in multi-dimensional spaces which puts values with similar effect to the target output value close to each other helping supervised training process to solve the problem.

#### 3.4 Feature Selection

Use varianceThreshold feature selection. It removes all features whose variance doesn’t meet some threshold.

## 4 Algorithm parameters

This parameters are gotten by automatic tuning tool MLBox which is called auto ML.

I assign the range of each parameters, and the tool will get the best parameters for me. 

### 4.1 GBDT

|parameter|value|
|:-:|:---:|
|learning_rate|0.001465943212346882|
|reg_alpha|1.8259818986702054|
|subsample|0.7490322499428315|
|colsample_bytree|0.8325100801548346| 
|n_estimators'|2100|
|reg_lambda| 0.985719052366061|
|max_depth'|6|
|fs__threshold|0.21609601827598018|

### 4.2 Linear Regression

No parameters.

## 5 Cross Validation Result

I use 3 folds to do cross validation.

### 5.1 GBDT

fold 1 = 49855.33580996014
fold 2 = 55278.94517651645
fold 3 = 64883.30948273477

### 5.2 Linear Regression

fold 1 = 57784.091439073265
fold 2 = 56887.66277338695
fold 3 = 70749.11970681962

