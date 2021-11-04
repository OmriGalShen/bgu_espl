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
	fgets(s, 10, stdin);
}

void bitwise_or(char* s){
  int res = 0;
  int i;
  for(i=0; i<strlen(s)-1; i++){
    res |= s[i];
  }
  
  char bin_string[9];
  int hex_num = res;
  for(i=7; i>=0; i--){
    bin_string[i] = (res&1)  ? '1':'0';
    res >>= 1;
  }
  bin_string[8] = '\0';

  printf("the result is %X in hex and %s in binary\n", hex_num, bin_string);

}
 
int main(int argc, char **argv){
  printf("write a string to echo:\n");
  char s[10]; 
  string_reader(s);
  printf("%s",s);
  printf("this is the bitwise_or test for 'abd' string\n");
  bitwise_or("abd");

  return 0;
}
