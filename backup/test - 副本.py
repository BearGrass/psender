from scapy.all import *
import sys
import struct
import os
import random
import wmi
from myGeo_header import MyGeo_gbc,gbc,MyGeo_beacon,beacon,BTP_B,ITS
class Calc(Packet):
    name = "MyCalc"
    fields_desc = [StrLenField("Pad","0")]
TYPE_GEO = 0x080A
#pad1 = "00000001000000c9c0a81eb8"
pad1 = "00000001c0a81eb800000069"
pad_decode1 = bytes.fromhex(pad1)

pad2 = "19a5d8"
pad_decode2 =  bytes.fromhex(pad2)
class MyGeo(Packet, IPTools):
    name = "MyGeo"
    fields_desc = [BitField("version", 4, 4),
                   BitField("ihl", None, 4),
                   XByteField("tos", 0),
                   ShortField("len", None),
                   ShortField("id", 1),
                   FlagsField("flags", 0, 3, ["MF", "DF", "evil"]),
                   BitField("frag", 0, 13),
                   ByteField("ttl", 64),
                   ByteEnumField("proto", 0, IP_PROTOS),
                   XShortField("chksum", None),
                   # IPField("src", "127.0.0.1"),
                   Emph(SourceIPField("src", "dst")),
                   Emph(IPField("dst", "127.0.0.1"))]
    def mysummary(self):
        s = self.sprintf("%IP.src% > %IP.dst% %IP.proto%")
        if self.frag:
            s += " frag:%i" % self.frag
        return s

netflow =  NetflowHeader()/NetflowHeaderV1()/NetflowRecordV1()
data = 'dataasdfasdfsfasdfadfadsdfva'
data1='4d4fa2a5dbb4fbecd6e05851c8585625cea624acaa73f49f00403522e86a85e7'
pkt = Ether(src="54:B2:03:91:14:26",dst="54:B2:03:91:33:03")/\
      IP(src='169.254.30.57', dst='169.254.131.41')/\
      data

pkt1 =Ether(src="00:e0:4c:68:4c:92",dst="e4:95:6e:2f:d3:44")/\
      MyGeo_gbc()/gbc()/\
      data
pkt2 = Ether(src="54:B2:03:91:32:A0",dst="54:B2:03:91:30:9C")/\
    #IPv6(src='fe80::60b1:ecb0:df7f:52c9', dst='fe80::e695:6eff:fe2f:2278')\
    IPv6(src='1234::5678:9012:3456:7890', dst='fe80::e695:6eff:fe2f:2278')\
    /\
     data
pkt3 = Ether(src="00:e0:4c:68:3c:93",dst="00:e0:4c:68:3c:92")/Dot1Q(vlan=4)/\
      IP(src='192.168.40.182', dst='192.168.30.181',chksum=1)/\
      data
pkt4 = Ether(src="00:e0:4c:68:3c:93",dst="00:e0:4c:68:3c:92")/\
      data
pkt5 = Ether(src="00:e0:4c:68:3c:93",dst="00:e0:4c:68:3c:92")/\
      IP(src='192.168.70.182', dst='192.168.30.182')/\
      data
pkt6 = Ether(src="00:e0:4c:68:3c:95",dst="00:e0:4c:68:3c:92",type=0x88ab)/Calc(Pad = pad_decode2)/data
pkt7 = Ether(src="00:e0:4c:68:3c:95",dst="00:e0:4c:68:3c:93",type=0x27c0)/Calc(Pad =  bytes.fromhex("0000000100000066c0a81eb8"))/data
pkt11 = Ether(src="00:e0:4c:68:3c:93",dst="00:e0:4c:68:3c:92")/\
      IP(src='192.168.40.182', dst='192.168.30.182')/\
      TCP(sport=100,dport=200)/\
      data
pkt12 = Ether(src="00:e0:4c:68:3c:93",dst="00:e0:4c:68:3c:92")/\
      	IP(src='192.168.40.182', dst='192.168.30.182')/\
      	data
pkt13 = Ether(src="00:e0:4c:68:3c:93",dst="00:e0:4c:68:3c:92")/\
      	IP(src='192.168.40.182', dst='192.168.30.182')/\
        Calc(Pad= bytes.fromhex(data1))

