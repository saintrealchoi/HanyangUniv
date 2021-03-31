gcc = CC

multiThraed : multiThread.o
	gcc -o multiThread multiThread.o -lpthread

multiThread.o : multiThread.c
	gcc -c -o multiThread.o multiThread.c -lpthread

clear : 
	rm *.o multiThread
