#include <stdio.h> 
#include <string.h>
 
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
    func_ptr(str[i]);
    printf(" ");
  }
  printf("\n");
}
 
void string_reader(char* s){
  /* TODO: Complete during task 2c*/
}
 
void bitwise_and(char* s){
  /* TODO: Complete during task2c */
}
 
int main(int argc, char **argv){
  char c[] = {'L','a','b','2','\0'};
  string_printer(c, ascii_printer); /* Result: 76 97 98 50 */

  return 0;
}
