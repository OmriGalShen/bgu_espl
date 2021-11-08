#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

int cmpstr(char *s1, char *s2);

int main(int argc, char **argv) {

	if (argc != 3) {
		fprintf(stderr, "Usage: %s string1 string2\n", argv[0]);
		exit(1);
	}

	int cmp = cmpstr(argv[1], argv[2]);
	printf("\"%s\" %s \"%s\"\n", argv[1], cmp < 0 ? "<" : cmp > 0 ? ">" : "==", argv[2]);
	printf("The difference is %d\n", cmp);

	return cmp;
}
