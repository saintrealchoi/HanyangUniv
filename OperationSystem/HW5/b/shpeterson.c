#include<stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>

#define COUNTING_NUMBER 2000000

struct smStruct{
		int processidassign;
		int turn;
		int flag[2];
		int critical_sectionvariable;
};

int main(){
	pid_t cpid1,cpid2,endpid1,endpid2;
	int state;
	int shmid;
	int ret;
	void *shmaddr;
	struct smStruct *mem;

	// get shared memory id
	shmid = shmget((key_t)1234,1024,IPC_CREAT|0666);
	if(shmid <0){
			perror("shmget");
			return 0;
	}
	
	// attach the shared memory
	shmaddr = shmat(shmid,(void*)0,0);
	if(shmaddr == (char*)-1){
		perror("attach failed\n");
		return 0;
	}

	// init the shared memory
	mem = (struct smStruct *)shmaddr;
	mem->turn=0;
	mem->processidassign=0;
	mem->flag[0] = 0;
	mem->flag[1] = 0;
	mem->critical_sectionvariable=0;
	
	if((cpid1=fork())==0){ // Generate process and execute child
		execl("./child",0); // execute child
		printf("This should not be executed.\n");// this line should not be executed
	}

	if((cpid2=fork())==0){ // Generate another process and execute child
		execl("./child",0); // execute child
		printf("This should not be executed too.\n"); // this line should not be executed
	}
	
	//wait until child process finished
	while(1){
		endpid1 = waitpid(cpid1,&state,WNOHANG);
		endpid2 = waitpid(cpid2,&state,WNOHANG);
		if(endpid1!=0&&endpid2!=0){
			break;
		}
	}
	// print cricical section variable, expected value
	printf("Acutal Count: %d | Expected Count : %d\n",mem->critical_sectionvariable,COUNTING_NUMBER*2);
	
	//detach the shared memory
	ret = shmdt(shmaddr);
	if(ret == -1){
		perror("detach failed\n");
		return 0;
	}
	
	//remove the shraed memory
	ret = shmctl(shmid, IPC_RMID,0);
	if(ret == -1){
		perror("remove failed\n");
		return 0;
	}
	return 0;
}
