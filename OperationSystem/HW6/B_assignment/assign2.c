#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>

#define people_num 6

sem_t chopstick[people_num];

void *philosopher(void *arg);
int func(void* arg);

int main()
{
    int i;
    pthread_t thread_id[people_num];
	//init
    for (i = 0; i < people_num; i++) {
        sem_init(&chopstick[i], 0, 1);
    }
	//create
    for (i = 0; i < people_num; i++) {
        pthread_create(&thread_id[i], NULL, philosopher, (void *)i);
    }
	//wait
    for (i = 0; i < people_num; i++) {
        pthread_join(thread_id[i], NULL);
    }
	//destory semaphore
    for (i = 0; i < people_num; i++)
    {
        sem_destroy(&chopstick[people_num]);
    }

}

void *philosopher(void *arg)
{
    int own_num = (int)arg;
    int right = (own_num + 1) % people_num;

	//짝수번째 철학자일 경우 오른손부터 집는다.
    if (own_num % 2 == 0) {
        sem_wait(&chopstick[right]);
        printf("#[%d] philosopher picks up %d chopstick with his right hand\n", own_num, right);
        sem_wait(&chopstick[own_num]);
        printf("#[%d] philosopher picks up %d chopstick with his left hand\n", own_num, own_num);
        //다 집었을 시 먹기시작
		printf("  #[%d] philosopher is starting eating.\n",own_num);
        sleep(1);
		//다먹음
        printf("  #[%d] philosopher finishes eating.\n",own_num);
        //다먹었을 시 양손을 모두 내려놓는다.
		sem_post(&chopstick[own_num]);
        sem_post(&chopstick[right]);

    }
	//홀수번째 철학자일 경우 왼쪽손부터 집는다.
    else {
		//짝수와 마찬가지로 진행
        sem_wait(&chopstick[own_num]);
        printf("#[%d] philosopher picks up %d chopstick with his left hand\n", own_num, own_num);
        sem_wait(&chopstick[right]);
        printf("#[%d] philosopher picks up %d chopstick with his right hand\n", own_num, right);
        printf("  #[%d] philosopher is starting eating\n", own_num);
        sleep(2);
        printf("  #[%d] philosopher finishes eating\n", own_num);
        sem_post(&chopstick[right]);
        sem_post(&chopstick[own_num]);
    }
}
