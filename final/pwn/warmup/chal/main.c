#include <stdio.h>
#include <unistd.h>
#include <signal.h>

void init() {
    // Disable buffering of stdin and stdout
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    
    // Set the alarm to a desired time (in seconds)
    alarm(60); // Change the value to the desired timeout
}


void read_from_address() {
    unsigned long long address;
    printf("Enter the address to read from (hex): ");
    if (scanf("%llx", &address) < 1) {
        return;
    }

    unsigned long long value = *(unsigned long long *)address;
    printf("Value at address %p: %llx\n", (void *)address, value);
}

void call_function() {
    unsigned long long address;
    printf("Enter the address of the function to call (first arg is \"/bin/sh\"): ");
    scanf("%llx", &address);

    void (*func)(char *) = (void (*)(char *))address;
    func("/bin/sh");
}

int dummy;

int main() {
    init();

    printf("Freebie: %p\n", &dummy);

    while (1) {
        int option;
        printf("\nSelect an option:\n");
        printf("1. Read from address\n");
        printf("2. Call an arbitrary address\n");
        printf("3. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &option);

        switch (option) {
            case 1:
                read_from_address();
                break;
            case 2:
                call_function();
                break;
            case 3:
                printf("Exiting...\n");
                return 0;
            default:
                printf("Invalid option. Try again.\n");
                break;
        }
    }

    return 0;
}

