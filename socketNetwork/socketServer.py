import socket
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP

def generate_keys():
    private_key = RSA.generate(1024)
    public_key = private_key.publickey()
    
    return private_key, public_key

def server_program():
    session_key = Random.new().read(AES.block_size)
    host = socket.gethostname() 
    port = 9500  #  port no. above 1024

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # get instance
    server_socket.bind((host, port))  #bind host and port

    server_socket.listen(2) #configure no. of clients the server can listen to(simultaneously)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from Client: " + str(address))
    client_public_key = RSA.import_key(conn.recv(1024))
    cipher_AES = AES.new(session_key,AES.MODE_CBC,session_key)

    rsa_encrypt = PKCS1_OAEP.new(client_public_key)
    encrypt_session_key = rsa_encrypt.encrypt(session_key)
    conn.send(bytes(encrypt_session_key))
    while True:
        data = conn.recv(1024) #receive the data packet less than 1024 bytes
        if not data:
            break
        plain_text = cipher_AES.decrypt(data)
        plain_text = plain_text[:-plain_text[-1]]
        print("Sent from connected user: " + str(plain_text))
        message = bytes(input('Enter the response message-> '),"utf-8")
        
        if message.lower().strip() ==b'end':
            break
    
        pad= AES.block_size - (len(message) % AES.block_size)
        message += bytes([pad]) * pad
        cipher_AES = AES.new(session_key,AES.MODE_CBC,session_key)
        ciphertext = cipher_AES.encrypt(message)
        conn.send(ciphertext)  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()