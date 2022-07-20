#include "mbedtls/des.h"
#include <stdio.h>
#include <string.h>
#include <stdint.h>

/* Private Key */
uint8_t key_des[8] = {
    0x06, 0xa9, 0x21, 0x40, 0x36, 0xb8, 0xa1, 0x5b
    //0x51, 0x2e, 0x03, 0xd5, 0x34, 0x12, 0x00, 0x06
};


static void dump_buf(uint8_t* buf, uint32_t len)
{
    int i;

    printf("buf:");

    for (i = 0; i < len; i++) {
        printf("%s%02X%s", i % 16 == 0 ? "\r\n\t" : " ",
            buf[i],
            i == len - 1 ? "\r\n" : "");
    }
}

int mbedtls_des()
{
    int ret;
    uint8_t output_buf[64];
    //des加密长度为64bit，分组两次加密
    const char* input = "Wang Fangqi";//明文

    mbedtls_des3_context ctx;

    /* 1. init cipher structuer */
    mbedtls_des_init(&ctx);

    /* 2. set key */
    ret=mbedtls_des_setkey_enc(&ctx, (unsigned char*)key_des);
    if (ret != 0) {
        goto exit;
    }


    int n = strlen(input);
    if (n % 8 == 0)
    {
        n = n / 8;
    }
    else
    {
        n = n / 8 + 1;
    }
    for (int i = 0; i < n; i++)
    {
        /* 3. encryption*/
        ret = mbedtls_des_crypt_ecb(&ctx, (unsigned char*)(input + 8 * i),(output_buf + 8 * i));
        if (ret != 0) {
            goto exit;
        }
    }

    printf("\r\nsource_context:%s\r\n", input);
    dump_buf((uint8_t*)input, strlen(input));
    dump_buf(output_buf,64);

exit:
    /* 8. free cipher structure */
    mbedtls_des_free(&ctx);

    return ret;
}