import os
from scapy.all import *
from proto import Proto


class Dev:
    def __init__(self) -> None:
        self.iface_list = []
        if os.name == 'nt':
            import wmi
            wmi_obj = wmi.WMI()

            # 获取网络适配器配置信息
            configs = wmi_obj.Win32_NetworkAdapterConfiguration(IPEnabled=True)

            for config in configs:
                # 获取对应的网络适配器
                adapter = wmi_obj.Win32_NetworkAdapter(Index=config.Index)[0]

                if adapter.NetEnabled:  # 只获取已启用的接口
                    iface_info = {
                        'name': adapter.NetConnectionID,  # 网络连接名称
                        # 'description': adapter.Description,  # 适配器描述
                        # 'mac': adapter.MACAddress,  # MAC地址
                        # 'type': adapter.AdapterType,  # 适配器类型
                        # 'interface_index': adapter.InterfaceIndex,  # 接口索引
                        # 'speed': adapter.Speed,  # 速度
                        # 'ip_addresses': []  # IP地址列表
                    }
                    self.iface_list.append(iface_info['name'])
        elif os.name == 'posix':
            print("linux")
            for root, dirs, files in os.walk("/sys/class/net"):
                for dir in dirs:
                    self.iface_list.append(dir)
            self.iface_list = self.iface_list

    def get_iface_desc(self):
        return self.iface_list


class Server:
    """
    1. choose iface
    2. choose data
    3. choose case
    4. run test
    """

    def __init__(self):
        self.dev = Dev()
        self.proto = Proto()

    def get_dev_from_input(self):
        # show iface list
        print("choose iface\n")
        iface_list = self.dev.get_iface_desc()
        for index, iface in enumerate(iface_list):
            # print(f"{index}: {iface['name']}")
            print(index, iface)
        index = int(input("index:"))
        if index > len(iface_list):
            print("out of range total interface num:", len(iface_list)-1)
            exit(1)
        else:
            self.iface = iface_list[index]
            # print(self.iface)

    def get_protocol_from_input(self):
        # show protocol list
        print("choose protocol")
        protocol_list = self.proto.get_services()
        temp_list = []
        for index, protocol in enumerate(protocol_list):
            temp_list.append(protocol)
            print(f"{index}: {protocol}")
        index = int(input("index:"))
        if index > len(protocol_list):
            print("out of range total protocol num:", len(protocol_list)-1)
            exit(1)
        else:
            self.protocol = protocol_list[temp_list[index]]
            # print(self.protocol)

        total_cases = len(self.protocol.Case().get_case())
        print(f"Choose case (1-{total_cases}, default: all)")

        try:
            case_input = input("Case number: ").strip()
            case_number = -1 if not case_input else int(case_input)

            if case_number != -1 and not 0 < case_number <= total_cases:
                raise ValueError
            self.case_number = case_number - 1

        except ValueError:
            print(
                f"Invalid input. Please enter -1 or a number between 0 and {total_cases}")

    def send_case_to_dev(self):
        case = self.protocol.Case()
        cases = case.get_case()
        setting = case.get_setting()
        Totol_send = 0
        print("case number = ", self.case_number)
        if self.case_number >= 0:
            index = self.case_number
            print(cases[index].show())
            sendp(cases[index],
                  inter=setting[index].inter,
                  count=setting[index].count,
                  iface=self.iface)
            Totol_send += setting[index].count
        else:
            print("send all cases")
            for index in range(len(cases)):
                print("send the", index, "pkt")
                print(cases[index].show())
                sendp(cases[index],
                      inter=setting[index].inter,
                      count=setting[index].count,
                      iface=self.iface)
                Totol_send += setting[index].count
        print("Totol send ", Totol_send, " pkts")


if __name__ == "__main__":
    server = Server()
    server.get_dev_from_input()
    server.get_protocol_from_input()
    server.send_case_to_dev()
    server.send_case_to_dev()
