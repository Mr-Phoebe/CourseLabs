%% ѡ����Ϣ������������  
function [ bestFeature ] = chooseBestFeature( data )  
global bestFeat
    [m,n] = size(data);% �õ����ݼ��Ĵ�С  
      
    % ͳ�������ĸ���  
    numOfFeatures = n-1;%���һ�������  
    % ԭʼ����  
    baseEntropy = calEntropy(data);  
      
    bestInfoGain = 0;%��ʼ����Ϣ����  
    bestFeature = 0;% ��ʼ����ѵ�����λ  
      
    % ��ѡ��ѵ�����λ  
    for j = 1:numOfFeatures  
        featureTemp = unique(data(:,j));  
        numF = length(featureTemp);%���Եĸ���  
        newEntropy = 0;%����֮�����  
        for i = 1:numF  
            subSet = splitData(data, j, featureTemp(i,:));  
            [m_1, n_1] = size(subSet);  
            prob = m_1./m;  
            newEntropy = newEntropy + prob * calEntropy(subSet);  
        end  
          
        %��������  
        infoGain = baseEntropy - newEntropy;  
          
        if infoGain > bestInfoGain  
            bestInfoGain = infoGain;  
            bestFeature = j;  
        end  
    end  
end  