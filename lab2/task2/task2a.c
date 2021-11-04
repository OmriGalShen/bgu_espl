#include <stdio.h> 
 
void echo_printer(char c){ /* task 0 from lab1 - prints c to the standard output */
	printf("%c ",c);
}

void ascii_printer(char c){ /* task 1a from lab1 - print the ASCII code of c to the standard output*/
	printf("%d ", c);
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
		printf("%c ", c & ~32);
	else
		printf("%c ", c & ~32);
}
 
void string_printer(char* str, void (*func_ptr) (char)){
  /* TODO: Complete during task 2b */
}
 
void string_reader(char* s){
  /* TODO: Complete during task 2c*/
}
 
void bitwise_and(char* s){
  /* TODO: Complete during task2c */
}
 
int main(int argc, char **argv){
  char c = 'a';  
  printf("initial char:%c",c);
  printf("\n");
  printf("echo_printer:");
  echo_printer(c);  
  printf("\n");
  printf("ascii_printer:");
  ascii_printer(c);  
  printf("\n");
  printf("binary_printer:");
  binary_printer(c);
  printf("\n");
  printf("lower_to_upper_printer:");
  lower_to_upper_printer(c);
  printf("\n");
  printf("\n");

  c = 'b';  
  printf("initial char:%c",c);
  printf("\n");
  printf("echo_printer:");
  echo_printer(c);  
  printf("\n");
  printf("ascii_printer:");
  ascii_printer(c);  
  printf("\n");
  printf("binary_printer:");
  binary_printer(c);
  printf("\n");
  printf("lower_to_upper_printer:");
  lower_to_upper_printer(c);
  printf("\n");

  return 0;
}
