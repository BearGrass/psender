import os
import importlib.util

class Proto:
    def __init__(self) -> None:
        self.services = {}  # 存储 pkt 模块
        self._load_services()  # 加载 pkt.py

    def _load_module(self, service_name, file_path, module_type):
        """Helper method to load a Python module dynamically"""
        try:
            spec = importlib.util.spec_from_file_location(
                f"{service_name}.{module_type}", 
                file_path
            )
            print(f"Loading {module_type} spec:", spec)
            if spec is None:
                print(f"Failed to create spec for {file_path}")
                return None

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

        except Exception as e:
            print(f"Error loading {module_type} for service {service_name}: {e}")
            return None

    def _load_services(self):
        """Load all pkt.py modules"""
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        print("Scanning directory for services:", data_dir)

        if not os.path.exists(data_dir):
            print("Error: data directory not found!")
            return

        for service_name in os.listdir(data_dir):
            service_path = os.path.join(data_dir, service_name)

            if not os.path.isdir(service_path):
                continue

            pkt_file = os.path.join(service_path, 'pkt.py')
            if os.path.exists(pkt_file):
                module = self._load_module(service_name, pkt_file, "pkt")
                if module:
                    self.services[service_name] = module

    def get_services(self):
        return self.services

    def get_all_class(self):
        for service_name, module in self.services.items():
            print(f"\nService: {service_name}")
            for name, obj in module.__dict__.items():
                if hasattr(obj, "__dict__") and obj.__module__ == module.__name__:
                    print(f"Class: {name}")

if __name__ == "__main__":
    print("Starting program...")
    proto = Proto()
    proto.get_all_class()
    print("\nLoaded services (pkt modules):", proto.get_services())
    goose = proto.get_services().get("goose")
    # for name, obj in goose.__dict__.items():
    #     if isinstance(obj, type) and obj.__module__ == goose.__name__:
    #         print(f"Goose class: {name}")

    print("\nProgram finished.")
