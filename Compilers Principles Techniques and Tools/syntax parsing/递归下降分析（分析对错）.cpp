#include<stdio.h>
#include<stdlib.h>

#define ERROR 0

char sym;  //������ʱ�洢�ļ��ж����ĵ����ַ�
FILE *fp;  //��ȡ�ļ���ָ��

//���ս������ķ���
void e();
void g();
void t();
void s();
void f();
//��ȡ�ļ��е���һ���ַ�
void advance();
int main()
{

	if((fp=fopen("Input.txt","r"))==NULL)//��ȡ�ļ����ݣ��������ļ�ָ�룬��ָ��ָ���ļ��ĵ�һ���ַ�
	{
		fprintf(stderr,"error opening.\n");
		exit(1);
	}
	e();

	return 0;
}
//��Ӧ����ʽ��1��E->TG
void e()
{
	advance();
	t();
	g();
	if(sym=='#')
	{
		printf("\n\n");
	}
	else
	{
		printf("ERROR");
	}

}
//��Ӧ����ʽ��2��G->+TG ��3��G->-TG��4��G->��  �� �������κδ���

void g()
{
	if(sym =='+')
	{
		printf("+");
		advance();
		t();
		g();
	}
	else if(sym == '-')
    {
        printf("-");
		advance();
		t();
		g();
    }
}
//��Ӧ����ʽ  ��5��T->FS
void t()
{
	f();
	s();
}
// ��Ӧ����ʽ��6��S->*FS ��7��S->/FS ��8��S->��
void s()
{
	if(sym == '*')
	{
		printf("*");
		advance();
		f();
		s();
	}
	else if(sym == '/')
    {
        printf("/");
		advance();
		f();
		s();
    }
}
//��Ӧ����ʽ��9��F->(E)  ��10��F->i ��11��F->num

void f()
{
	if(sym == '(')
	{
		advance();
		e();
		if(sym == ')')
			advance();
		else
		{
			printf("ERROR");
			exit(ERROR);
		}
	}
	else if(sym == 'i')
	{
		printf("i");
		advance();
	}
	else if(sym >='0' && sym <='9')
    {
        printf("%c",sym);
    }
	else
	{
		printf("ERROR");
		exit(ERROR);
	}
}
void advance()
{
	sym = fgetc(fp);// ��������������һ���ַ�
}
