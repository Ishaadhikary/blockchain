import socket


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 9500  #  port no. above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  #bind host and port

    server_socket.listen(2) #configure no. of clients the server can listen to(simultaneously)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    
    while True:
        data = conn.recv(1024).decode() #receive the data packet less than 1024 bytes
        if not data:
            break
        print("Sent from connected user: " + str(data))
        data = input('Enter the message-> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()