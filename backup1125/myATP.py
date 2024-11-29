from scapy.all import *

class ATP:
    def __init__(self) -> None:
        self.h1 = ATP_H1()
        self.h2 = ATP_H2()
        self.h3 = ATP_H3()
        self.h4 = ATP_H4()

class ATP_H1(Packet):
    name = "ATP_H1"
    fields_desc = [ BitField("bitmap", 0x1, 32),
                    BitField("agtr_time",0x4, 8),
                    BitField("overflow",0x0,1),
                    BitField("PSIndex",0x1,2),
                    BitField("dataIndex",0x0,1),
                    BitField("ECN",0x0,1),
                    BitField("isResend",0x0,1),
                    BitField("isSWCollision",0x0,1),
                    BitField("isACK",0x0,1),
                    BitField("appIDandSeqNum",0x02,32),
                    BitField("p4ml_agtr_index",0xff,16),
                    BitField("data0",0x1,32),
                    BitField("data1",0x1,32),
                    BitField("data2",0x1,32),
                    BitField("data3",0x1,32),
                    BitField("data4",0x1,32),
                    BitField("data5",0x1,32),
                    BitField("data6",0x1,32),
                    BitField("data7",0x1,32),
                    BitField("data8",0x1,32),
                    BitField("data9",0x1,32),
                    BitField("data10",0x1,32),
                    BitField("data11",0x1,32),
                    BitField("data12",0x1,32),
                    BitField("data13",0x1,32),
                    BitField("data14",0x1,32),
                    BitField("data15",0x1,32),
                    BitField("data16",0x1,32),
                    BitField("data17",0x1,32),
                    BitField("data18",0x1,32),
                    BitField("data19",0x1,32),
                    BitField("data20",0x1,32),
                    BitField("data21",0x1,32),
                    BitField("data22",0x1,32),
                    BitField("data23",0x1,32),
                    BitField("data24",0x1,32),
                    BitField("data25",0x1,32),
                    BitField("data26",0x1,32),
                    BitField("data27",0x1,32),
                    BitField("data28",0x1,32),
                    BitField("data29",0x1,32),
                    BitField("data30",0x1,32),
                    BitField("data31",0x1,32)
    ]

class ATP_H2(Packet):
    name = "ATP_H2"
    fields_desc = [ BitField("bitmap", 0x2, 32), # 10
                    BitField("agtr_time",0x4, 8),
                    BitField("overflow",0x0,1),
                    BitField("PSIndex",0x1,2),
                    BitField("dataIndex",0x0,1),
                    BitField("ECN",0x0,1),
                    BitField("isResend",0x0,1),
                    BitField("isSWCollision",0x0,1),
                    BitField("isACK",0x0,1),
                    BitField("appIDandSeqNum",0x02,32),
                    BitField("p4ml_agtr_index",0xff,16),
                    BitField("data0",0x1,32),
                    BitField("data1",0x1,32),
                    BitField("data2",0x1,32),
                    BitField("data3",0x1,32),
                    BitField("data4",0x1,32),
                    BitField("data5",0x1,32),
                    BitField("data6",0x1,32),
                    BitField("data7",0x1,32),
                    BitField("data8",0x1,32),
                    BitField("data9",0x1,32),
                    BitField("data10",0x1,32),
                    BitField("data11",0x1,32),
                    BitField("data12",0x1,32),
                    BitField("data13",0x1,32),
                    BitField("data14",0x1,32),
                    BitField("data15",0x1,32),
                    BitField("data16",0x1,32),
                    BitField("data17",0x1,32),
                    BitField("data18",0x1,32),
                    BitField("data19",0x1,32),
                    BitField("data20",0x1,32),
                    BitField("data21",0x1,32),
                    BitField("data22",0x1,32),
                    BitField("data23",0x1,32),
                    BitField("data24",0x1,32),
                    BitField("data25",0x1,32),
                    BitField("data26",0x1,32),
                    BitField("data27",0x1,32),
                    BitField("data28",0x1,32),
                    BitField("data29",0x1,32),
                    BitField("data30",0x1,32),
                    BitField("data31",0x1,32)
    ]

