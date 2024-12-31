import os
import re
import subprocess

def get_wireless_info(iface):
    """获取无线网卡信息"""
    try:
        # 使用iwconfig获取无线网卡信息
        output = subprocess.check_output(['iwconfig', iface], stderr=subprocess.DEVNULL).decode()
        
        # 提取比特率信息
        bit_rate = re.search(r'Bit Rate[=:](.*?/s)', output)
        if bit_rate:
            rate_str = bit_rate.group(1).strip()
            # 转换到Mbps
            if 'Gb/s' in rate_str:
                return float(rate_str.replace('Gb/s', '')) * 1000
            elif 'Mb/s' in rate_str:
                return float(rate_str.replace('Mb/s', ''))
            
        # 如果没有比特率信息，尝试获取链接质量
        quality = re.search(r'Link Quality=(\d+)/(\d+)', output)
        if quality:
            current, max_quality = map(int, quality.groups())
            return f"Quality: {current}/{max_quality}"
            
    except:
        pass
    return None

def get_interface_speed():
    """获取所有网卡的速率信息"""
    
    def parse_ethtool_output(iface):
        """解析ethtool输出"""
        try:
            output = subprocess.check_output(['ethtool', iface], stderr=subprocess.DEVNULL).decode()
            speed_match = re.search(r'Speed: (\d+)([MGT])b/s', output)
            if speed_match:
                value = int(speed_match.group(1))
                unit = speed_match.group(2)
                # 转换为Mbps
                if unit == 'G':
                    return value * 1000
                elif unit == 'T':
                    return value * 1000000
                return value
        except:
            pass
        return None

    def parse_sysfs_speed(iface):
        """从sysfs读取速率"""
        try:
            with open(f'/sys/class/net/{iface}/speed', 'r') as f:
                return int(f.read().strip())
        except:
            return None

    def get_interface_type(iface):
        """获取网卡类型"""
        # 检查是否是无线网卡
        if os.path.exists(f'/sys/class/net/{iface}/wireless'):
            return 'Wireless'
            
        try:
            with open(f'/sys/class/net/{iface}/type', 'r') as f:
                type_id = int(f.read().strip())
                return {1: 'Ethernet', 772: 'Loopback', 65534: 'Wireless'}.get(type_id, 'Unknown')
        except:
            return 'Unknown'

    def is_interface_up(iface):
        """检查网卡是否启用"""
        try:
            with open(f'/sys/class/net/{iface}/operstate', 'r') as f:
                state = f.read().strip()
                return state.lower() == 'up'
        except:
            return False

    interfaces = {}
    
    for iface in os.listdir('/sys/class/net/'):
        if iface == 'lo':  # 跳过loopback接口
            continue
            
        iface_type = get_interface_type(iface)
        
        interface_info = {
            'name': iface,
            'type': iface_type,
            'status': 'UP' if is_interface_up(iface) else 'DOWN',
            'speed_mbps': None
        }
        
        # 根据接口类型使用不同的方式获取速率
        if iface_type == 'Wireless':
            speed = get_wireless_info(iface)
            interface_info['speed_mbps'] = speed
        else:
            # 有线网卡使用之前的方法
            speed = parse_ethtool_output(iface)
            if speed is None:
                speed = parse_sysfs_speed(iface)
            interface_info['speed_mbps'] = speed
            
        interfaces[iface] = interface_info
    
    return interfaces

def print_interface_info():
    """打印网卡信息"""
    interfaces = get_interface_speed()
    
    print("\n网卡速率信息:")
    print("-" * 70)
    print(f"{'接口名':15} {'类型':12} {'状态':8} {'速率':20}")
    print("-" * 70)
    
    for iface, info in sorted(interfaces.items()):
        if isinstance(info['speed_mbps'], (int, float)):
            speed = f"{info['speed_mbps']:,} Mbps"
        elif info['speed_mbps']:
            speed = str(info['speed_mbps'])
        else:
            speed = "Unknown"
            
        print(f"{info['name']:15} {info['type']:12} {info['status']:8} {speed:20}")
    print("-" * 70)

if __name__ == "__main__":
    print_interface_info()
