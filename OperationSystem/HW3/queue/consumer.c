#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <fcntl.h>

struct msgbuf{
	long msgtype;
	char mtext[20];
};

int main(int argc, char **argv){
	key_t key_id;
	int i=0;
	struct msgbuf rsvbuf;
	int msgtype=3;

	key_id = msgget((key_t)1234, IPC_CREAT|0666);

	if(key_id == -1){
		perror("msgget error :");
		return 0;
	}
	while(1){
		if(msgrcv(key_id,(void *)&rsvbuf, sizeof(struct msgbuf),msgtype,0)==-1){
			perror("msgrcv error :");
		}

		else{
			if(strcmp(rsvbuf.mtext,"end")==0){
					break;
			}
			printf("The %dth received message is : %s\n",i++,rsvbuf.mtext);
		}
	}
	return 0;
}
