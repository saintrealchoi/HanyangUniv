#include<stdio.h>
#include<pthread.h>
#include<semaphore.h>

//semaphore
sem_t read;
sem_t write;

//check reader number
int readers= 0;

void reader();
void *writer(void *arg);

//critical section
int cur_writer=0;
int cur_count=0;

int main(){
	int i;

	//init
	sem_init(&read,0,2);
	sem_init(&write,0,1);

	pthread_t readerThread[2],writerThread[5];
	
	//create thread
	for(i=0;i<2;i++){
		pthread_create(&readerThread[i],NULL,reader,NULL);
	}
	for(i=0;i<5;i++){
		pthread_create(&writerThread[i],NULL,writer,(void *)i);
	}

	//wait thread
	for(i=0;i<5;i++){
		pthread_join(writerThread[i],NULL);
	}
	for(i=0;i<2;i++){
		pthread_join(readerThread[i],NULL);
	}
	
	//delete semaphore
	sem_destroy(&write);
	sem_destroy(&read);
}

void *writer(void *arg){
	int i=0;
	int writer_id=(int)arg;
	

	for(i=0;i<100000;i++){
		usleep(100000);	
		//wait, writer가 접근하고 있을 동안 어떠한 reader/writer도 접근할 수 없음
		sem_wait(&write);
		//critical section
		cur_writer = writer_id;
		cur_count=i;
		//signal, write semaphore의 변수 증가
		sem_post(&write);
	}
}

void reader(){
	int i=0;
	
	for(i =0; i < 100000 ; i++){
		usleep(30000);
		// race condition을 막기위해 reader수 측정
		sem_wait(&read);
		readers++;
		// 첫번째 reader라면 만약 writer가 접근중인지 확인 후 wait
		if(readers ==1)
			sem_wait(&write);
		// reader수 증가 확인
		sem_post(&read);
		//critical section
		printf("The most current writer id = [%d], count = [%d]\n",cur_writer,cur_count);
		//reader수 감소
		sem_wait(&read);
		readers--;
		//마지막 reader일 경우 writer진행
		if(readers ==0)
			sem_post(&write);
		sem_post(&read);

	}
}
