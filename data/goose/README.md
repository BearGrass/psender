# 项目说明
## 报文描述
```
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
```

## 例子
```
# 创建GOOSE数据包
goose = GoosePacket(
    appid=0x1000,
    length=100,
    reserved_one=0,
    reserved_two=0
)

# 设置以太网参数
goose.set_ether(
    src="00:11:22:33:44:55",
    dst="01:0C:CD:01:00:01",
    etype=0x8100
)

# 设置VLAN参数
goose.set_vlan(
    vlan=100,
    vlan_type=0x88B8,
    prio=4
)

# 生成数据包
packet = goose.gen_pkt()
```