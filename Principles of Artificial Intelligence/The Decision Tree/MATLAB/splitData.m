function [ subSet ] = splitData( data, axis, value )  
    [m,n] = size(data);%�õ����������ݵĴ�С  
      
    subSet = data;  
    subSet(:,axis) = [];  
    k = 0;  
    for i = 1:m  
        if data(i,axis) ~= value  
            subSet(i-k,:) = [];  
            k = k+1;  
        end  
    end     
end  