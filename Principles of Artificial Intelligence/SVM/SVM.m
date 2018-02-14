%������
clear all;
close all;
C = 10;
kertype = 'linear';
%ѵ������
n = 50;
randn('state',6);
x1 = randn(2,n);    %2��N�о���
y1 = ones(1,n);       %1*N��1
x2 = 5+randn(2,n);   %2*N����
y2 = -ones(1,n);      %1*N��-1
 
figure;
plot(x1(1,:),x1(2,:),'bx',x2(1,:),x2(2,:),'k.'); 
axis([-3 8 -3 8]);
hold on;
 
X = [x1,x2];        %ѵ������d*n����nΪ����������dΪ������������
Y = [y1,y2];        %ѵ��Ŀ��1*n����nΪ����������ֵΪ+1��-1
svm = svmTrain(X,Y,kertype,C);
plot(svm.Xsv(1,:),svm.Xsv(2,:),'ro');

%����
[x1,x2] = meshgrid(-2:0.05:7,-2:0.05:7);  %x1��x2����181*181�ľ���
[rows,cols] = size(x1);  
nt = rows*cols;                  
Xt = [reshape(x1,1,nt);reshape(x2,1,nt)];
Yt = ones(1,nt);
result = svmTest(svm, Xt, Yt, kertype);

Yd = reshape(result.Y,rows,cols);
contour(x1,x2,Yd,'m');

