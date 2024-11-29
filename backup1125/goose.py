from scapy.all import *

class GOOSE:
    def __init__(self) -> None:
        self.h = goose_h()
        self.sv = goose_sv()


class goose_h(Packet):
    """
    header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> ethernetType;
    }
    header vlan_t{
        bit<3>  pri;
        bit<1>  cfi;
        bit<12> vid;
        bit<16> vlan_ether_type;
    }
    header goose_t{
    bit<16> goose_appid;
    bit<16> goose_length;
    bit<16> goose_reserved_one;
    bit<16> goose_reserved_two;
    }
    header sv_t{
        bit<16> sv_appid;
        bit<16> sv_length;
        bit<16> sv_reserved_one;
        bit<16> sv_reserved_two;
    }
    """
    name = "goose_h"
    fields_desc = [
        BitField("goose_appid", 0x3fff, 16),
        BitField("goose_length", 0x3fff, 16),
        BitField("goose_reserved_one", 0x1, 16),
        BitField("goose_reserved_two", 0x1, 16),
    ]
class goose_sv(Packet):
    name = "goose_sv"
    fields_desc = [
        BitField("dstAddr", 0x1, 48),
        BitField("srcAddr", 0x1, 48),
        BitField("ethernetType", 0x0800, 16),
        BitField("pri", 0x1, 3),
        BitField("cfi", 0x1, 1),
        BitField("vid", 1003, 12),
        BitField("ether_type", 0x0800, 16),        
        BitField("sv_appid", 0x1, 16),
        BitField("sv_length", 0x1, 16),
        BitField("sv_reserved_one", 0x1, 16),
        BitField("sv_reserved_two", 0x1, 16),
    ]
