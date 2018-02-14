#include <algorithm>
#include <iostream>
#include <iomanip>
#include <cstring>
#include <climits>
#include <complex>
#include <fstream>
#include <cassert>
#include <cstdio>
#include <bitset>
#include <vector>
#include <deque>
#include <queue>
#include <stack>
#include <ctime>
#include <set>
#include <map>
#include <cmath>
#include <functional>
#include <numeric>
using namespace std;
const int maxn=305;
set<string> VT,VN;
vector<pair<string,string> > Phi;
map<string,int> Map;
map<int,string> re;
vector<string> G[maxn];
set<string> FIRST[maxn],FOLLOW[maxn];
int number;
string S;
int vis[maxn],vis1[maxn];
string kesi="kesi";
pair<string,string> M[maxn][maxn];

set<string> getFIRST(string t)
{
    if(t.length()==1)
    {
        int x=Map[t];
        if(vis[x])return FIRST[x];//���x��FIRST���Ѿ������ֱ�ӷ���
        vis[x]=1;
        for(int i=0; i<G[x].size(); i++)
        {
            if(G[x][i]==kesi)FIRST[x].insert(kesi);
            bool flag=true;//��ʾFIRST1~i-1�Ķ���kesi,��ʼֵ��Ϊtrue����������������Էŵ�һ��
            if(G[x][i]==kesi)
            {
                FIRST[x].insert(kesi);
                continue;
            }
            for(int j=0; j<G[x][i].length()&&flag; j++)
            {
                if(!vis[Map[G[x][i].substr(j,1)]])getFIRST(G[x][i].substr(j,1));
                int v=Map[G[x][i].substr(j,1)];
                for(set<string>::iterator it=FIRST[v].begin(); it!=FIRST[v].end(); it++)
                {
                    string tmp=(*it);
                    {
                        string B="E";
                        string f="+";
                        if(t==B&&(*it)==f)cout<<G[x][i]<<" "<<i<<endl;
                    }
                    if(tmp!=kesi)FIRST[x].insert(tmp);
                }
                if(FIRST[v].find(kesi)==FIRST[v].end())flag=false;
            }
            if(flag)FIRST[x].insert(kesi);
        }
        return FIRST[x];
    }
    else
    {
        bool flag=true;
        set<string> ret;
        ret.clear();
        for(int i=0; i<t.size()&&flag; i++)
        {
            int u=Map[t.substr(i,1)];
            for(set<string>::iterator it=FIRST[u].begin(); it!=FIRST[u].end(); it++)
            {
                string t=(*it);
                if(t!=kesi)ret.insert(t);
            }
            if(FIRST[u].find(kesi)==FIRST[u].end())flag=false;
        }
        if(flag)ret.insert(kesi);
        return ret;
    }
}



set<string> getFOLLOW(string B)
{
    int x=Map[B];
    if(vis1[x])return FOLLOW[x];
    vis1[x]=1;
    for(int i=0; i<Phi.size(); i++)
    {
        string A=Phi[i].first,omiga=Phi[i].second;
        int Size=omiga.size();
        for(int j=0; j<Size; j++)
            if(omiga.substr(j,1)==B)
            {
                int u=Map[omiga.substr(j,1)];
                set<string> FIRSTt;
                FIRSTt.clear();
                if(j+1<Size)
                {
                    FIRSTt=getFIRST(omiga.substr(j+1,Size-(j+1)));
                    for(set<string>::iterator it=FIRSTt.begin(); it!=FIRSTt.end(); it++)
                    {
                        string t=(*it);
                        if(t!=kesi)FOLLOW[u].insert(t);
                    }
                }
                if(A!=B&&(j==Size-1||FIRSTt.find(kesi)!=FIRSTt.end()))
                {
                    if(!vis1[Map[A]])getFOLLOW(A);
                    for(set<string>::iterator it=FOLLOW[Map[A]].begin(); it!=FOLLOW[Map[A]].end(); it++)
                    {
                        string t=(*it);
                        FOLLOW[Map[B]].insert(t);
                    }
                }
            }
    }
    return FOLLOW[x];
}

