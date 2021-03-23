CC = gcc

all : read write

read : read.o
	gcc -o read read.c

read.o : read.c
	gcc -c -o read.o read.c

write : write.o
	gcc -o write write.c

write.o : write.c
	gcc -c -o write.o write.c

clean :
	rm *.o read write named_pipe_file
