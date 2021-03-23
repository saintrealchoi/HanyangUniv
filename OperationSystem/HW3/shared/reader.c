#include<stdio.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>

#define MSG_SIZE 20

struct shared_mem{
		int written;
		char data[MSG_SIZE];
};

int main(){
	int shmid;
	void *shmaddr;
	int ret;
	int check;
	struct shared_mem *mem;

	// get shared memory id
	shmid = shmget((key_t)1234,1024,IPC_CREAT|0666);
	if(shmid == -1){
		perror("shared memory access is failed\n");
		return 0;
	}
	//attach the shared memory
	shmaddr = shmat(shmid,(void*)0,0);
	if(shmaddr ==(char*)-1){
		perror("attach failed\n");
		return 0;
	}
	
	mem = (struct shared_mem *)shmaddr;
	mem->written = 1;

	while(1){	
		if(mem->written == 0){
			printf("data read from shared memory: %s\n", mem->data);
			mem->written = 1;
			if(strcmp(mem->data,"end")==0){
				break;
			}
		}
	}
	//detach the shared memory
	ret = shmdt(shmaddr);
	if(ret == -1){
		perror("detach faild\n");
		return 0;
	}
	//remove the shared memory
	ret = shmctl(shmid, IPC_RMID,0);
	if(ret == -1){
		perror("remove failed\n");
		return 0;
	}

	return 0;
}
