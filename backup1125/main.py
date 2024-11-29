from scapy.all import *
import sys
import struct
import os
import random
from myGeo_header import *
from sender import *
from data import *
from myATP import *
from mynetcache import *
from my_zjvlan import *
from goose import *

class Dev:
    def __init__(self) -> None:
        self.iface_list = []
        if os.name == 'windows':
            import wmi
            w=wmi.WMI()
            iface_list=[]
            ifacelist=w.Win32_NetworkAdapterConfiguration ()
            for interface in ifacelist :
                iface_desc=interface.Description
                iface_list.append(iface_desc)
        elif os.name == 'posix':
            print("linux")
            for root, dirs, files in os.walk("/sys/class/net"):
                for dir in dirs:
                    self.iface_list.append(dir)
            self.iface_list = self.iface_list

    def get_iface_desc(self):
        return self.iface_list

def link(sender, data):
    # bind network type to pkt
    sender.bind(NetworkType.IPV4, data.pkt)
    sender.bind(NetworkType.GEO, data.pkt1)
    sender.bind(NetworkType.IPV6, data.pkt2)
    sender.bind(NetworkType.POWERLINK, data.pkt6)
    sender.bind(NetworkType.MF, data.pkt7)
    sender.bind(NetworkType.DSTMAC, [data.pkt8, data.pkt9])
    sender.bind(NetworkType.SRCMAC, data.pkt10)
    sender.bind(NetworkType.DSTIPV4, data.pkt)
    sender.bind(NetworkType.DSTIPV4_DSTMAC, data.pkt11)
    sender.bind(NetworkType.IPV4_PROT, data.pkt12)
    sender.bind(NetworkType.IPV4_ENCRYPT_PAYLOCD, data.pkt13)
    sender.bind(NetworkType.IPV4_DECRPYT_LOAD, [data.pkt_pwl_11, data.pkt_pwl_12, data.pkt_ipv6_7891, data.pkt_ipv6_7892])
    sender.bind(NetworkType.IPV4_TEST, [data.pkt_ipv4_03, data.pkt_ipv4_04])
    sender.bind(NetworkType.IPV4_0304_TEST, [data.pkt_ipv6_7891, data.pkt_ipv6_7892])
    sender.bind(NetworkType.IPV6_9192_TEST, [data.pkt_pwl_11, data.pkt_pwl_12])
    sender.bind(NetworkType.PWL_1112_TEST, data.pkt_mf_d1001)

def gen_atp(data, sender):
    atp = ATP()
    # The sender(vm) mac 00:0c:29:ab:6d:43
    # The reciever mac 48:21:0b:34:c2:3b
    e = geth(src="00:0c:29:ab:6d:43",dst="48:21:0b:34:c2:3b", type=0x0800)
    i = gip(src="111.11.1.33", dst="111.11.1.31")
    u = gudp(sport=19999, dport=6001)
    data.gen_l4_udp_pkt("atp", e, i, u, atp.h1)
    data.gen_l4_udp_pkt("atp", e, i, u, atp.h2)
    data.gen_l4_udp_pkt("atp", e, i, u, atp.h3)
    data.gen_l4_udp_pkt("atp", e, i, u, atp.h4)
    sender.bind(NetworkType.ATP, data.pkts["atp"])

def gen_netcache(data, sender):
    netcache = NETCACHE()
    e = geth(src="00:0c:29:ab:6d:43",dst="48:21:0b:34:c2:3b", type=0x0800)
    i = gip(src="111.11.1.33", dst="111.11.1.31")
    u = gudp(sport=50000, dport=50000)
    data.gen_l4_udp_pkt("netcache", e, i, u, netcache.h1)
    sender.bind(NetworkType.NETCACHE, data.pkts["netcache"])

def gen_myvlan(data, sender):
    myvlan = ZJVLAN()
    e = geth(src="00:0c:29:ab:6d:43",dst="48:21:0b:34:c2:3b", type=0x0801)
    i = gip(src="111.11.1.33", dst="111.11.1.31")
    data.pkts["myvlan"] = []
    data.pkts["myvlan"].append(Ether(src=e.src, dst=e.dst, type=e.type) / myvlan.h1 / IP(src=i.src, dst=i.dst))
    sender.bind(NetworkType.ZJVLAN, data.pkts["myvlan"])

def gen_goose(data, sender):
    #     BitField("dstAddr", 0x010ccd010001, 48),
    # BitField("srcAddr", 0x112233445566, 48),
    # BitField("ethernetType", 0x8100, 16),
    goose = GOOSE()
    data.pkts["goose"] = []
    data.pkts["goose"].append(Ether(src="02:0c:cd:11:00:00", dst="01:0c:cd:01:00:00", type=0x8100) \
                              / Dot1Q(vlan=2, type=0x88b8, prio=1, id=1)\
                                / goose.h)
    # data.gen_l2_pkt("goose", Ether(src="11:22:33:44:55:66", dst="01:0c:cd:01:00:01"), goose.h)
    sender.bind(NetworkType.GOOSE, data.pkts["goose"])

# main process
if __name__ == "__main__":
    dev = Dev()
    opt = Opt()
    opt.set_iface_by_dev(dev)
    opt.set_network_type_by_input()
    opt.set_count_by_input()

    sender = Sender(opt)
    data = Data()
    link(sender, data)
    gen_goose(data, sender)
    # gen_atp(data, sender)
    # gen_netcache(data, sender)
    # gen_myvlan(data, sender)

    # send pkt
    sender.send(opt)


