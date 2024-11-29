from scapy.all import *

TYPE_GEO = 0x8947

class MyGeo_gbc(Packet):
    name = "MyGeo_gbc"
    fields_desc = [BitField("version", 0, 4),
                   BitField("ihl", 1, 4),
                   XByteField("reserved_basic", 0),
                   BitField("lt",241,8),
                   BitField("rhl",10,8),
                   BitField("nh", 2, 4),
                   BitField("reserved_common_a", 0, 4),
                   BitField("ht", 4, 4),
                   BitField("hst",0, 4),
                   BitField("tc", 0, 8),
                   BitField("flag", 128, 8),
                   BitField("pl", 4, 16),
                   BitField("mhl", 10, 8),
                   BitField("reserved_common_b", 0, 8),
                   
]
class MyGeo_beacon(Packet):
    name = "MyGeo_beancon"
    fields_desc = [BitField("version", 0, 4),
                   BitField("ihl", 1, 4),
                   XByteField("reserved_basic", 0),
                   BitField("lt",241,8),
                   BitField("rhl",10,8),
                   BitField("nh", 0, 4),
                   BitField("reserved_common_a", 0, 4),
                   BitField("ht", 2, 4),
                   BitField("hst", 2, 4),
                   BitField("tc", 0, 8),
                   BitField("flag", 128, 8),
                   BitField("pl", 4, 16),
                   BitField("mhl", 10, 8),
                   BitField("reserved_common_b", 0, 8),
                   
]
   
class beacon(Packet):
    name ="beacon"
    fields_desc=[
        BitField("gnaddr",0x942edca632ec5db3,64),
        BitField("tst", 0, 32),
        BitField("lat", 0, 32),
        BitField("longg", 0, 32),
        BitField("pai", 0, 1),
        BitField("s", 0, 15),
        BitField("h", 0, 16),       
    ]
   

class gbc(Packet):
    name="gbc"
    fields_desc=[   BitField("sn", 0x15, 16),
                   BitField("reserved_gbc_a", 0, 16),
                   BitField("gnaddr", 0x942edca632ec5db3, 64),
                   BitField("tst", 0, 32),
                   BitField("lat", 0, 32),
                   BitField("longg", 0, 32),
                   BitField("pai", 0, 1),
                   BitField("s", 0, 15),
                   BitField("h", 0, 16),
                   BitField("geoAreaPosLat", 15, 32),
                   BitField("geoAreaPosLon", 15, 32),
                   BitField("disa", 65535, 16),
                   BitField("disb", 0, 16),
                   BitField("angle", 0, 16),
                   BitField("reserved_gbc_b", 0, 16) ]
class BTP_B(Packet):
    name="BTP_B"
    fields_desc=[   BitField("dp", 0x07d2, 16),
                   BitField("dpi", 0, 16),
                  ]
class ITS(Packet):
    name = "ITS"
    fields_desc=[   BitField("pv",1,8),
                    BitField("mid",1,8),
                    BitField("sid",100,32),
                    
                    ]

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


bind_layers(Ether, MyGeo_beacon, type=TYPE_GEO)
bind_layers(Ether, MyGeo_gbc, type=TYPE_GEO)
bind_layers(MyGeo_gbc, gbc)
bind_layers(gbc,BTP_B)
bind_layers(BTP_B,ITS)
bind_layers(MyGeo_beacon, beacon)

