#include <stdio.h>
#include <stdlib.h>

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
    char str[8];
    printf("Echo server: ");
    read(0, str, 1024);
    printf(str);
    puts("");
    printf("Echo server: ");
    read(0, str, 1024);
    printf(str);
    puts("");
    return 0;
}
