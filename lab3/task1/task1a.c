#include <stdio.h>
#include <stdlib.h>

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
        fprintf(output, "byte %ld %X %X\n",data->offset, data->orig_value, data->new_value);
        curr = curr->next;
    }
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

int main(int argc, char **argv) {
    diff *data1 = calloc(1, sizeof(diff));
    diff *data2 = calloc(1, sizeof(diff));
    diff *data3 = calloc(1, sizeof(diff));
    data1->orig_value = 0xA1;
    data1->new_value = 0xFF;
    data1->offset = 1;
    data2->orig_value = 0xA2;
    data2->new_value = 0xFF;
    data2->offset = 2;
    data3->orig_value = 0xA3;
    data3->new_value = 0xFF;
    data3->offset = 3;
    struct node *list = NULL;
    list = list_append(list,data1);
    list = list_append(list,data2);
    list = list_append(list,data3);
    list_print(list,stdout);
    list_free(list);
    return 0;
}