#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void task1a();
void task1b();
void task1c();
void getBinary(char* arr,int num);
FILE* input;
FILE* output;

int main(int argc, char **argv)
{
    input = stdin;
    output = stdout;
    char isBin = 0, isCase = 0; // flags
    for (int i = 1; i < argc; i++)
    {
        if (strcmp(argv[i], "-b") == 0) isBin = 1;
        else if (strcmp(argv[i], "-c") == 0) isCase = 1;
        else if (strcmp(argv[i], "-i") == 0) input = fopen(argv[++i],"r");
        else if (strcmp(argv[i], "-o") == 0) output = fopen(argv[++i],"w");
        else printf("invalid parameter - %s\n", argv[i]);
    }
    if(isCase) task1c();
    else if(isBin) task1b();
    else task1a();
    return 0;
}

void task1a()
{
    char ch;
    while((ch=getc(input))!=EOF){
        if(ch!='\n')
            fprintf(output,"%d ",ch);
        else 
            fprintf(output,"%c",ch);
    }
}

void task1b()
{
    char ch;
    char arr[8];
    while((ch=getc(input))!=EOF){
        if(ch!='\n')
        {
            getBinary(arr,ch); // fill array with 8bit binary 
            for(int i=0;i<8;i++)
                fprintf(output,"%d",arr[i]);
            fprintf(output," ");
        }
        else 
            fprintf(output,"%c",ch);
    }
}

void getBinary(char* arr,int num)
{
    for(int i=0;i<8;i++) arr[i]=0; //zero out
    int j=7;
    while(num>0&&j>=0){
        arr[j]=num&1; //masking last bit
        j--;
        num = num >> 1; //divide by 2
    }
}

void task1c()
{
    char ch;
    while((ch=getc(input))!=EOF){
        if(ch >= 'a' && ch <= 'z') ch-=32;
        else if(ch >= 'A' && ch <= 'Z') ch+=32;               
        fprintf(output,"%c",ch);
    }
}

