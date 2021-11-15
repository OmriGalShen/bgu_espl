#include <stdio.h>
int cmpstr(char *s1, char *s2)
{
    int res=0;
    while(*(s1++) != '\0'&& *(s2++) != '\0')
    {
        res = (*s1)-(*s2);
        if(res!=0)
            return res; 
    }
    return res;
}