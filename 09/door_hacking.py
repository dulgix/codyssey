import zipfile
import itertools
import time
import string
import os
from multiprocessing import Pool, cpu_count, Manager


def check_chunk(args):
    '''나누어진 암호 덩어리를 검사하고 진행수를 보고하는 함수'''
    file_name, passwords, progress_dict, worker_id = args
    count = 0
    try:
        with zipfile.ZipFile(file_name) as zf:
            for pwd in passwords:
                count = count + 1
                # 10,000번마다 메인 프로세스에 진행 상황 공유
                if count % 10000 == 0:
                    progress_dict[worker_id] = count
                
                password = ''.join(pwd)
                try:
                    # 암호 대입 시도
                    zf.extractall(pwd=password.encode('utf-8'))
                    return password
                except:
                    continue
    except:
        pass
    progress_dict[worker_id] = count
    return None


def unlock_zip():
    file_name = 'emergency_storage_key.zip'
    # 숫자와 소문자 알파벳 조합 (PEP 8 규칙 준수)
    chars = string.digits + string.ascii_lowercase
    password_length = 6
    total_combinations = len(chars) ** password_length
    
    if not os.path.exists(file_name):
        print('오류: 파일을 찾을 수 없습니다.')
        return

    # CPU 코어 개수 확인 및 시작 시간 기록
    num_workers = cpu_count()
    start_time = time.time()
    
    print('암호 해독 시작 시간:', time.ctime(start_time))
    print('사용 CPU 코어:', num_workers, '개')
    print('총 조합 수:', format(total_combinations, ','), '개')
    print('--------------------------------------------------')

    # 병렬 프로세스 간 데이터 공유를 위한 매니저 객체
    manager = Manager()
    progress_dict = manager.dict()
    for i in range(num_workers):
        progress_dict[i] = 0

    # 전체 조합 생성
    all_combinations = itertools.product(chars, repeat=password_length)
    
    # 메모리 효율을 위한 덩어리 크기 설정
    chunk_size = 2000000 
    
    with Pool(processes=num_workers) as pool:
        while True:
            # 조합 덩어리 추출
            raw_chunk = list(itertools.islice(all_combinations, chunk_size))
            if not raw_chunk:
                break
            
            # 각 코어에 배분할 작업 리스트 생성
            sub_size = len(raw_chunk) // num_workers
            tasks = []
            for i in range(num_workers):
                start_idx = i * sub_size
                end_idx = None if i == num_workers - 1 else (i + 1) * sub_size
                tasks.append((file_name, raw_chunk[start_idx:end_idx], progress_dict, i))

            # 비동기로 작업 시작
            result_obj = pool.map_async(check_chunk, tasks)
            
            # 작업이 완료될 때까지 터미널에 진행 상황 출력
            while not result_obj.ready():
                current_total = sum(progress_dict.values())
                elapsed = time.time() - start_time
                if elapsed > 0:
                    speed = current_total / elapsed
                    progress = (current_total / total_combinations) * 100
                    remaining = (total_combinations - current_total) / speed if speed > 0 else 0
                    
                    # 실시간 진행 상황 출력 (\r 사용)
                    print(f'\r[진행] {progress:.4f}% | 속도: {int(speed):,}회/초 | '
                          f'남은시간: {int(remaining/60)}분 {int(remaining%60)}초 ', end='')
                time.sleep(0.1)

            # 결과 확인 및 저장
            for res in result_obj.get():
                if res:
                    print('\n' + '=' * 50)
                    print('암호 해독 성공!')
                    print('찾은 암호:', res)
                    print('총 반복 횟수:', format(current_total, ','))
                    print('총 소요 시간:', int(time.time() - start_time), '초')
                    print('=' * 50)
                    
                    # 결과를 password.txt에 저장
                    with open('password.txt', 'w', encoding='utf-8') as f:
                        f.write(res)
                    return

    print('\n암호를 찾지 못했습니다.')


if __name__ == '__main__':
    unlock_zip()