function [ output_args ] = createTree( data)  
    global besttmp
    [m,n] = size(data);  
    classList = data(:,n);  
    classOne = 1;%��¼��һ����ĸ���  
    for i = 2:m  
        if classList(i,:) == classList(1,:)  
            classOne = classOne+1;  
        end  
    end  
      
    % ���ȫ��ͬ  
    if classOne == m  
        disp('final data: ');
        tv=data(1,end);
        disp(tv);  
        return;  
    end  
      
    % ����ȫ������  
    if n == 1  
        disp('final data: ');
        c=unique(data);
        for i=1:length(c)
            ci(i)=length(find(data==c(i)));
        end
        [v,i]=max(ci);
        cv=c(i);
        disp(cv);  
        return;  
    end  
      
    bestFeat = chooseBestFeature(data);  
    besttmp=[besttmp bestFeat];
    disp(['bestFeat: ', num2str(bestFeat)]);  
    featValues = unique(data(:,bestFeat));  
    numOfFeatValue = length(featValues);  
      
    for i = 1:numOfFeatValue
        subtree=splitData(data, bestFeat, featValues(i));
        disp(['select value:',num2str(featValues(i))]);
        createTree(subtree);  
        disp('-------------------------');  
    end  
end  

