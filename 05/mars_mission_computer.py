import json
import time
import platform
import psutil

class DummySensor:
    def get_value(self):
        return 25.5

class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        self.ds = DummySensor()
        # [보너스] 설정 파일 로드
        self.settings = self.load_settings()

    def load_settings(self):
        """setting.txt 파일에서 설정값을 읽어옵니다."""
        conf = {}
        try:
            with open('setting.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line:
                        k, v = line.strip().split('=')
                        conf[k] = v.lower() == 'true'
        except:
            pass # 파일이 없으면 모든 항목 True로 간주
        return conf

    def apply_filter(self, data):
        """설정값에 True로 되어 있는 항목만 남깁니다."""
        return {k: v for k, v in data.items() if self.settings.get(k, True)}

    def get_mission_computer_info(self):
        try:
            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_cores': psutil.cpu_count(logical=False),
                'memory_size': f'{round(psutil.virtual_memory().total / (1024**3), 2)} GB'
            }
            # [보너스] 필터 적용
            filtered_info = self.apply_filter(info)
            print('--- Mission Computer System Info ---')
            print(json.dumps(filtered_info, indent=4))
        except Exception as e:
            print(f'Error retrieving system info: {e}')

    def get_mission_computer_load(self):
        try:
            load = {
                'cpu_usage_percent': psutil.cpu_percent(interval=1),
                'memory_usage_percent': psutil.virtual_memory().percent
            }
            # [보너스] 필터 적용
            filtered_load = self.apply_filter(load)
            print('--- Mission Computer Real-time Load ---')
            print(json.dumps(filtered_load, indent=4))
        except Exception as e:
            print(f'Error retrieving system load: {e}')

runComputer = MissionComputer()

if __name__ == '__main__':
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()