# psender
## Description
A Python CLI tool for creating and sending custom network packets based on user-defined packet descriptions.

## Features
- 🖥️ Cross-platform support for both Windows and Linux
- 🔍 Automatic network port scanning and availability detection
- 📁 Project-based packet management in `data` directory
- 📝 Support for multiple test cases within each project
- 🛠️ Customizable packet structures using YAML/JSON descriptions
- 📊 Real-time packet transmission and monitoring

## Directory Structure

```
psender/
├── data/                    # Packet projects root directory
│   ├── goose/              # Example project
│   │   ├── pkt.py          # Project packet definition
|── |   |—— case.yml        # Packet description file
│   │   └── README.md       # Project documentation
│   └── your_project/       # Your custom project
│       |── pkt.py          # Your packet definition
|       └—— case.yml        # Your packet description file
├── src/                    # Source code
├── requirements.txt        # Python dependencies(TODO)
└── README.md
```
## Developer Guide

### Creating a New Project

1. Create a new directory under `data/` with your project name
2. Create a `pkt.py` file in your project directory
3. Implement the required `Case` class structure
4. Create a `case.yml` file in your project directory

### Required Class Structure

Your `pkt.py` must contain a `Case` class with the following structure:

```python
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
                    ...
                )
                data = (Ether(
                    src=case['ether']['src'],
                    ...
                ) / Dot1Q(
                    vlan=case['dot1q']['vlan'],
                    ...
                ) / goose)
                setting = Setting(
                    count=case['setting']['count'],
                    ...
                )
                self.cases.append(data)
                self.setting.append(setting)
        except FileNotFoundError:
            print(f"Error: Cannot find {yaml_file} in {current_dir}")
        except Exception as e:
            print(f"Error loading YAML file: {str(e)}")

```

### Example Project Structure

Reference the `goose` directory for a complete example:

```
data/
└── goose/                  # Example project
    ├── pkt.py             # Packet definition file
    |—— case.yml           # Packet description file
    └── README.md          # Project documentation
```
## Usage
```bash
# Using your custom project
sudo python main.py
```
![alt text](image-1.png)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Contact

- Author: 龙卫平
- Email: longweiping@zhejianglab.com
```