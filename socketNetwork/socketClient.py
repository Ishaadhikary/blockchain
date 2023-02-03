import socket
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

def generate_keys():
    private_key = RSA.generate(1024)
    public_key = private_key.public_key()
    return private_key,public_key

def client_program():
    host = socket.gethostname()  
    port = 9500  # socket server port number
    private_key, public_key = generate_keys()
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    client_socket.send(public_key.export_key())
    encryption_session_key = client_socket.recv(1024)
    rsa_decrypt = PKCS1_OAEP.new(private_key)
    session_key = rsa_decrypt.decrypt(encryption_session_key)
    cipher_aes = AES.new(session_key, AES.MODE_CBC, session_key)
    message = bytes(input("Text from Client -> "),'utf-8') 

    while message.lower().strip() != 'end':
        pad = AES.block_size - (len(message)%AES.block_size)
        message += bytes([pad]) * pad
        cipher_aes = AES.new(session_key, AES.MODE_CBC, session_key)
        ciphertext= cipher_aes.encrypt(message)
        print("Encrypted Message:", ciphertext)
        client_socket.send(ciphertext)  # send message
        data = client_socket.recv(1024)  
        if not data:
            break
        cipher_aes = cipher_aes = AES.new(session_key, AES.MODE_CBC, session_key)
        plain_response = cipher_aes.decrypt(data)
        plain_response = plain_response[:- plain_response[-1]]
        print('Message Received from server: ' + str(plain_response))  
        message = bytes(input("Enter the message-> "), "utf-8")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()