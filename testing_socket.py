import psutil
connections = psutil.net_connections(kind='udp')
established_connections = [conn for conn in connections]

for conn in established_connections:
    if '169.254.225.160' in conn.laddr or '169.254.225.160' in conn.raddr:
        
        print(conn)
'''sconn(fd=-1, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_DGRAM: 2>, laddr=addr(ip='169.254.225.160', port=137), raddr=(), status='NONE', pid=4)
sconn(fd=-1, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_DGRAM: 2>, laddr=addr(ip='169.254.225.160', port=1900), raddr=(), status='NONE', pid=3288)
sconn(fd=-1, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_DGRAM: 2>, laddr=addr(ip='169.254.225.160', port=59460), raddr=(), status='NONE', pid=3288)
sconn(fd=-1, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_DGRAM: 2>, laddr=addr(ip='169.254.225.160', port=138), raddr=(), status='NONE', pid=4)'''

io_stats = psutil.net_io_counters(pernic=True) #connection flowing or not

for name, stats in io_stats.items():
    if "以太网" in name or "eth" in name:
        if stats.bytes_sent > 500 and stats.bytes_recv > 500:
            print(f"Interface {name}:")
            # print(f"  Bytes sent: {stats.bytes_sent}")
            # print(f"  Bytes received: {stats.bytes_recv}")
            # print(f"  Packets sent: {stats.packets_sent}")
            # print(f"  Packets received: {stats.packets_recv}")
            '''Interface 以太网 9:
    Bytes sent: 86572
    Bytes received: 19596
    Packets sent: 557'''
            tar_ethernet_name = name

def PrintNetIfAddr():
    r""" 打印多网卡 mac 和 ip 信息 """
    dic = psutil.net_if_addrs()
    for adapter in dic:
        if adapter in tar_ethernet_name:    #the flowing connected Ethernet
            snicList = dic[adapter]
            mac = '无 mac 地址'
            ipv4 = '无 ipv4 地址'
            ipv6 = '无 ipv6 地址'
            for snic in snicList:
                if snic.family.name in {'AF_LINK', 'AF_PACKET'}:
                    mac = snic.address
                elif snic.family.name == 'AF_INET':
                    ipv4 = snic.address
                elif snic.family.name == 'AF_INET6':
                    ipv6 = snic.address
            print('%s, %s, %s, %s' % (adapter, mac, ipv4, ipv6))
            #以太网 9, 00-E0-4C-77-17-2F, 169.254.225.160, fe80::13e2:ca27:a5b5:874e
PrintNetIfAddr()                           
