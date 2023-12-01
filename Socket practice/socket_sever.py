import socket
import threading

def link_handler(link, client:tuple):
    '''
    线程需要执行的函数，即需要处理的客户端连接
    link: link running
    client: socket of client,should be a tuple
    return:None
    '''
    
    while True:
        client_data = link.recv(1024).decode()
        
        #print out the client message
        print('>> recevie a message from [%s:%s] :' % (client[0], client[1]), 
        'Message is [%s]' % (client_data) )

        if client_data == 'exit':
            print('>> Close the connect with [%s:%s]' % (client[0], client[1]))
            break
        print('>> Message from [%s:%s]' % (client[0], client[1]))
        link.sendall('>> Server has recived your massage'.encode())
    link.close()

#get host ip adress
_local_ip = socket.gethostbyname(socket.getfqdn())

ip_port = (_local_ip, 13400)
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.bind(ip_port)
sk.listen(10)

print('>> Server socket [%s:%s]inited, waitting for connecing' % (ip_port[0], 
                                                                    ip_port[1]))

if __name__ == '__main__':
    while True:
        #waitting for connection from client, should be block 
        conn, address = sk.accept() 

        #inite a new thread when come in a client

        t = threading.Thread(target=link_handler, args=(conn, address))
        t.start()

