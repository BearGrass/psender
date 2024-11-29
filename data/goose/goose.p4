#include <core.p4>
#define V1MODEL_VERSION 20180101
#include <v1model.p4>
#define CPU_PORT 255

const bit<16> ETHERTYPE_TPID = 0x8100;
const bit<16> TYPE_GOOSE = 0x88B8;
const bit<16> TYPE_SV = 0x88BA;
const bit<9> PORT_ONOS =255;
const bit<9> PORT_BIT_MCAST =254;
const int FlOW_SIZE = 128;
typedef bit<64>  mcast_group_id_t;
typedef bit<8>   flag_t;
const bit<3> GOOSE_PRI = 7;
const bit<3> SV_PRI = 6;

header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> ethernetType;
}
header vlan_t{
    bit<3>  pri;
    bit<1>  cfi;
    bit<12> vid;
    bit<16> ether_type;
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

@controller_header("packet_in")
header onos_in_header_t {
    bit<9>  ingress_port;
    bit<7>      _pad;
}

@controller_header("packet_out")
header onos_out_header_t {
    bit<9>  egress_port;
    bit<7>      _pad;
}

struct metadata{
    bool is_multicast;
    flag_t is_flag;
}
struct headers {
    onos_out_header_t               onos_out;       
    onos_in_header_t                onos_in;        
    ethernet_t                      ethernet;
    vlan_t                          vlan;
    goose_t                         goose;           
    sv_t                            sv;           

}

parser ParserImpl(packet_in packet, out headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    @name(".start") state start {
    transition select(standard_metadata.ingress_port){
           PORT_ONOS: parse_packet_out; 
           default: parse_ethernet;
        }
    }
    @name(".parse_packet_out") state parse_packet_out {
        packet.extract(hdr.onos_out);
        transition parse_ethernet;
    }

    @name(".parse_ethernet") state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.ethernetType) {
            ETHERTYPE_TPID: parse_vlan;
            default: accept;
        }
    }
    @name(".parse_vlan") state parse_vlan {
        packet.extract(hdr.vlan);
        transition select(hdr.vlan.ether_type){
            TYPE_GOOSE: parse_goose;
            TYPE_SV   : parse_sv;
            default   : accept;
        }
    }
    @name(".parse_goose") state parse_goose {
        packet.extract(hdr.goose);
        transition accept;
    }
    @name(".parse_sv") state parse_sv {
        packet.extract(hdr.sv);
        transition accept;
        }
}
    

control egress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    apply {
            if (standard_metadata.egress_port == CPU_PORT) {
                hdr.onos_in.setValid();
                hdr.onos_in.ingress_port = standard_metadata.ingress_port;
                exit;
            }
            if (meta.is_multicast == true &&
              standard_metadata.ingress_port == standard_metadata.egress_port) {
                mark_to_drop(standard_metadata);
            }
    }
}


control ingress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {

    action goose_multicast(mcast_group_id_t gid,flag_t flag) {
        standard_metadata.mcast_grp = gid;
        meta.is_flag = flag;
        meta.is_multicast = true;
        standard_metadata.egress_spec = PORT_BIT_MCAST;
    }
    action sv_multicast(mcast_group_id_t gid,flag_t flag) {
        standard_metadata.mcast_grp = gid;
        meta.is_flag = flag;
        meta.is_multicast = true;
        standard_metadata.egress_spec = PORT_BIT_MCAST;
    }
    table goose_table {
        key = {
            hdr.ethernet.dstAddr     : ternary;
            hdr.ethernet.srcAddr     : ternary;
            hdr.vlan.vid             : ternary;
            hdr.goose.goose_appid    : ternary;
        }
        actions = {
            goose_multicast;
        }
        size = FlOW_SIZE;
    }
    table sv_table {
        key = {
            hdr.ethernet.dstAddr     : ternary;
            hdr.ethernet.srcAddr     : ternary;
            hdr.vlan.vid             : ternary;
            hdr.sv.sv_appid          : ternary;
        }
        actions = {
            sv_multicast;
        }
        size = FlOW_SIZE;
    }
    
    apply {
        if(hdr.goose.isValid()){
            goose_table.apply();
            if(meta.is_flag == 1){
                hdr.vlan.pri = GOOSE_PRI;
            }
        }
        if(hdr.sv.isValid()){
            sv_table.apply();
            if(meta.is_flag == 1){
                hdr.vlan.pri = SV_PRI;
            }

        }
    }
}

control DeparserImpl(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.vlan);
        packet.emit(hdr.goose);
        packet.emit(hdr.sv);
    }
}

control verifyChecksum(inout headers hdr, inout metadata meta) {
    apply {
    }
}

control computeChecksum(inout headers hdr, inout metadata meta) {
    apply {
    }
}

V1Switch(ParserImpl(), verifyChecksum(), ingress(), egress(), computeChecksum(), DeparserImpl()) main;

