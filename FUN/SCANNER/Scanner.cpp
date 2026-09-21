#include <iostream>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string>
#include <cstring>
#include <sys/time.h>
#include <netdb.h>

extern "C" {
    int check_path_cpp(const char* hostname, int port, const char* path) {
        struct addrinfo hints, *res;
        std::memset(&hints, 0, sizeof(hints));
        hints.ai_family = AF_INET;
        hints.ai_socktype = SOCK_STREAM;

        if (getaddrinfo(hostname, std::to_string(port).c_str(), &hints, &res) != 0) {
            return 0;
        }

        int sock = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
        if (sock < 0) {
            freeaddrinfo(res);
            return 0;
        }

        struct timeval timeout;
        timeout.tv_sec = 1;
        timeout.tv_usec = 0;
        setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &timeout, sizeof(timeout));
        setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));

        if (connect(sock, res->ai_addr, res->ai_addrlen) < 0) {
            close(sock);
            freeaddrinfo(res);
            return 0;
        }

        freeaddrinfo(res);

        std::string request = "HEAD " + std::string(path) + " HTTP/1.1\r\nHost: " + std::string(hostname) + "\r\nConnection: close\r\n\r\n";
        if (send(sock, request.c_str(), request.length(), 0) < 0) {
            close(sock);
            return 0;
        }

        char response;
        std::memset(response, 0, sizeof(response));
        int bytes_received = recv(sock, response, sizeof(response) - 1, 0);
        close(sock);

        if (bytes_received > 0) {
            if (std::strstr(response, "HTTP/1.1 200") != nullptr || 
                std::strstr(response, "HTTP/1.1 30") != nullptr || 
                std::strstr(response, "HTTP/1.1 403") != nullptr) {
                return 1;
            }
        }
        return 0;
    }
}
