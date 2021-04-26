#include <stdio.h>
#include <semaphore.h>
#include <pthread.h>

void producer();
void consumer();

int buffer[100];
int rear = -1;
int front = -1;

sem_t empty_slot;
sem_t data_items;

int main(){
	int i;

	sem_init(&empty_slot,0,100);
	sem_init(&data_items,0,0);

	pthread_t thread_producer,thread_consumer;
	pthread_create(&thread_producer, NULL, (void *)&producer, NULL);
	pthread_create(&thread_consumer, NULL, (void *)&consumer, NULL);

	pthread_join(thread_producer, NULL);
	pthread_join(thread_consumer, NULL);

	sem_destroy(&empty_slot);
	sem_destroy(&data_items);
}

void producer(){
	int i;
	int empty_slot_value, data_items_value;
	for(i =0; i < 1000; i++){
			printf("producer data = %d\n", i);

			sem_wait(&empty_slot);

			rear++;
			rear %= 100;
			buffer[rear] = i;

			sem_post(&data_items);
			sem_getvalue(&empty_slot, &empty_slot_value);
			sem_getvalue(&data_items, &data_items_value);
			printf("empty_slot=%d\tdata_items=%d\n",empty_slot_value,data_items_value);
	}
}

void consumer(){
	int i,data;
	int empty_slot_value, data_items_value;
	
	for (i =0; i<1000; i++){
		sem_wait(&data_items);

		front++;
		front %= 100;
		data = buffer[front];

		sem_post(&empty_slot);

		sem_getvalue(&empty_slot, &empty_slot_value);
		sem_getvalue(&data_items, &data_items_value);

		printf("\t\tconsumer data = %d, empty_slot = %d\tdata_items=%d\n", data,empty_slot_value,data_items_value);
	}
}
