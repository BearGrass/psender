from scapy.all import *

class ZJVLAN:
    def __init__(self) -> None:
        self.h1 = zjvlan_h1()

class zjvlan_h1(Packet):
    name = "zjvlan_h1"
    fields_desc = [
        BitField("vid", 1003, 16),
        BitField("ethtype", 0x0800, 16),
    ]