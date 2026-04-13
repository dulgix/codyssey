import json
import time
import platform
import psutil

# 문제 3에서 제작한 DummySensor 클래스
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

    def get_mission_computer_info(self):
        """
        시스템 기본 정보를 가져와 JSON 형식으로 출력합니다.
        """
        try:
            # platform과 psutil을 사용하여 상세 정보 수집
            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_cores': psutil.cpu_count(logical=False),
                'memory_size': f'{round(psutil.virtual_memory().total / (1024**3), 2)} GB'
            }
            print('--- Mission Computer System Info ---')
            print(json.dumps(info, indent=4))
        except Exception as e:
            # 제약사항: 시스템 정보를 가져오는 부분은 예외처리가 되어 있어야 함
            print(f'Error retrieving system info: {e}')

    def get_mission_computer_load(self):
        """
        실시간 CPU 및 메모리 부하 정보를 가져와 JSON 형식으로 출력합니다.
        """
        try:
            load = {
                'cpu_usage_percent': psutil.cpu_percent(interval=1),
                'memory_usage_percent': psutil.virtual_memory().percent
            }
            print('--- Mission Computer Real-time Load ---')
            print(json.dumps(load, indent=4))
        except Exception as e:
            # 제약사항: 예외처리 포함
            print(f'Error retrieving system load: {e}')

# 요구사항: 'runComputer' 라는 이름으로 인스턴스화
runComputer = MissionComputer()

if __name__ == '__main__':
    # 1. 시스템 정보 출력 확인
    runComputer.get_mission_computer_info()
    
    # 2. 실시간 부하 출력 확인
    runComputer.get_mission_computer_load()