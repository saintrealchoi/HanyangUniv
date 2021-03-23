CC = gcc

all : reader writer

reader : reader.o
	gcc -o reader reader.o
reader.o : reader.c
	gcc -c -o reader.o reader.c

writer : writer.o
	gcc -o writer writer.o
writer.o : writer.c
	gcc -c -o writer.o writer.c

clean :
	rm *.o writer reader