class ATP_H3(Packet):
    name = "ATP_H3"
    fields_desc = [ BitField("bitmap", 0x4, 32), # 100
                    BitField("agtr_time",0x4, 8),
                    BitField("overflow",0x0,1),
                    BitField("PSIndex",0x1,2),
                    BitField("dataIndex",0x0,1),
                    BitField("ECN",0x0,1),
                    BitField("isResend",0x0,1),
                    BitField("isSWCollision",0x0,1),
                    BitField("isACK",0x0,1),
                    BitField("appIDandSeqNum",0x02,32),
                    BitField("p4ml_agtr_index",0xff,16),
                    BitField("data0",0x1,32),
                    BitField("data1",0x1,32),
                    BitField("data2",0x1,32),
                    BitField("data3",0x1,32),
                    BitField("data4",0x1,32),
                    BitField("data5",0x1,32),
                    BitField("data6",0x1,32),
                    BitField("data7",0x1,32),
                    BitField("data8",0x1,32),
                    BitField("data9",0x1,32),
                    BitField("data10",0x1,32),
                    BitField("data11",0x1,32),
                    BitField("data12",0x1,32),
                    BitField("data13",0x1,32),
                    BitField("data14",0x1,32),
                    BitField("data15",0x1,32),
                    BitField("data16",0x1,32),
                    BitField("data17",0x1,32),
                    BitField("data18",0x1,32),
                    BitField("data19",0x1,32),
                    BitField("data20",0x1,32),
                    BitField("data21",0x1,32),
                    BitField("data22",0x1,32),
                    BitField("data23",0x1,32),
                    BitField("data24",0x1,32),
                    BitField("data25",0x1,32),
                    BitField("data26",0x1,32),
                    BitField("data27",0x1,32),
                    BitField("data28",0x1,32),
                    BitField("data29",0x1,32),
                    BitField("data30",0x1,32),
                    BitField("data31",0x1,32)
    ]

class ATP_H4(Packet):
    name = "ATP_H4"
    fields_desc = [ BitField("bitmap", 0x8, 32), # 1000
                    BitField("agtr_time",0x4, 8),
                    BitField("overflow",0x0,1),
                    BitField("PSIndex",0x1,2),
                    BitField("dataIndex",0x0,1),
                    BitField("ECN",0x0,1),
                    BitField("isResend",0x0,1),
                    BitField("isSWCollision",0x0,1),
                    BitField("isACK",0x0,1),
                    BitField("appIDandSeqNum",0x02,32),
                    BitField("p4ml_agtr_index",0xff,16),
                    BitField("data0",0x1,32),
                    BitField("data1",0x1,32),
                    BitField("data2",0x1,32),
                    BitField("data3",0x1,32),
                    BitField("data4",0x1,32),
                    BitField("data5",0x1,32),
                    BitField("data6",0x1,32),
                    BitField("data7",0x1,32),
                    BitField("data8",0x1,32),
                    BitField("data9",0x1,32),
                    BitField("data10",0x1,32),
                    BitField("data11",0x1,32),
                    BitField("data12",0x1,32),
                    BitField("data13",0x1,32),
                    BitField("data14",0x1,32),
                    BitField("data15",0x1,32),
                    BitField("data16",0x1,32),
                    BitField("data17",0x1,32),
                    BitField("data18",0x1,32),
                    BitField("data19",0x1,32),
                    BitField("data20",0x1,32),
                    BitField("data21",0x1,32),
                    BitField("data22",0x1,32),
                    BitField("data23",0x1,32),
                    BitField("data24",0x1,32),
                    BitField("data25",0x1,32),
                    BitField("data26",0x1,32),
                    BitField("data27",0x1,32),
                    BitField("data28",0x1,32),
                    BitField("data29",0x1,32),
                    BitField("data30",0x1,32),
                    BitField("data31",0x1,32)
    ]