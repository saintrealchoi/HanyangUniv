CC = g++

peterson : peterson.o
	g++ -o peterson peterson.o -lpthread

peterson.o : peterson.cpp
	g++ -c -o peterson.o peterson.cpp -lpthread

clean :
	rm *.o peterson
	
