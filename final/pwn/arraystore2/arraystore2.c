#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

uint64_t array[100];
FILE* randfile;
int main() {
    randfile = fopen("/dev/urandom", "r");
    char str[100];
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
    printf("Your array has 100 entries\n");
    while(1) {
        printf("Read/Write/Random?: ");
        fgets(str, 100, stdin);
        if(str[1] == 'e') {
            printf("Index: ");
            fgets(str, 100, stdin);
            uint64_t index = strtoul(str, NULL, 10);
            printf("Value: %lu\n", array[index]);
        } else if(str[1] == 'r') {
            printf("Index: ");
            fgets(str, 100, stdin);
            uint64_t index = strtoul(str, NULL, 10);
            printf("Value: ");
            fgets(str, 100, stdin);
            array[index] = strtoul(str, NULL, 10);
        } else if(str[1] == 'a') {
            uint64_t num;
            fread(&num, 1, 8, randfile);
            printf("Value: %lu\n", num);
        } else {
            printf("Invalid option\n");
            break;
        }
    }
    fclose(randfile);
    return 0;
}