#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct diff {
    long offset; /* offset of the difference in file starting from zero*/
    unsigned char orig_value;     /* value of the byte in ORIG */
    unsigned char new_value;     /* value of the byte in NEW */
} diff;

typedef struct node node;

struct node {
    diff *diff_data; /* pointer to a struct containing the offset and the value of the bytes in each of the files*/
    node *next;
};

/* Print the nodes in diff_list in the following format: byte POSITION ORIG_VALUE NEW_VALUE.
Each item followed by a newline character. */
void list_print(node *diff_list, FILE *output) {
    node *curr = diff_list;
    diff *data;
    while (curr != NULL) {
        data = curr->diff_data;
        fprintf(output, "byte %ld %X %X\n", data->offset, data->orig_value, data->new_value);
        curr = curr->next;
    }
}

void list_print_k(node *diff_list, FILE *output, int k) {
    node *curr = diff_list;
    diff *data;
    while (curr != NULL && k > 0) {
        data = curr->diff_data;
        fprintf(output, "byte %ld %X %X\n", data->offset, data->orig_value, data->new_value);
        curr = curr->next;
        k--;
    }
}

int get_list_length(node *diff_list) {
    node *curr = diff_list;
    int counter = 0;
    while (curr != NULL) {
        curr = curr->next;
        counter++;
    }
    return counter;
}

/* Add a new node with the given data to the list,
   and return a pointer to the list (i.e., the first node in the list).
   If the list is null - create a new entry and return a pointer to the entry.*/
node *list_append(node *diff_list, diff *data) {
    struct node *head = malloc(sizeof(node));
    head->diff_data = data;
    head->next = diff_list;
    return head;
}

/* Free the memory allocated by and for the list. */
void list_free(node *diff_list) {
    struct node *curr = diff_list, *next;
    while (curr != NULL) {
        next = curr->next;
        free(curr->diff_data);
        free(curr);
        curr = next;
    }
}

unsigned char *read_file(FILE *fp, size_t *result) {
    long len;
    unsigned char *buffer;
    fseek(fp, 0, SEEK_END);
    len = ftell(fp);
    rewind(fp);
    buffer = (unsigned char *) malloc(sizeof(char) * len);
    *result = fread(buffer, 1, len, fp);
    return buffer;
}

struct node *diff_list(FILE *first_input, FILE *second_input) {
    size_t result1, result2; /*successfully read characters*/
    unsigned char *buffer1 = read_file(first_input, &result1); /* on heap*/
    unsigned char *buffer2 = read_file(second_input, &result2); /* on heap*/
    size_t length = (result1 < result2) ? result1 : result2; /* minimum of the two*/
    struct node *list = NULL;
    long i;
    unsigned char c1, c2;
    diff *data = NULL;
    for (i = 0; i < length; i++) {
        c1 = buffer1[i]; /*character in first file*/
        c2 = buffer2[i]; /*character in second file*/
        if (c1 != c2) {
            data = malloc(sizeof(diff)); /*released at list_free call*/
            data->orig_value = c1;
            data->new_value = c2;
            data->offset = i;
            list = list_append(list, data);
        }
    }
    if (buffer1) free(buffer1);
    if (buffer2) free(buffer2);
    return list;
}

void restore_file(struct node *list, FILE *fp, int r) {
    node *curr = list;
    rewind(fp);
    while (curr != NULL && r != 0) {
        unsigned char original_c = curr->diff_data->orig_value;
        long offset = curr->diff_data->offset;
        fseek(fp, offset, SEEK_SET);
        fputc(original_c, fp);
        r--;
        curr = curr->next;
    }
}


int main(int argc, char **argv) {
    FILE *first_input = NULL;
    FILE *second_input = NULL;
    FILE *output_file = stdout;
    char t_flag = 0, input_flag = 0, r_flag = 0; /* flags */
    int k = -1, i, r = -1;
    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-k") == 0) k = atoi(argv[++i]);
        else if (strcmp(argv[i], "-t") == 0) t_flag = 1;
        else if (strcmp(argv[i], "-r") == 0) {
            if (i != argc - 1) r = atoi(argv[++i]);
            r_flag = 1;
        } else if (strcmp(argv[i], "-o") == 0) output_file = fopen(argv[++i], "w");
        else if (!input_flag) {
            first_input = fopen(argv[i], "rb"); /*read first input file*/
            input_flag = 1;
        } else second_input = fopen(argv[i], "rb+"); /*read second input file*/
    }
    struct node *list = diff_list(first_input, second_input);
    if (r_flag) restore_file(list, second_input, r);
    if (t_flag) fprintf(output_file, "%d\n", get_list_length(list));
    else if (k > 0)list_print_k(list, output_file, k);
    else list_print(list, output_file);
    /* cleaning */
    list_free(list);
    if (first_input)fclose(first_input);
    if (second_input)fclose(second_input);
    if (output_file != stdout)fclose(output_file);
    return 0;
}