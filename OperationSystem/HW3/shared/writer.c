#include<stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <string.h>

#define MSG_SIZE 20

struct shared_mem{
	int written;
	char data[MSG_SIZE];
};

int main(){
	int shmid;
	int ret;
	void *shmaddr;
	char tmp[20];
	struct shared_mem *mem;
	

	//make a shared memroy
	shmid = shmget((key_t)1234,1024,IPC_CREAT|0666);
	if(shmid <0){
		perror("shmget");
		return 0;
	}

	//attach the shared memory
	shmaddr = shmat(shmid,(void*)0,0);
	if(shmaddr == (char *)-1){
		perror("attach failed\n");
		return 0;
	}
	mem= (struct shared_mem *)shmaddr;
	
	while(1){
		if(mem->written == 1){
			fgets(tmp, MSG_SIZE, stdin);
			tmp[strlen(tmp)-1] = '\0';
			strcpy(mem->data, tmp);
			mem->written = 0;
			if(strcmp(mem->data,"end")==0){
					break;
			}
		}
	}
	//detach the shared memory
	ret = shmdt(shmaddr);
	if(ret == -1){
		perror("detach failed\n");
		return 0;
	}

	return 0;
}
