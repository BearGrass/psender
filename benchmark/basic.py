from scapy.all import *
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import queue
import signal
import sys
import os

class SystemStats:
    def __init__(self):
        self.prev_interrupts = None
        self.prev_time = None
        self.prev_net = None
        self.prev_cpu = None
        self.cpu_count = len(os.listdir('/sys/devices/system/cpu/'))
        
    def get_network_stats(self):
        """获取网络统计信息"""
        try:
            stats = {}
            with open('/proc/net/dev', 'r') as f:
                lines = f.readlines()[2:]  # 跳过头两行
                for line in lines:
                    if ':' in line:
                        iface, data = line.split(':')
                        iface = iface.strip()
                        values = data.split()
                        stats[iface] = {
                            'rx_bytes': int(values[0]),
                            'rx_packets': int(values[1]),
                            'tx_bytes': int(values[8]),
                            'tx_packets': int(values[9])
                        }
            return stats
        except Exception as e:
            print(f"读取网络统计失败: {e}")
            return None

    def get_cpu_stats(self):
        """获取CPU使用率"""
        try:
            cpu_info = {}
            with open('/proc/stat', 'r') as f:
                for line in f:
                    if line.startswith('cpu'):
                        parts = line.split()
                        if parts[0] != 'cpu':  # 只统计单个CPU核心
                            cpu_num = int(parts[0][3:])
                            total = sum(int(x) for x in parts[1:])
                            idle = int(parts[4])
                            cpu_info[cpu_num] = {'total': total, 'idle': idle}
            return cpu_info
        except Exception as e:
            print(f"读取CPU统计失败: {e}")
            return None

    def get_softirqs(self):
        """读取软中断详细信息"""
        try:
            irq_stats = {'NET_RX': [], 'NET_TX': []}
            with open('/proc/softirqs', 'r') as f:
                lines = f.readlines()
                
            for line in lines:
                if line.startswith('NET_RX:') or line.startswith('NET_TX:'):
                    parts = line.split()
                    irq_type = parts[0].strip(':')
                    values = [int(x) for x in parts[1:]]
                    irq_stats[irq_type] = values
                    
            return irq_stats
        except Exception as e:
            print(f"读取软中断统计失败: {e}")
            return None

    def calculate_stats(self):
        """计算综合统计信息"""
        current_time = time.time()
        current_irqs = self.get_softirqs()
        current_net = self.get_network_stats()
        current_cpu = self.get_cpu_stats()
        
        if (self.prev_interrupts is None or self.prev_time is None):
            self.prev_interrupts = current_irqs
            self.prev_time = current_time
            self.prev_net = current_net
            self.prev_cpu = current_cpu
            return None
            
        time_delta = current_time - self.prev_time
        if time_delta <= 0:
            return None
            
        stats = {
            'irq_rates': {},
            'network': {},
            'cpu': {}
        }
        
        # 计算软中断率
        for irq_type in ['NET_RX', 'NET_TX']:
            per_cpu_rates = []
            for i in range(min(len(current_irqs[irq_type]), len(self.prev_interrupts[irq_type]))):
                rate = (current_irqs[irq_type][i] - self.prev_interrupts[irq_type][i]) / time_delta
                per_cpu_rates.append(rate)
            stats['irq_rates'][irq_type] = sum(per_cpu_rates)
        
        # 计算网络速率
        for iface in current_net:
            if iface in self.prev_net:
                stats['network'][iface] = {
                    'rx_pps': (current_net[iface]['rx_packets'] - self.prev_net[iface]['rx_packets']) / time_delta,
                    'tx_pps': (current_net[iface]['tx_packets'] - self.prev_net[iface]['tx_packets']) / time_delta,
                }
        
        # 计算CPU使用率
        for cpu in current_cpu:
            if cpu in self.prev_cpu:
                total_delta = current_cpu[cpu]['total'] - self.prev_cpu[cpu]['total']
                idle_delta = current_cpu[cpu]['idle'] - self.prev_cpu[cpu]['idle']
                if total_delta > 0:
                    cpu_usage = 100 * (1 - idle_delta / total_delta)
                    stats['cpu'][cpu] = cpu_usage
        
        self.prev_interrupts = current_irqs
        self.prev_time = current_time
        self.prev_net = current_net
        self.prev_cpu = current_cpu
        
        return stats

