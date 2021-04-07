#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <string.h>
#include <unistd.h>

#define COUNTING_NUMBER 2000000

struct smStruct{
		int processidassign;
		int turn;
		int flag[2];
		int critical_sectionvariable;
};

//using Peterson Algorithm
void lock(struct smStruct *mem,int self){
	mem->flag[self] = 1;
	mem->turn = 1-self;
	while(mem->flag[1-self]==1 && mem->turn == 1-self);
}

void unlock(struct smStruct *mem, int self){
		mem->flag[self] = 0;
}

int main(){
	int localcount =0;
	int i;
	int Myorder;
	int shmid;
	int ret;
	void *shmaddr;
	struct smStruct *mem;
	

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
	mem= (struct smStruct *)shmaddr;
	
	//Decide order by processidassign which is in the shared memory
	Myorder = mem->processidassign++;
	
	//Print order, pid
	printf("Myorder = %d,process pid = %d\n",Myorder,getpid());

	for(i=0;i<COUNTING_NUMBER;i++){
		localcount++;
		lock(mem,Myorder);
		mem->critical_sectionvariable++;
		unlock(mem,Myorder);
	}

	//when finishing the process, print local count value
	printf(" child finish! local count = %d\n",localcount);

	//detach the shared memory
	ret = shmdt(shmaddr);
	if(ret == -1){
		perror("detach failed\n");
		return 0;
	}

	return 0;
}
