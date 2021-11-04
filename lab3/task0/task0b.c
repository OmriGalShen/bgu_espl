#include <stdio.h>
#include <stdlib.h>

void printHex(unsigned char* buffer,int length){
    int i;
    for (i=0;i<length;i++){
        printf("%X ",buffer[i]);
    }
    printf("\n");
}

int main(int argc, char **argv) {
    int length;
    FILE *fp = fopen(argv[1],"rb");
    unsigned char* buffer;
    size_t result;

    fseek(fp , 0 , SEEK_END);
    length = ftell(fp);
    rewind(fp);

    buffer = (unsigned char*) malloc (sizeof(char)*length);
    result = fread(buffer,1,length,fp);

    printHex(buffer,result);

    fclose(fp);
    free (buffer);
    return 0;
}