class PacketSender:
    def __init__(self, dst_ip, packet_size=1000):
        self.packet = Ether()/IP(dst=dst_ip)/TCP()/Raw(load="X"*packet_size)
        self.raw_packet = bytes(self.packet)
        self.packet_size = len(self.raw_packet) * 8
        self.running = True
        self.stats_queue = queue.Queue()
        self.total_sent = 0
        self.start_time = None
        
        self.interval_packets = 0
        self.interval_bits = 0
        self.stats_lock = threading.Lock()
        
        self.sys_stats = SystemStats()
        
    def sender_worker(self, thread_id, batch_size=100):
        sock = conf.L2socket()
        local_count = 0
        
        try:
            while self.running:
                for _ in range(batch_size):
                    sock.send(self.raw_packet)
                    local_count += 1
                
                with self.stats_lock:
                    self.interval_packets += batch_size
                    self.interval_bits += self.packet_size * batch_size
                
        except Exception as e:
            print(f"Thread {thread_id} error: {e}")
        finally:
            sock.close()
            self.stats_queue.put(local_count)

    def stats_monitor(self, interval=1.0):
        last_time = time.time()
        peak_bps = 0
        peak_pps = 0
        
        while self.running:
            time.sleep(interval)
            current_time = time.time()
            duration = current_time - last_time
            
            with self.stats_lock:
                packets = self.interval_packets
                bits = self.interval_bits
                self.interval_packets = 0
                self.interval_bits = 0
            
            system_stats = self.sys_stats.calculate_stats()
            
            if duration > 0 and system_stats:
                pps = packets / duration
                bps = bits / duration
                peak_bps = max(peak_bps, bps)
                peak_pps = max(peak_pps, pps)
                
                # 清屏并移动光标到开头
                print("\033[2J\033[H", end='')
                
                print("发包统计:")
                print(f"当前PPS: {pps:,.0f} | 当前速率: {bps/1000000:,.2f} Mbps")
                print(f"峰值PPS: {peak_pps:,.0f} | 峰值速率: {peak_bps/1000000:,.2f} Mbps")
                print("-" * 50)
                
                print("软中断统计 (每秒):")
                print(f"NET_RX: {system_stats['irq_rates']['NET_RX']:,.0f}")
                print(f"NET_TX: {system_stats['irq_rates']['NET_TX']:,.0f}")
                print("-" * 50)
                
                print("CPU使用率:")
                for cpu, usage in sorted(system_stats['cpu'].items()):
                    print(f"CPU{cpu}: {usage:.1f}%")
                print("-" * 50)
                
                print("网络接口统计 (每秒):")
                for iface, stats in system_stats['network'].items():
                    print(f"{iface}:")
                    print(f"  接收: {stats['rx_pps']:,.0f} pps")
                    print(f"  发送: {stats['tx_pps']:,.0f} pps")
            
            last_time = current_time

    def signal_handler(self, signum, frame):
        print("\n正在停止发包...")
        self.running = False

    def run(self, thread_count=8, batch_size=100):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.start_time = time.time()
        
        stats_thread = threading.Thread(target=self.stats_monitor)
        stats_thread.daemon = True
        stats_thread.start()
        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            for i in range(thread_count):
                futures.append(
                    executor.submit(self.sender_worker, i, batch_size)
                )
            
            for future in futures:
                try:
                    packets_sent = self.stats_queue.get()
                    self.total_sent += packets_sent
                except Exception as e:
                    print(f"Error getting thread results: {e}")
        
        duration = time.time() - self.start_time
        self.print_final_stats(duration)

    def print_final_stats(self, duration):
        print("\n\n最终统计:")
        print("-" * 50)
        print(f"运行时间: {duration:.2f} 秒")
        print(f"总发包数: {self.total_sent:,}")
        print(f"包大小: {self.packet_size/8:,} 字节")
        print(f"平均 PPS: {self.total_sent/duration:,.2f}")
        print(f"平均速率: {(self.total_sent * self.packet_size)/duration/1000000:,.2f} Mbps")
        print(f"总发送数据: {(self.total_sent * self.packet_size)/8/1000000:,.2f} MB")
        print("-" * 50)

def optimize_system():
    try:
        # 基础网络参数
        os.system('sysctl -w net.core.rmem_max=16777216')
        os.system('sysctl -w net.core.wmem_max=16777216')
        os.system('sysctl -w net.core.netdev_max_backlog=50000')
        
        # 软中断和网络性能优化
        os.system('sysctl -w net.core.rps_sock_flow_entries=32768')
        os.system('sysctl -w net.core.netdev_budget=600')
        os.system('sysctl -w net.ipv4.tcp_timestamps=0')
        os.system('sysctl -w net.ipv4.tcp_low_latency=1')
        
        # 网卡中断优化
        os.system('for i in /sys/class/net/*/queues/rx-*/rps_cpus; do echo ff > $i 2>/dev/null; done')
        os.system('for i in /sys/class/net/*/queues/tx-*/xps_cpus; do echo ff > $i 2>/dev/null; done')
        
    except Exception as e:
        print(f"系统优化警告: {e}")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("需要root权限运行!")
        sys.exit(1)
        
    optimize_system()
    
    sender = PacketSender(
        dst_ip="192.168.1.1",  # 修改为目标IP
        packet_size=1000       # 修改包大小
    )
    
    # 自动检测CPU核心数
    thread_count = os.cpu_count()
    if thread_count > 1:
        thread_count -= 1  # 预留一个核心处理系统任务
    
    sender.run(
        thread_count=thread_count,
        batch_size=100
    )
