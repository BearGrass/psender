from scapy.all import *
from enum import Enum

class NetworkType(Enum):
    IPV4 = 1, "ipv4"
    GEO = 2, "geo"
    IPV6 = 3, "ipv6"
    POWERLINK = 4, "powerlink"
    MF = 5, "mf"
    ALL = 6, "all"
    DSTMAC = 7, "dstmac"
    SRCMAC = 8, "srcmac"
    DSTIPV4 = 9, "dstipv4"
    DSTIPV4_DSTMAC = 10, "dstipv4_dstmac"
    IPV4_PROT = 11, "ipv4_prot"
    IPV4_ENCRYPT_PAYLOCD = 12, "ipv4_encrypt_paylocd"
    IPV4_DECRPYT_LOAD = 13, "ipv4_decrpyt_load"
    IPV4_TEST = 14, "ipv4_test"
    IPV4_0304_TEST = 15, "ipv4_0304_test"
    IPV6_9192_TEST = 16, "ipv6_9192_test"
    PWL_1112_TEST = 17, "pwl_1112_test"
    ATP = 18, "atp"
    NETCACHE = 19, "netcache"
    ZJVLAN = 20, "zjvlan"
    GOOSE = 21, "goose"

    def __new__(cls, value, name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._name_ = name
        return obj

    def __int__(self):
        return self.value

    def __str__(self):
        return self.name

    def get_network_type_by_value(value):
        return NetworkType._value2member_map_[value]

class Sender:
    def __init__(self, opt):
        self.pkt_tables = {}
        for network_type in NetworkType:
            self.pkt_tables[network_type] = []
        self.count = opt.count
        self.iface = opt.iface

    def bind(self, network_type, pkts):
        print("bind", network_type)
        for pkt in pkts:
            self.pkt_tables[network_type].append(pkt)
        if network_type == NetworkType.IPV4:
            print("bind", type(network_type))

    def send(self, opt, count=None, iface=None):
        if count is None:
            count = self.count
        if iface is None:
            iface = self.iface
        if opt.network_type == NetworkType.ALL:
            self.send_all_pkt()
        else:
            self.send_single_pkt(opt.network_type, count, iface)
        

    def send_single_pkt(self, network_type, count=None, iface=None):
        if count is None:
            count = self.count
        if iface is None:
            iface = self.iface
        for pkt in self.pkt_tables[network_type]:
            print("debug", str(network_type))
            print(pkt.show())
            sendp(pkt,inter=0,count=count,iface=iface)

    def send_all_pkt(self):
        for network_type in self.pkt_tables.keys():
            self.send_single_pkt(network_type, self.count, self.iface)
    