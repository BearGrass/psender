import os
import yaml
from scapy.all import Ether, Dot1Q, struct, Packet, XShortField, ShortField


class Setting:
    def __init__(self, count= 1, inter= 0) -> None:
        self.count = count
        self.inter = inter

class GOOSE(Packet):
    name = "goose"
    # fields_desc应该是类变量，不应在__init__中定义
    # XShortField 和 ShortField 是 Scapy 中用于定义数据包字段的类型，它们都是16位(2字节)
    fields_desc = [
        XShortField("goose_appid", 0x0000),
        ShortField("goose_length", None),
        XShortField("goose_reserved_1", 0x0000),
        XShortField("goose_reserved_2", 0x0000)
    ]

    def __init__(self, appid=0x0000, length=None, reserved_1=0x0000, reserved_2=0x0000, **kwargs):
        # 调用父类的__init__
        super().__init__(**kwargs)
        # 设置字段值
        self.fields['goose_appid'] = appid
        if length is not None:
            self.fields['goose_length'] = length
        self.fields['goose_reserved_1'] = reserved_1
        self.fields['goose_reserved_2'] = reserved_2

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Case:
    cases = []
    setting = []
    def append(self, data, setting):
        self.cases.append(data)
        if setting is None:
            setting = Setting()
        self.setting.append(setting)

    def load_cases_from_yaml(self, yaml_file="case.yml"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(current_dir, yaml_file)
        try:
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
            for case in data['cases']:
                goose = GOOSE(
                    appid=case['goose']['appid'],
                    length=case['goose']['length'],
                    reserved_1=case['goose']['reserved_1'],
                    reserved_2=case['goose']['reserved_2']
                )
                data = (Ether(
                    src=case['ether']['src'],
                    dst=case['ether']['dst'],
                    type=case['ether']['type']
                ) / Dot1Q(
                    vlan=case['dot1q']['vlan'],
                    type=case['dot1q']['type'],
                    prio=case['dot1q']['prio']
                ) / goose)
                setting = Setting(
                    count=case['setting']['count'],
                    inter=case['setting']['inter']
                )
                self.cases.append(data)
                self.setting.append(setting)
        except FileNotFoundError:
            print(f"Error: Cannot find {yaml_file} in {current_dir}")
        except Exception as e:
            print(f"Error loading YAML file: {str(e)}")



    def get_case(self):
        return self.cases
    def get_setting(self):
        return self.setting

    def __init__(self) -> None:
        self.load_cases_from_yaml()
