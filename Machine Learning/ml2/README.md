README

1. For the program, I split the positive and negative test data into two files which make the computation for confusion matrix easier.

2. Considering the loss of accuracy, I apply reciprocal of distance rather than normal distance in the program. So I will find the largest value from reciprocals of distances.

3. To apply the new distance rule, change the distance parameter in KNearestNeighbor.train to 1.