#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <cmath>
using namespace std;
#define MAXLEN 6//����ÿ�е����ݸ���

/*
�������ʵ��
1 �����
2 ��ָ���ʾ�������ھ����Ҹ�����Ӧ��
3 ��Ů����ʾ�������ھ������ӽ���Ӧ��
4 ���ӣ����ֵܱ�ʾ��,ʵ�ֱȽ��鷳
5 ÿ���������к�����vector����
��ѵ:���ݽṹ����ƺ���Ҫ�����㷨����5�ȽϺ��ʣ�ͬʱ
ע��ά��ʣ��������ʣ��������Ϣ������ʱ���������ѭ�����Ե�ֵ��
����������ݹ����
*/
vector <vector <string> > state;//ʵ����
vector <string> item(MAXLEN);//��Ӧһ��ʵ����
vector <string> attribute_row;//�������м�����������
string end("end");//�������
string yes("yes");
string no("no");
string blank("");
map<string,vector < string > > map_attribute_values;//�洢���Զ�Ӧ�����е�ֵ
int tree_size = 0;
struct Node{//�������ڵ�
    string attribute;//����ֵ
    string arrived_value;//���������ֵ
    vector<Node *> childs;//���еĺ���
    Node(){
        attribute = blank;
        arrived_value = blank;
    }
};
Node * root;

//��������ʵ������������ֵ��ɵ�map
void ComputeMapFrom2DVector(){
    unsigned int i,j,k;
    bool exited = false;
    vector<string> values;
    for(i = 1; i < MAXLEN-1; i++){//�����б���
        for (j = 1; j < state.size(); j++){
            for (k = 0; k < values.size(); k++){
                if(!values[k].compare(state[j][i])) exited = true;
            }
            if(!exited){
                values.push_back(state[j][i]);//ע��Vector�Ĳ��붼�Ǵ�ǰ�����ģ�ע�����it��ʼ��ָ��vectorͷ
            }
            exited = false;
        }
        map_attribute_values[state[0][i]] = values;
        values.erase(values.begin(), values.end());
    }
}

//���ݾ������Ժ�ֵ��������
double ComputeEntropy(vector <vector <string> > remain_state, string attribute, string value,bool ifparent){
    vector<int> count (2,0);
    unsigned int i,j;
    bool done_flag = false;//�ڱ�ֵ
    for(j = 1; j < MAXLEN; j++){
        if(done_flag) break;
        if(!attribute_row[j].compare(attribute)){
            for(i = 1; i < remain_state.size(); i++){
                if((!ifparent&&!remain_state[i][j].compare(value)) || ifparent){//ifparent��¼�Ƿ��㸸�ڵ�
                    if(!remain_state[i][MAXLEN - 1].compare(yes)){
                        count[0]++;
                    }
                    else count[1]++;
                }
            }
            done_flag = true;
        }
    }
    if(count[0] == 0 || count[1] == 0 ) return 0;//ȫ������ʵ�����߸�ʵ��
    //��������� ����[+count[0],-count[1]],log2Ϊ��ͨ�����׹�ʽ������Ȼ������
    double sum = count[0] + count[1];
    double entropy = -count[0]/sum*log(count[0]/sum)/log(2.0) - count[1]/sum*log(count[1]/sum)/log(2.0);
    return entropy;
}

//���㰴������attribute���ֵ�ǰʣ��ʵ������Ϣ����
double ComputeGain(vector <vector <string> > remain_state, string attribute){
    unsigned int j,k,m;
    //������������ʱ����
    double parent_entropy = ComputeEntropy(remain_state, attribute, blank, true);
    double children_entropy = 0;
    //Ȼ���������ֺ����ֵ����
    vector<string> values = map_attribute_values[attribute];
    vector<double> ratio;
    vector<int> count_values;
    int tempint;
    for(m = 0; m < values.size(); m++){
        tempint = 0;
        for(k = 1; k < MAXLEN - 1; k++){
            if(!attribute_row[k].compare(attribute)){
                for(j = 1; j < remain_state.size(); j++){
                    if(!remain_state[j][k].compare(values[m])){
                        tempint++;
                    }
                }
            }
        }
        count_values.push_back(tempint);
    }

    for(j = 0; j < values.size(); j++){
        ratio.push_back((double)count_values[j] / (double)(remain_state.size()-1));
    }
    double temp_entropy;
    for(j = 0; j < values.size(); j++){
        temp_entropy = ComputeEntropy(remain_state, attribute, values[j], false);
        children_entropy += ratio[j] * temp_entropy;
    }
    return (parent_entropy - children_entropy);
}

int FindAttriNumByName(string attri){
    for(int i = 0; i < MAXLEN; i++){
        if(!state[0][i].compare(attri)) return i;
    }
    cerr<<"can't find the numth of attribute"<<endl;
    return 0;
}

//�ҳ�������ռ��������/����
string MostCommonLabel(vector <vector <string> > remain_state){
    int p = 0, n = 0;
    for(unsigned i = 0; i < remain_state.size(); i++){
        if(!remain_state[i][MAXLEN-1].compare(yes)) p++;
        else n++;
    }
    if(p >= n) return yes;
    else return no;
}

