#  -*-  coding:utf-8  -*-
import socket
import time
import psutil


'''
Notification:
1. According to { if "以太网" in name or "eth" in name }, make sure your have one 
unique Ethernet connection on your equipment at the moment
2. Make sure the Protocol of vehicle, IVP4 or IVP6, IVP4 verificated;
3. Notice in the vehicle announcement message's 31th and 32th byte, if not 0x00 
or none, need additional message to connect

'''

'''
# Why there are more than 1 port for the flowing UDP adress IP? Does that main "bindding"?
connections_list = psutil.net_connections(kind='udp')
connections = [conn for conn in connections_list]

for conn in connections:
    if '169.254.225.160' in conn.laddr or '169.254.225.160' in conn.raddr:
        
        print(conn)
#sconn(fd=-1, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_DGRAM: 2>, laddr=addr(ip='169.254.225.160', port=137), raddr=(), status='NONE', pid=4)
#sconn(fd=-1, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_DGRAM: 2>, laddr=addr(ip='169.254.225.160', port=1900), raddr=(), status='NONE', pid=3288)
#sconn(fd=-1, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_DGRAM: 2>, laddr=addr(ip='169.254.225.160', port=59460), raddr=(), status='NONE', pid=3288)
#sconn(fd=-1, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_DGRAM: 2>, laddr=addr(ip='169.254.225.160', port=138), raddr=(), status='NONE', pid=4)
'''


class Doip_client():
    def __init__(self):
        self.TCPConnected = None
        self._local_addr, self._local_ip, self.ethernet_name = None, None, None
        self.vin, self.tar_ip, self.tar_port = None, None, None

        self._local_port = 13400
        self._TCP_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udpServer = None


    def get_eth_addr(self, ivp: str):
        '''return a activated Ethernet connection IPV4 IP address'''
        io_stats = psutil.net_io_counters(pernic=True) #connection flowing or not
        for name, stats in io_stats.items():
            if "以太网" in name or "eth" in name:
                if stats.bytes_sent > 500 and stats.bytes_recv > 500:
                    # print(f"Interface {name}:")   #Interface 以太网 9:
                    tar_ethernet_name = name    # The activated Ethernet connection

                    net_card_dic = psutil.net_if_addrs() # Return the addresses associated to each
                    #NIC (network interface card) installed
                    for adapter in net_card_dic:
                        if adapter in tar_ethernet_name:    #the flowing connected Ethernet
                            snicList = net_card_dic[adapter]
                            mac = 'mac address'
                            ipv4 = 'ipv4 address'
                            ipv6 = 'ipv6 address'
                            for snic in snicList:
                                if snic.family.name in {'AF_LINK', 'AF_PACKET'}:
                                    mac = snic.address
                                elif snic.family.name == 'AF_INET':
                                    ipv4 = snic.address
                                elif snic.family.name == 'AF_INET6':
                                    ipv6 = snic.address
                            # print('%s, %s, %s, %s' % (adapter, mac, ipv4, ipv6))
                            #以太网 9, 00-E0-4C-77-17-2F, 169.254.225.160, fe80::13e2:ca27:a5b5:874e
                            if ivp == 'IVP4':
                                self._local_ip, self.ethernet_name = ipv4, tar_ethernet_name
                            elif ivp == 'IVP6':
                                self._local_ip, self.ethernet_name = ipv6, tar_ethernet_name 

    def find_vehicle(self, udp_addr, ethernet_name):
        '''Through UDP ACK to find the doip vehicle and print the VIN and addr'''
        tried = 1
        self.udpServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #IVP4
        self.udpServer.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)   #set the over time
        self.udpServer.bind(udp_addr)  
        print(">> Waiting for connection at %s, %sth trying...." % (udp_addr[0], tried))
        while tried <= 5:
            try:
                self.udpServer.settimeout(2)
                pri_data, addr_veh = self.udpServer.recvfrom(1024)
                if pri_data:
                    vin = str(pri_data[7: 25])[3:20]
                    print(">> %s found from ip %s, port %s with Ethernet %s" \
                        %(vin, addr_veh[0], addr_veh[1], ethernet_name))
                    return vin, addr_veh[0], addr_veh[1]
            except socket.timeout:
                print('## %s times to find ACK from avalibale vehicle' % (tried))
                tried += 1
                continue

            if tried == 5:
                print(">> %s times tried, no available connection" % (tried))

    def ConnectToServer(self):
        self.get_eth_addr('IVP4')
        self._local_addr = (self._local_ip, self._local_port)
        try:
            self.vin, self.tar_ip, self.tar_port = self.find_vehicle(self._local_addr, self.ethernet_name)
        except TypeError:
            print('## No available vehicle..')

            self._TCP_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        '''creat socket and connect to server'''

        try:
            self._TCP_Socket.bind(self._local_addr)
            self._TCP_Socket.connect((self.tar_ip, self.tar_port))
            self.TCPConnected = 1
            time.sleep(0.2)

        except Exception as err:
                print( "Unable to connect to Server. Socket failed with error: %s" % (err))

    def DisconnectToServer(self):
        '''shut done the TCP connection'''
        if self._TCP_Socket:
            try:
                self._TCP_Socket.shutdown(1)
                self._TCP_Socket.close()
                self.TCPConnected = 0
            except Exception as err:
                print('## can\'t shutdown/close the socket with %s' % (err))

    def SendTcpMessage(self, message:str):
        if self.TCPConnected:
            self.pri_s_message = message
            by_message = bytes.fromhex(message)
            self._TCP_Socket.send(by_message)
            time.sleep(0.2)

    def ReceiveTCPMessage(self):
        if self.TCPConnected:
            self.pri_r_message = self._TCP_Socket.recv(1024)

    def CheckConnection(self):
        if self.TCPConnected:
            return 1
        else:
            return 0

    def ttt(self):
        print("testing in the client class")
My_client=Doip_client()
# My_client.ConnectToServer()



 