### for windows
if os.name == 'windows':
    import wmi
    def get_iface_desc():
        w=wmi.WMI()
        iface_list=[]
        ifacelist=w.Win32_NetworkAdapterConfiguration ()
        for interface in ifacelist :
            iface_desc=interface.Description
            iface_list.append(iface_desc)
        return iface_list
elif os.name == 'posix':
    def get_iface_desc():
        iface_list=[]
        for root, dirs, files in os.walk("/sys/class/net"):
            for dir in dirs:
                iface_list.append(dir)
        return iface_list
###################
# iface 即为需要指定的网卡接口
#################
#iface="Intel(R) Wi-Fi 6 AX200 160MHz"
iface_list=get_iface_desc()
for i in range(0,len(iface_list)):
    print(i, iface_list[i])
print("chose nic interface: ")
index=int(input("index:"))
if(index>len(iface_list)):
  print(" out of range total  interface num: ",len(iface_list)-1)
  exit(1)
else:
  iface=iface_list[index]
##################
print("| ipv4:1 | geo:2 | ipv6:3 | powerllink:4 | mf:5 | all:6 | dstmac:7 | srcmac:8 |dstipv4:9 | dstipv4_dstmac:10 | ipv4_prot:11 |")
print("|ipv4_encrypt_paylocd:12 | ipv4_decrpyt_load:13|")
a1=int(input("leixing:"))
a=int(input("jici:"))
for i in range(a):
    print(i)
    Maclist = []
    for i in range(1, 20):
        RANDSTR = "".join(random.sample("0123456789abcdef", 2))
        Maclist.append(RANDSTR)
    RANDMAC = ":".join(Maclist)
    if a1==1:
        print("ipv4")
        sendp(pkt,inter=1,count=1,iface=iface)
        time.sleep(1)
    if a1==2:
        print("geo")
        sendp(pkt1,inter=1,count=1,iface=iface)
        time.sleep(1)
    if a1==3:
        print("ipv6")
        sendp(pkt2,inter=1,count=1,iface=iface)
        time.sleep(1)
    if a1==4:
        print("powerllink")
        sendp(pkt6, inter=0, count=1, iface=iface)
        #time.sleep(1)
    if a1==5:
        print("mf")
        sendp(pkt7, inter=1, count=1, iface=iface)
    if a1==6:
        print("ip")
        sendp(pkt, inter=1, count=1, iface=iface)
        time.sleep(1)
        print("geo")
        sendp(pkt1, inter=1, count=1, iface=iface)
        time.sleep(1)
        print("ipv6")
        sendp(pkt2, inter=1, count=1, iface=iface)
        time.sleep(1)
        print("powerllink")
        sendp(pkt6, inter=1, count=1, iface=iface)
        time.sleep(1)
        print("mf")
        sendp(pkt7, inter=1, count=1, iface=iface)
        time.sleep(1)  
    if a1==7:
        print("dstmac")
        pkt8 = Ether(src=RANDMAC, dst="00:e0:4c:68:3c:92") / \
              IP(src='192.168.40.182', dst='192.168.30.182') / \
              data
        pkt9 = Ether(src=RANDMAC, dst="00:e0:4c:68:3c:95") / \
              IP(src='192.168.40.182', dst='192.168.30.182') / \
              data
        sendp(pkt8,inter=1,count=1,iface=iface)
        time.sleep(1)
        sendp(pkt9,inter=1,count=1,iface=iface)
        time.sleep(1)
    if a1==8:
        print("srcmac")
        pkt10 = Ether(src="00:e0:4c:68:3c:93", dst=RANDMAC) / \
              IP(src='192.168.40.182', dst='192.168.30.182') / \
              data
        sendp(pkt10,inter=1,count=1,iface=iface)
        time.sleep(1)
    if a1==9:
        print("ipv4_mac")
        sendp(pkt,inter=1,count=1,iface=iface)
        time.sleep(1)
    if a1==10:
        print("ivp4_port")
        sendp(pkt11,inter=1,count=1,iface=iface)
        time.sleep(1)
    if a1==12:
        print("ipv4_encrypt_payload")
        sendp(pkt12,inter=1,count=1,iface=iface)
        time.sleep(1)
    if a1==13:
        print("ipv4_dencrypt_payload")
        sendp(pkt13,inter=1,count=1,iface=iface)
        time.sleep(1)
