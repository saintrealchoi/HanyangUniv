#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>

#define MSG_SIZE 80
#define PIPENAME "./named_pipe_file"

int main(){
    char msg[MSG_SIZE];
    int fd;
    int ret,i;

    //open the named pipe
    fd = open(PIPENAME, O_WRONLY);
    if(fd<0){
        printf("Open Failed\n");
        return 0;
    }

	printf("Hello,this is A process. Ill give the data to B.\n");
	
	// iterate until write "end"
	while(1)
    {
		char tmp[MSG_SIZE];
		fgets(tmp, MSG_SIZE, stdin);
		tmp[strlen(tmp)-1] = '\0';
		snprintf(msg,sizeof(msg),tmp);
		ret = write(fd,msg,sizeof(msg));
        if(ret <0)
        {
            printf("Write failed\n");
            return 0;
        }
		if(strcmp(msg,"end")==0){
				break;
		}

    }
    return 0;
}
