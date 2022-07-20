#include "mbedtls/cipher.h"
#include "mbedtls/dhm.h"
#include "mbedtls/md.h"
#include "mbedtls/des.h"

int main()
{
	/*
	aes_test(MBEDTLS_CIPHER_AES_128_ECB);
	return 1;
	*/

	/*
	//调用 DES，加密你的学号
	des_test(MBEDTLS_CIPHER_DES_ECB);
	return 1;
	*/
   
	/*
	//调用 RSA，加密你的学号
	mbedtls_rsa_test();
	return 1;
	*/

	/*
	//调用 RSA，对你的学号进行签名
	mbedtls_rsa_sign_test();
    return 1;
	*/

	/*
	//利用 DH 密钥协商协议协商一个密钥
	mbedtls_dhm_test();
    return 1;
	*/

	/*
	//并利用 SHA256 对协商的秘密信息做哈希，得到一个密钥
	mbedtls_shax_test(MBEDTLS_MD_SHA512);
    return 1;
	*/

	/*
	//利用这个密钥和 ARIA 密码算法对你的学号进行加密、解密
	mbedtls_aria_test(MBEDTLS_CIPHER_ARIA_256_ECB);
	return 1;
	*/

	/*
	密码设计
	mbedtls_des();
	return 1;
	*/
	
	mbedtls_des();

	/*
	88B8BD1D171F2F927BDA25212ABE4A8C411E9CE2C5973BAB05848753CA3286E32DA20FE65FA5F950BFB98A8AD65AC5E1D353A527B8A2E420D143683FF789A096217FCB955C923A5A446B35F1178ECF8E04EAB6C6B7F9831B7BFF079A3795C7CC0CB1AB27D0EA9EA9BB70A26DCB8BE22B44CF8601A3A8F10C0FA06C0936AE3BCBC4B37A88C37F89C976A05C96BE7803E62C5EE31006569A2FCF97A45042A56D8D9F43CE35160E478AD2303E3B74EC85E0BE05E804E44C97B384C6C31B48EC1BB9A9956DAB1958FD8AE7EBE34004F2BE64EF4FB27A18BB94238FD08F94D8C74B0A770E770872B0B3C527598E9C7E9E490A8A8FC6238317262F96A0975B4B85F162
	*/
	/*
	b9d94a29ec1dd74b5f9cad303e8ed8c17f9eaf8c71b21d4301d457d23e8e24a0
    */

	/*
	source_context:202000460007
    buf:
        32 30 32 30 30 30 34 36 30 30 30 37
    cipher name:ARIA-256-ECB block size is:16
    buf:
        0E BF F9 FB 9B 7E 5D 91 B3 F3 8B B2 14 9A B6 60
	*/
}

