#!/bin/bash

qemu-system-x86_64 \
	-m 1024 \
	-kernel ./bzImage \
	-initrd ./initramfs.cpio.gz \
	-nographic \
	-monitor none \
	-no-reboot \
	-cpu kvm64,+smep,+smap \
	-smp 1 \
	-append "console=ttyS0 kaslr kpti=1 quiet panic=1"