//�ж������Ƿ������Զ�Ϊlabel
bool AllTheSameLabel(vector <vector <string> > remain_state, string label){
    int count = 0;
    for(unsigned int i = 0; i < remain_state.size(); i++){
        if(!remain_state[i][MAXLEN-1].compare(label)) count++;
    }
    if(count == remain_state.size()-1) return true;
    else return false;
}

//������Ϣ���棬DFS����������
//current_nodeΪ��ǰ�Ľڵ�
//remain_stateΪʣ������������
//remian_attributeΪʣ�໹û�п��ǵ�����
//���ظ����ָ��
Node * BulidDecisionTreeDFS(Node * p, vector <vector <string> > remain_state, vector <string> remain_attribute){
    //if(remain_state.size() > 0){
        //printv(remain_state);
    //}
    if (p == NULL)
        p = new Node();
    //�ȿ���������Ҷ�����
    if (AllTheSameLabel(remain_state, yes)){
        p->attribute = yes;
        return p;
    }
    if (AllTheSameLabel(remain_state, no)){
        p->attribute = no;
        return p;
    }
    if(remain_attribute.size() == 0){//���е����Ծ��Ѿ���������,��û�з־�
        string label = MostCommonLabel(remain_state);
        p->attribute = label;
        return p;
    }

    double max_gain = 0, temp_gain;
    vector <string>::iterator max_it = remain_attribute.begin();
    vector <string>::iterator it1;
    for(it1 = remain_attribute.begin(); it1 < remain_attribute.end(); it1++){
        temp_gain = ComputeGain(remain_state, (*it1));
        if(temp_gain > max_gain) {
            max_gain = temp_gain;
            max_it = it1;
        }
    }
    //�������max_itָ������������ֵ�ǰ���������������������Լ�
    vector <string> new_attribute;
    vector <vector <string> > new_state;
    for(vector <string>::iterator it2 = remain_attribute.begin(); it2 < remain_attribute.end(); it2++){
        if((*it2).compare(*max_it)) new_attribute.push_back(*it2);
    }
    //ȷ������ѻ������ԣ�ע�Ᵽ��
    p->attribute = *max_it;
    vector <string> values = map_attribute_values[*max_it];
    int attribue_num = FindAttriNumByName(*max_it);
    new_state.push_back(attribute_row);
    for(vector <string>::iterator it3 = values.begin(); it3 < values.end(); it3++){
        for(unsigned int i = 1; i < remain_state.size(); i++){
            if(!remain_state[i][attribue_num].compare(*it3)){
                new_state.push_back(remain_state[i]);
            }
        }
        Node * new_node = new Node();
        new_node->arrived_value = *it3;
        if(new_state.size() == 0){//��ʾ��ǰû�������֧����������ǰ��new_nodeΪҶ�ӽڵ�
            new_node->attribute = MostCommonLabel(remain_state);
        }
        else
            BulidDecisionTreeDFS(new_node, new_state, new_attribute);
        //�ݹ麯������ʱ������ʱ��Ҫ1 ���½����븸�ڵ㺢������ 2���new_state����
        p->childs.push_back(new_node);
        new_state.erase(new_state.begin()+1,new_state.end());//ע�������new_state�е�ǰһ��ȡֵ��������׼��������һ��ȡֵ����
    }
    return p;
}

void Input(){
    string s;
    while(cin>>s){//EOFΪ�������
        item[0] = s;
        for(int i = 1;i < MAXLEN; i++){
            cin>>item[i];
        }
        state.push_back(item);//ע��������ϢҲ�����ȥ��������
    }
    for(int j = 0; j < MAXLEN; j++){
        attribute_row.push_back(state[0][j]);
    }
}

void PrintTree(Node *p, int depth){
    for (int i = 0; i < depth; i++) cout << '\t';//����������������tab
    if(!p->arrived_value.empty()){
        cout<<p->arrived_value<<endl;
        for (int i = 0; i < depth+1; i++) cout << '\t';//����������������tab
    }
    cout<<p->attribute<<endl;
    for (vector<Node*>::iterator it = p->childs.begin(); it != p->childs.end(); it++){
        PrintTree(*it, depth + 1);
    }
}

void FreeTree(Node *p){
    if (p == NULL)
        return;
    for (vector<Node*>::iterator it = p->childs.begin(); it != p->childs.end(); it++){
        FreeTree(*it);
    }
    delete p;
    tree_size++;
}

int main(){
    Input();
    vector <string> remain_attribute;

    string outlook("Outlook");
    string Temperature("Temperature");
    string Humidity("Humidity");
    string Wind("Wind");
    remain_attribute.push_back(outlook);
    remain_attribute.push_back(Temperature);
    remain_attribute.push_back(Humidity);
    remain_attribute.push_back(Wind);
    vector <vector <string> > remain_state;
    for(unsigned int i = 0; i < state.size(); i++){
        remain_state.push_back(state[i]);
    }
    ComputeMapFrom2DVector();
    root = BulidDecisionTreeDFS(root,remain_state,remain_attribute);
    cout<<"the decision tree is :"<<endl;
    PrintTree(root,0);
    FreeTree(root);
    cout<<endl;
    cout<<"tree_size:"<<tree_size<<endl;
    return 0;
}
