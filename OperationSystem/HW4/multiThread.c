#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define ARGUMENT_NUMBER 20

long long result = 0;
void *ThreadFunc(void *n){
	long long temp=0; // 연산결과를 저장할 임시변수 선언
	long long i;
	long long number = *((long long *)n);
	printf("number = %lld\n",number);
	for(i = 0 ; i <25000000; i++)
	{
			temp += number; // 연산결과 저장
	}
	result += temp; // 결과값에 연산결과 덧셈
}

int main(void){
	pthread_t threadID[ARGUMENT_NUMBER]; // 20개의 스레드를 생성
	long long argument[ARGUMENT_NUMBER];
	long long i;

	for(i = 0 ; i <ARGUMENT_NUMBER ; i++){
		argument[i] = i;
	}

	for (i=0; i < ARGUMENT_NUMBER; i++){
		pthread_create(&(threadID[i]), NULL, ThreadFunc, (void *)&argument[i]);//20개의 스레드를 각각의 argument와 함께 생성
	}

	printf("Main Thread is waiting for Child Thread!\n"); // 위의 스레드 생성이 끝날 시 출력

	for(i = 0 ; i <ARGUMENT_NUMBER ;i++){
		pthread_join(threadID[i],NULL); // 스레드가 끝날때까지 기다림
	}

	printf("result = %lld \n",result); //결과 값 출력
	return 0;
}
