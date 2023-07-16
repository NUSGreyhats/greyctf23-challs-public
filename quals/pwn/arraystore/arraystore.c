#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    int64_t array[100];
    char str[100];
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
    printf("Your array has 100 entries\n");
    while(1) {
        printf("Read/Write?: ");
        fgets(str, 100, stdin);
        if(str[0] == 'R') {
            printf("Index: ");
            fgets(str, 100, stdin);
            int64_t index = strtoll(str, NULL, 10);
            if (index > 99) {
                printf("Invalid index\n");
                continue;
            }
            printf("Value: %lld\n", array[index]);
        } else if(str[0] == 'W') {
            printf("Index: ");
            fgets(str, 100, stdin);
            int64_t index = strtoll(str, NULL, 10);
            if (index > 99) {
                printf("Invalid index\n");
                continue;
            }
            printf("Value: ");
            fgets(str, 100, stdin);
            array[index] = strtoll(str, NULL, 10);
        } else {
            printf("Invalid option\n");
            break;
        }
    }
    return 0;
}