// #include <stdio.h>
// #include <string.h>
// #include <stdlib.h>

// void task1a();
// void task1b();
// void task1c();
// void getBinary(char* arr,int num);

// int main(int argc, char **argv)
// {
//     if(argc==1)
//         task1a();
//     else if(argc==2 && (strcmp(argv[1], "-b") == 0))
//         task1b();
//     else if(argc==2 && (strcmp(argv[1], "-c") == 0))
//         task1c();
//     else 
//         return 1;
//     return 0;
// }

// void task1a()
// {
//     char ch = getc(stdin);
//     while(ch!=EOF){
//         if(ch!='\n')
//             printf("%d ",ch);
//         else 
//             printf("%c",ch);
//         ch = getc(stdin);
//     }
// }

// void task1b()
// {
//     char ch = getc(stdin);
//     char arr[8];
//     while(ch!=EOF){
//         if(ch!='\n')
//         {
//             getBinary(arr,ch);
//             for(int i=0;i<8;i++)
//                 printf("%d",arr[i]);
//             printf(" ");
//         }
//         else 
//             printf("%c",ch);
//         ch = getc(stdin);
//     }
// }

// void getBinary(char* arr,int num)
// {
//     for(int i=0;i<8;i++) arr[i]=0; //zero out
//     int j=7;
//     while(num>0&&j>=0){
//         arr[j]=num&1; //masking last bit
//         j--;
//         num = num >> 1; //divide by 2
//     }
// }

// void task1c()
// {
//     char ch = getc(stdin);
//     while(ch!=EOF){
//         if(ch!='\n')
//         {
//             if(ch >= 'a' && ch <= 'z')
//                 ch-=32;
//             else if(ch >= 'A' && ch <= 'Z')
//                 ch+=32;
//             printf("%c ",ch);
//         }
//         else 
//             printf("%c",ch);
//         ch = getc(stdin);
//     }
// }

