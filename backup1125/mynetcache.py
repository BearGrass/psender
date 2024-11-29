from scapy.all import *

class NETCACHE:
    def __init__(self) -> None:
        self.h1 = netcache_H1()
        # self.h2 = netcache_H2()

class netcache_H1(Packet):
    name = "netcache_H1"
    fields_desc = [ BitField("op", 0x00, 8),
                    BitField("seq",0x01, 32),
                    BitField("key",1,16),
                    BitField("value",666,512),
    ]