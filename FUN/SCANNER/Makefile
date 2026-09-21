CC = g++
CFLAGS = -shared -fPIC -O3
TARGET = libscanner.so
SRC = Scanner.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)
