CC = g++

main: main.o satellite.o
	$(CC) -O2 -o main main.o satellite.o

main.o: main.cpp
	$(CC) -c main.cpp

satellite.o: satellite.h