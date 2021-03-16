#include <stdio.h>
#include <stdlib.h>

int main(){
	//FILE* pFile= fopen("test.txt", "w");
	int num = 0;
	char str[20];
	for(int i =0 ; i< 12; i++){
		sleep(1);
		FILE* pFile = fopen("test.txt","w");
		printf("Child1 wrote %d.\n",num);
		fprintf(pFile,"%d\n",num++);
		//printf("Child1 wrote %d.\n",num);
		fclose(pFile);
	}
	//fclose(pFile);
	exit(0);

}
