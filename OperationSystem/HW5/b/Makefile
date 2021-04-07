CC = gcc

all : shpeterson child

shpeterson : shpeterson.o
	gcc -o shpeterson shpeterson.o

shpeterson.o : shpeterson.c
	gcc -c -o shpeterson.o shpeterson.c

child : child.o
	gcc -o child child.o

child.o : child.c
	gcc -c -o child.o child.c

clean :
	rm *.o shpeterson child
