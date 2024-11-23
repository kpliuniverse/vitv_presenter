#include <stdlib.h>

#include <stdio.h>


void vitv_error(const char* info) {
    fprintf(stderr, "ERROR: %s\n", info);
    //fprintf(stderr, "ERROR: %s\n", info);
    exit(1);
}

void vitv_info(const char* info) {
    printf("INFO: %s\n", info);
    //fprintf(stderr, "ERROR: %s\n", info);
    //exit(1);
}