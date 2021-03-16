#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>

int main(){
	pid_t cpid1,cpid2,endpid1,endpid2;
	int state;
	
	printf("Waiting for child Processes\n");
	
	if((cpid1=fork())==0){
		execl("./child1",0);
		printf("??\n");
	}

	if((cpid2=fork())==0){
		execl("./child2",0);
		printf("?????\n");
	}
	
	while(1){
		endpid1 = waitpid(cpid2,&state,WNOHANG);
		endpid2 = waitpid(cpid1,&state,WNOHANG);	
		if(endpid1!=0&&endpid2!=0){
			break;
		}
	}
	printf("Child processes are exit (0) (0)\n");
}
