CC = gcc

all : producer consumer

producer : producer.o
	gcc -o producer producer.o
producer.o : producer.c
	gcc -c -o producer.o producer.c

consumer : consumer.o
	gcc -o consumer consumer.o
consumer.o : consumer.c
	gcc -c -o consumer.o consumer.c

clean : 
	rm *.o producer consumer
