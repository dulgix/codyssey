import json
import time

# 문제 3에서 제작한 DummySensor 클래스 (가정)
class DummySensor:
    def get_value(self):
        # 센서에서 값을 가져오는 동작을 시뮬레이션
        return 25.5

class MissionComputer:
    def __init__(self):
        # 화성 기지 환경 값을 저장할 사전(Dict) 객체 속성
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        # DummySensor 클래스를 ds라는 이름으로 인스턴스화
        self.ds = DummySensor()

    def get_sensor_data(self):
        """
        센서 값을 가져와 env_values에 담고, json 형태로 5초마다 출력합니다.
        """
        while True:
            # 1. 센서의 값을 가져와서 env_values에 담기
            # 각 항목에 대해 ds.get_value()를 호출하여 업데이트
            for key in self.env_values:
                self.env_values[key] = self.ds.get_value()

            # 2. env_values의 값을 json 형태로 화면에 출력
            # (json.dumps를 사용하여 json 형식의 문자열로 변환)
            print(json.dumps(self.env_values))

            # 3. 위의 두 가지 동작을 5초에 한 번씩 반복
            time.sleep(5)

# MissionComputer 클래스를 RunComputer라는 이름으로 인스턴스화
RunComputer = MissionComputer()

# RunComputer 인스턴스의 get_sensor_data() 메소드 호출
if __name__ == '__main__':
    RunComputer.get_sensor_data()