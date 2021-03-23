#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/stat.h>

#define MSG_SIZE 19

struct msgbuf{
	long msgtype;
	char mtext[20];
};

int main(){
	key_t key_id;
	int i=0;
	struct msgbuf sndbuf;

	key_id = msgget((key_t)1234,IPC_CREAT|0666);

	if (key_id == -1){
		perror("msgget error : ");
		return 0;
	}
	while(1){
		sndbuf.msgtype = 3;

		char tmp[20];
		fgets(tmp, MSG_SIZE, stdin);
		tmp[strlen(tmp)-1] = '\0';

		strcpy(sndbuf.mtext,tmp);
		
		if(msgsnd(key_id,(void *)&sndbuf, sizeof(struct msgbuf), IPC_NOWAIT)==-1){
			perror("msgsnd error :");
		}

		if(strcmp(tmp,"end")==0){
				break;
		}

		printf("%dth Sending message is succeed\n",i++);
	}
	return 0;
}
