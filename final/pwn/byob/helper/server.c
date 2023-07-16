#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include "quickjs-libc.h"

/* gcc -O0 -D _GNU_SOURCE -I . -o server server.c ./libquickjs.a -lm -ldl -lpthread -g */
#define MIN(a, b) ((a) < (b) ? (a) : (b))

static JSContext *JS_NewCustomContext(JSRuntime *rt)
{
  JSContext *ctx = JS_NewContextRaw(rt);
  if (!ctx)
    return NULL;
  JS_AddIntrinsicBaseObjects(ctx);
  JS_AddIntrinsicDate(ctx);
  JS_AddIntrinsicEval(ctx);
  JS_AddIntrinsicStringNormalize(ctx);
  JS_AddIntrinsicRegExp(ctx);
  JS_AddIntrinsicJSON(ctx);
  JS_AddIntrinsicProxy(ctx);
  JS_AddIntrinsicMapSet(ctx);
  JS_AddIntrinsicTypedArrays(ctx);
  JS_AddIntrinsicPromise(ctx);
  JS_AddIntrinsicBigInt(ctx);
  return ctx;
}

void setup() {
  // Disable buffering on stdin
  setvbuf(stdin, NULL, _IONBF, 0);

  // Disable buffering on stdout
  setvbuf(stdout, NULL, _IONBF, 0);

  // Set an alarm to terminate the program after a specified time
  alarm(60);  // Set the timeout to 60 seconds
}

const char BANNER[] = "\n ____  _  _  _____  ____ \n(  _ \\( \\/ )(  _  )(  _ \\\n ) _ < \\  /  )(_)(  ) _ <\n(____/ (__) (_____)(____/\n";

int main(int argc, char **argv)
{
  JSRuntime *rt;
  JSContext *ctx;
  u_int32_t size = 0, bytes_read = 0;
  u_int8_t *bytecode;

  setup();

  puts(BANNER);
  printf("[+] Bytecode size: ");
  if (scanf("%u", &size) < 1) {
      printf("[!] Invalid size.");
      return -1;
  }
  bytecode = malloc(size);

  printf("[+] Enter exactly %u bytecode bytes\n", size);
  while (bytes_read < size) {
    bytes_read += read(STDIN_FILENO, &bytecode[bytes_read], MIN(0x1000, size - bytes_read));
  }

  puts("[+] Running your code now");

  rt = JS_NewRuntime();
  js_std_set_worker_new_context_func(JS_NewCustomContext);
  js_std_init_handlers(rt);
  ctx = JS_NewCustomContext(rt);
  js_std_add_helpers(ctx, argc, argv);
  js_std_eval_binary(ctx, bytecode, size, 0);
  js_std_loop(ctx);
  JS_FreeContext(ctx);
  JS_FreeRuntime(rt);

  puts("[+] Done!");
  return 0;
}
