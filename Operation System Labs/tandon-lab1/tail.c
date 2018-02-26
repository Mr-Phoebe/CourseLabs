#include "types.h"
#include "stat.h"
#include "user.h"
#include "fcntl.h"

char buf[512];


void print_help()
{
    printf(1, "Usage: tail [OPTION]... [FILE]...\nPrint the first 10 lines of each FILE to standard output.\nWith more than one FILE, precede each with a tailer giving the filename.\nPossible arguments are:\n\n\t-NUM\t\tprint the first NUM lines of each file;\n");
    exit();
}

void print_error(uint err, char* s)
{
    switch(err)
    {
    case(0):
        printf(2, "tail: invalid option %s\nTry 'tail --help' for more information\n", s);
        break;
    case(1):
        printf(2,"tail: invalid number of lines: %s\n", s);
        break;
    case(2):
        printf(2, "tail: cannot open '%s' for reading: No such file or directory\n", s);
        break;
    default:
        printf(2, "tail: error\n");
    }
    exit();
}

void tail(int fd, int n)
{
    int i, r, l = 0, nl, tmpptr;
  
    tmpptr = open ("tmpfile", O_CREATE | O_RDWR);
    while((r = read(fd, buf, sizeof(buf))) > 0)
    {

        write(tmpptr, buf, sizeof(char)*r);
        for(i = 0; i < r; i++)
            if(buf[i]=='\n')
                l++;
    }
    nl = l;
    l = 0;
    close(tmpptr);
    tmpptr = open ("tmpfile", 0);

    while((r = read(tmpptr, buf, sizeof(buf))) > 0)
    {
        for(i = 0; i < r; i++)
        {
            if(nl - l <= n)
                printf(1, "%c", buf[i]);
            if(buf[i] == '\n')
                l++;
        }
    }
    close(tmpptr);
    unlink("tmpfile");
}

int main(int argc, char *argv[])
{
    int i, n = 10, fd;
    char *c;
    short flag = 0;
    short stop = 0;
    for(i = 1; i < argc; i++)
    {
        strcpy(buf, argv[i]);
        if(stop == 0 && buf[0]=='-')
        {
            if(buf[1] == '-')
            {
                c = buf;
                c += 2;
                if(strcmp(c, "help") == 0)
                    print_help();
                else if(strcmp(c, "\0") == 0)
		    stop = 1;
		else
                    print_error(0, argv[i]);
            }
            else
            {
                c = buf;
                c += 1;
                if(atoi(c) == 0)
                    print_error(1, c);
                n = atoi(c);
            }
        }
        else
        {
            flag = 1;
            if((fd = open(argv[i], 0)) < 0){
                print_error(2, argv[i]);
                exit();
            }
            tail(fd, n);
	    close(fd);
            if(i+1 < argc)
                printf(1, "\n");
        }
    }
    if(flag == 0)
    {
        tail(0, n);
    }
    exit();
}