int main()
{
    freopen("input1.txt","r",stdin);
//	freopen("output.txt","w",stdout);
    printf("�������ķ�G=(VT,VN,S,Phi),����:\n");
    printf("�������ս���ż���VT(�Ե������Ž��б�ʾ),(��������Ŀ����һ��Ϊ�ս���ţ��м��Կո�ֿ�):\n");
    int idx=0;//���ս������ս�����б��
    cin>>number;
    while(number--)
    {
        string s;
        cin>>s;
        if(!Map.count(s))
        {
            re[idx]=s;
            Map[s]=idx++;
        }
        VT.insert(s);
    }
    Map["$"]=idx++;

    printf("��������ս���ż���VN(�Դ�д������ĸ���б�ʾ)��(��������Ŀ����һ��Ϊ���ս���ţ��м��Կո�ֿ�):\n");
    cin>>number;
    while(number--)
    {
        string s;
        cin>>s;
        if(!Map.count(s))
        {
            re[idx]=s;
            Map[s]=idx++;
        }
        VN.insert(s);
    }


    printf("�������ķ�G�Ŀ�ʼ����S:\n");
    cin>>S;

    printf("�������ķ�G�Ĳ���ʽ����Phi(��������Ŀm��֮��m��Ϊ����ʽ����ʽΪalpha beta,��ʾalpha->beta���м��Կո�ֿ�����kesi��ʾ��):\n");
    int phinum;
    cin>>phinum;
    Phi.clear();
    while(phinum--)
    {
        string alpha,beta;
        cin>>alpha>>beta;
        Phi.push_back(make_pair(alpha,beta));
        G[Map[alpha]].push_back(beta);
    }

    for(int i=0; i<Phi.size(); i++)
    {
        string alpha=Phi[i].first,beta=Phi[i].second;
        cout<<alpha<<"->"<<beta<<endl;
    }

    //��ֹ����FIRST���Ĺ���
    for(set<string>::iterator it=VT.begin(); it!=VT.end(); it++)
    {
        string x=(*it);
        FIRST[Map[x]].insert(x);
        vis[Map[x]]=1;//��ʾX��FIRST���Ѿ���������ں��������ֹ���ŵ�FIRST��ļ��仨��������
    }


    //����ֹ����FIRST���Ĺ���
    for(set<string>::iterator it=VN.begin(); it!=VN.end(); it++)
    {
        string x=(*it);
        FIRST[Map[x]]=getFIRST(x);
    }

    for(set<string>::iterator it=VN.begin(); it!=VN.end(); it++)
    {
        cout<<"FIRST["<<(*it)<<"]={";
        string X=(*it);
        bool first=true;
        for(set<string>::iterator it1=FIRST[Map[X]].begin(); it1!=FIRST[Map[X]].end(); it1++)
        {
            if(first)
            {
                cout<<(*it1);
                first=false;
            }
            else cout<<","<<(*it1);
        }
        cout<<"}"<<endl;
    }


    FOLLOW[Map[S]].insert("$");

    for(set<string>::iterator it=VN.begin(); it!=VN.end(); it++)
    {
        string B=(*it);
        FOLLOW[Map[B]]=getFOLLOW(B);
    }

    for(set<string>::iterator it=VN.begin(); it!=VN.end(); it++)
    {
        cout<<"FOLLOW["<<(*it)<<"]={";
        string X=(*it);
        bool first=true;
        for(set<string>::iterator it1=FOLLOW[Map[X]].begin(); it1!=FOLLOW[Map[X]].end(); it1++)
        {
            if(first)
            {
                cout<<(*it1);
                first=false;
            }
            else cout<<","<<(*it1);
        }
        cout<<"}"<<endl;
    }
    int delta=VT.size();
    delta++;

    for(int i=0; i<VN.size(); i++)
        for(int j=0; j<VT.size(); j++)M[i][j]=make_pair("","");

    for(int i=0; i<Phi.size(); i++)
    {
        string A=Phi[i].first,alpha=Phi[i].second;
        set<string> FIRSTalpha=getFIRST(alpha);
        cout<<A<<"->"<<alpha<<endl;
        cout<<"FIRST[Alpha]={";
        bool first=true;
        for(set<string>::iterator it=FIRSTalpha.begin(); it!=FIRSTalpha.end(); it++)
        {
            if(first)
            {
                first=false;
                cout<<(*it);
            }
            else cout<<","<<(*it);
        }
        cout<<"}"<<endl;

        cout<<"FOLLOW["<<A<<"]={";
        first=true;
        for(set<string>::iterator it=FOLLOW[Map[A]].begin(); it!=FOLLOW[Map[A]].end(); it++)
        {
            if(first)
            {
                first=false;
                cout<<(*it);
            }
            else cout<<","<<(*it);
        }
        cout<<"}"<<endl;

        for(set<string>::iterator it=FIRSTalpha.begin(); it!=FIRSTalpha.end(); it++)
        {
            string a=(*it);
            if(VT.find(a)!=VT.end())
            {
                M[Map[A]-delta][Map[a]]=Phi[i];
                cout<<A<<' '<<a<<' '<<Phi[i].first<<"->"<<Phi[i].second<<endl;;
            }
        }
        if(FIRSTalpha.find(kesi)!=FIRSTalpha.end())
            for(set<string>::iterator it=FOLLOW[Map[A]].begin(); it!=FOLLOW[Map[A]].end(); it++)
            {
                string b=(*it);
                M[Map[A]-delta][Map[b]]=Phi[i];
                cout<<A<<' '<<b<<' '<<Phi[i].first<<"->"<<Phi[i].second<<endl;;
            }
    }

    return 0;
}
