#include <stdio.h>
#include <stdint.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// description.txt
// try out our newest calculator model, known to be the fastest ever!
// it currently only does addition though...

char binsh[] = "/bin/sh";
#define RED "\e[0;31m"
#define GRN "\e[0;32m"
#define clear "\e[0m"
#define cave 0x401428

void win(char* arg) {
	if (!strcmp(binsh, arg))
		system(arg);
}

void print_stuff(const char* str, unsigned int security) {
	if (security != 0xdeadbeef)
		return;
	for (int i = 0; i < strlen(str); i++) {
		putchar(*(str+i));
	}
}

void error() {
	print_stuff(RED"CASIO-GLIBC237"": ERROR! USER ISSUE?\n"clear, 0xdeadbeef);
	exit(-1);
}

void boot_emulator(uint8_t a, uint8_t b) {
	mprotect((void*)0x401000, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC);
	*(char*)(cave) = 0xb0;
	*(int*)(cave+1) = a;
	*(char*)(cave+2) = 0x04;
	*(int*)(cave+3) = b;
	*(char*)(cave+4) = 0xc3;
	mprotect((void*)0x401000, 0x1000, PROT_READ | PROT_EXEC);
}

unsigned int run_emulator() {
}

void calculator() {

	uint8_t n1 = 0;
	uint8_t n2 = 0;

	print_stuff("\nThe wise choice!\n", 0xdeadbeef);
	print_stuff("Provide us with two numbers!\nNumber 1: ", 0xdeadbeef);
	scanf("%hhd", &n1);
	print_stuff("Number 2: ", 0xdeadbeef);
	scanf("%hhd", &n2);
	getchar();

	print_stuff(RED"\n[*] ""Booting up CASIO-GLIBC237 emulator", 0xdeadbeef);
	boot_emulator(n1, n2);
	for (int i = 0; i < 3; i++) {
		print_stuff(".", 0xdeadbeef);
		sleep(1);
	}
	print_stuff(RED"\n[*] NOTE: ""WE ONLY COMPILE UP TO NUMBER 255 AS OF NOW.\n", 0xdeadbeef);
	sleep(1);
	print_stuff(RED"[*] ""Emulator booted.\n", 0xdeadbeef);
	sleep(1);
	print_stuff(RED"[*] ""Profiling and running calculation.\n", 0xdeadbeef);

	clock_t start_time = clock();
	unsigned int res = run_emulator();
	clock_t end_time = clock();
	double time_taken = (double)(end_time-start_time) / CLOCKS_PER_SEC;


	char* out = (char*)calloc(0x1000, sizeof(char));
	sprintf(out, GRN"[*] ""CASIO-GLIBC237: %u\n", res);
	print_stuff(out, 0xdeadbeef);
	sleep(1);
	sprintf(out, RED"[*] ""Calculation took %f seconds! Wasn't that fast?\n"clear, time_taken);
	print_stuff(out, 0xdeadbeef);
	free(out);

}

int main() {
	char buf[0x100];

	setbuf(stdin, NULL);
	setbuf(stdout, NULL);

	print_stuff("Before we start pwning, do you want to see the fastest and most efficient calculator created by me, ever?\n (y/n): ", 0xdeadbeef);
	char resp = getchar();
	getchar();

	if (resp == 'y' || resp == 'Y')
		calculator();

	print_stuff("\nOnly since I'm feeling nice, you get an easy buffer overflow for coming to NUS today!\nWhat's the magic word? ", 0xdeadbeef);
	gets(buf);
	if (strcmp(buf, "pleaseeeeeee")) {
		print_stuff("Please be more grateful.\n", 0xdeadbeef);
		exit(-1);
	}
	return 0;
}
