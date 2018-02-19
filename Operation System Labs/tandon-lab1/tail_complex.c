#include "types.h"
#include "stat.h"
#include "user.h"
#define MAX_BUF 512
#define STDIN "_stdin"

char buf[MAX_BUF];

void print_help()
{
    printf(1, "Usage: tail [OPTION]... [FILE]...\n\
           Print the last 10 lines of each FILE to standard output.\n\
           With more than one FILE, precede each with a header giving the filename.\n\
           Possible arguments are:\n\t-c NUM\t\tprint the last NUM bytes of each file;\n\
           \t-n NUM\t\tprint the last NUM lines of each file;\n\
           \t-q\t\tquiet, never print headers giving file names;\n\
           \t-v\t\tverbose, print headers giving file names;\n");
    exit();
}

void error_tail(uint err, char* s)
{
    switch(err)
    {
    case(0):
        printf(2, "tail: syntax error\n");
        break;
    case(1):
        printf(2, "tail: invalid option %s\nTry 'tail --help' for more information\n", s);
        break;
    case(2):
        printf(2,"tail: syntax error, expected at least one argument\n");
        break;
    case(3):
        printf(2,"tail: invalid number of lines: %s\n", s);
        break;
    case(4):
        printf(2,"tail: invalid number of bytes: %s\n", s);
        break;
    case(5):
        printf(2, "tail: read error\n");
        break;
    case(6):
        printf(2, "tail: cannot open '%s' for reading: No such file or directory\n", s);
        break;
    default:
        printf(2, "tail: error\n");
    }
    exit();
}

void tail(char *fn, int n, int mode, int moden)
{
    int i, r, fd;
    int nr=0, nb=0; //number of rows, bytes
    int nrf, nbf;   //final number of rows, bytes

    if(strcmp(fn, STDIN)==0)
    {
        fd=0;
    }
    else
    {
        fd = open(fn, 0);
        if(fd < 0)
        {
            error_tail(6, fn);
        }
    }

    //print the filename when required
    if(mode==2)
    {
        printf(1, "==> %s <==\n", fn);
    }

    //first passage on file to know the total number of lines and bytes
    while((r = read(fd, buf, sizeof(buf))) > 0)
    {
        for(i=0; i<r; i++)
        {
            nb++;
            if(buf[i] == '\n' && moden != 2)
            {
                nr++;
                //nbtot+=nb;
                //nb=0;
            }
        }
    }
    if(r < 0)
    {
        close(fd);
        error_tail(5, 0);
    }
    nbf=nb;
    nrf=nr;
    nb=0;
    nr=0;
    close(fd);
    fd = open(fn, 0);

    //second passage with actual printing
    while((r = read(fd, buf, sizeof(buf))) > 0)
    {
        for(i=0; i<r; i++)
        {
            if(moden!=2 && nrf-nr<=n)
            {
                printf(1, "%c", buf[i]);
            }
            if(moden==2 && nbf-nb<=n)
            {
                printf(1, "%c", buf[i]);
            }

            nb++;
            if(buf[i] == '\n' && moden != 2)
            {
                nr++;
            }
        }
    }
    if(r < 0)
    {
        close(fd);
        error_tail(5, 0);
    }

}

int main(int argc, char *argv[])
{
    int i, mode=0, moden=0, n=10;
    char *c;

    if(argc <= 1)
    {
        tail(STDIN, n, mode, moden);
        exit();
    }
    //start checking the arguments
    //skip the first since it is the name of the command
    for(i = 1; i < argc; i++)
    {
        strcpy(buf, argv[i]);
        if(buf[0]=='-')   //option, not filename
        {
            switch(buf[1])
            {
            case 'n':
                if(atoi(argv[++i]) == 0)
                {
                    error_tail(3, argv[i]);
                }
                n = atoi(argv[i]);
                moden=1;
                break;
            case 'c':
                if(atoi(argv[++i]) == 0)
                {
                    error_tail(4, argv[i]);
                }
                n = atoi(argv[i]);
                moden=2;
                break;
            case 'v':
                mode=2;
                break;
            case 'q':
                mode=1;
                break;
            case '-':
                c=buf;
                c+=2;
                if(strcmp(c, "help") == 0)
                {
                    print_help();
                }
                else
                {
                    error_tail(1, argv[i]);
                }
                break;
            default:
                error_tail(1, argv[i]);
                break;
            }
        }
        else
        {
            //filenames
            if(i+1<argc && mode==0)
            {
                //-q not specified and multiple files
                mode=2;
            }
            tail(argv[i], n, mode, moden);
            if(i+1 < argc)
            {
                printf(1, "\n");
            }
        }
    }//end cicle arguments
    exit();
}
