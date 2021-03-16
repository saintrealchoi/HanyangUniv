CC = gcc

child1.o : child1.c
	gcc -c child1.o child1.c

child1 : child1.o
	gcc -o child1 child1.o


child2 : child2.o
	gcc -o child2 child2.o

child2.o : child2.c
	gcc -c child2.o child2.c

fork : fork.o
	gcc -o fork fork.o

fork.o : fork.c
	gcc -c fork.o fork.c

clean : 
	rm *.o child1 child2


