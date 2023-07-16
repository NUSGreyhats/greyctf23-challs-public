#include <linux/kernel.h>
#include <linux/panic.h>
#include <linux/fs.h>
#include <linux/module.h>
#include <linux/miscdevice.h>
#include <linux/slab.h>
#include <linux/string.h>

// #include <linux/panic.h>
// #include <linux/list.h>
// #include <linux/types.h>
// #include <linux/uaccess.h>
// #include <linux/mutex.h>
// #include <linux/random.h>
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Elma");
MODULE_DESCRIPTION("Ask and you shall receive (or not).");

static int __init dean_init(void) {
	unsigned long addr = (unsigned long)kmalloc(0x1000, GFP_ATOMIC);
	addr &= 0xFFFFFFFFFFFF0000;
	while (1) {
		if (!strncmp((char*)addr, "grey{", 4)) {
			printk("found flag at %llx", addr);
			printk("%s", (char*)addr);
			printk("flush");
			break;
		}
		addr += 0x1000;
	}
    return 0;
}

static void __exit dean_exit(void) {
	return;
}

module_init(dean_init);
module_exit(dean_exit);
