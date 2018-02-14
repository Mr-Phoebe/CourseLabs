#! /bin/bash
KEY_ID="my-key-pair"
IDENTITY="/Users/Phoebe/Documents/my-key-pair.pem"
./spark-ec2-setup/spark-ec2 \
-k $KEY_ID \
-i $IDENTITY \
-t m4.xlarge \
-s 4 \
-a ami-6d15ec7b \
--ebs-vol-size=200 \
--ebs-vol-num=1 \
--ebs-vol-type=gp2 \
--spot-price=10 \
--additional-tags="Project:15719.p2" \
launch SparkCluster
