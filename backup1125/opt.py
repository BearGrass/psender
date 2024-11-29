from enum import Enum

class ServiceType(Enum):
    COMMEN = 1, "common"
    NATION_NETWORK = 2, "nation_network"

    def __new__(cls, value, name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._name_ = name
        return obj
    
    def __int__(self):
        return self.value
    
    def __str__(self):
        return self.name
    
    def get_service_type_by_value(value):
        return ServiceType._value2member_map_[value]
    
class Opt:
    def __init__(self) -> None:
        self.iface = None
        self.network_type = None
        self.count = None
    
    def set_iface_by_dev(self, dev):
        iface_list = dev.get_iface_desc()
        
        for times in range(0,len(iface_list)):
            print(times, iface_list[times])
        print("chose nic interface: ")
        index=int(input("index:"))
        if(index>len(iface_list)):
            print(" out of range total  interface num: ",len(iface_list)-1)
            exit(1)
        else:
            self.iface=iface_list[index]

    def get_iface(self):
        return self.iface

    def 

    def set_network_type_by_input(self):
        print("| ipv4:1 | geo:2 | ipv6:3 | powerllink:4 | mf:5 | all:6 | dstmac:7 | srcmac:8 |dstipv4:9 | dstipv4_dstmac:10 | ipv4_prot:11 |")
        print("|ipv4_encrypt_paylocd:12 | ipv4_decrpyt_load:13| ipv4_test:14 | ipv4_0304_test:15 | ipv6_9192_test:16 | pwl_1112_test:17")
        print("| atp:18 | netcache:19 | zjvlan:20 | goose:21 |")
        self.network_type = NetworkType.get_network_type_by_value(int(input("network type:")))
    def get_network_type(self):
        return self.network_type
    
    def set_count_by_input(self):
        self.count=int(input("pkt count:"))
    
    def get_count(self):
        return self.count