#include <stdio.h> 
#include <string.h>
#include <stdlib.h>
 
void echo_printer(char c){ /* task 0 from lab1 - prints c to the standard output */
	printf("%c",c);
}

void ascii_printer(char c){ /* task 1a from lab1 - print the ASCII code of c to the standard output*/
	printf("%d", c);
} 

void binary_printer(char c){ /* task 1b from lab1 – print the binary representation of c to the standard output */
  int binary[8];
  int i;
	for(i=7; i>=0; i--){
		binary[i] = c&1;
		c >>= 1;
	}
  for(i=0; i<8; i++)
    printf("%d",binary[i]);
}

void lower_to_upper_printer(char c){ /* task 1c from lab1 – print c to the standard output in upper case */
  if (c >= 'a' && c <= 'z')
		printf("%c", c & ~32);
	else
		printf("%c", c & ~32);
}
 
void string_printer(char* str, void (*func_ptr) (char)){
  int i;
  for(i=0; i<strlen(str); i++){
    if(str[i] != '\n')
        func_ptr(str[i]);
    printf(" ");
  }
  printf("\n");
}
 
void string_reader(char* s){
	fgets(s, 10, stdin);
}

void bitwise_or(char* s){
  int res = 0;
  int i;
  for(i=0; i<strlen(s)-1; i++){
    res |= s[i];
  }

  printf("the result is %X in hex and ",res);
  binary_printer(res);
  printf(" in binary\n");

}

typedef struct fun_desc{
    char *name;
    void (*fun)(char);
} fun_desc;

int main(int argc, char **argv){
  fun_desc functions[] =    {{"echo printer",echo_printer},
                            {"ASCII printer",ascii_printer},
                            {"binary printer",binary_printer},
                            {"lower to upper",lower_to_upper_printer},
                            {"bitwise or",NULL}};
  printf("Please enter a string (0<size<=10):\n");                
  
  char s[10];
  string_reader(s);

  printf("Please choose printer type:\n");  
  int i;
  for(i=0; i<=4; i++){
      printf("%d) %s\n",i,functions[i].name);
  }

  int c=0;
  while((fscanf(stdin,"%d",&c) != EOF)){
    printf("Option: ");
    
    if(c=='\n')
        continue;

    if(c>=0 && c<=3)
        string_printer(s, functions[c].fun);
    else if(c == 4)
        bitwise_or(s);
    else
        printf("Please select 1-4 or CTRL-D to exit.\n");
  }
  printf("DONE.\n");

  return 0;
}
