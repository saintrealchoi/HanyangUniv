#include <stdio.h>
#include <stdlib.h>

int main(){
	char str[20];
	char *pStr;
	for(int i=0; i< 6; i++){
		sleep(2);
		FILE* pFile = fopen("test.txt","r");
		pStr = fgets( str, sizeof(str), pFile );
		printf("%s",str);
		fclose(pFile);
	}
	exit(0);
}
