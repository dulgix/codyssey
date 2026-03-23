# 파일 경로 설정
input_file = 'Mars_Base_Inventory_List.csv'
output_danger_csv = 'Mars_Base_Inventory_danger.csv'
output_bin = 'Mars_Base_Inventory_List.bin'

# --- [과제 1] 파일 내용을 그대로 읽어서 출력 ---
print("--- [과제 1] 파일 내용 출력 ---")
try:
    with open(input_file, mode='r', encoding='utf-8') as f:
        content = f.read()
        print(content)
except FileNotFoundError:
    print(f"{input_file} 파일을 찾을 수 없습니다.")

# --- [과제 2] 내용을 리스트(List) 객체로 변환 ---
inventory_list = []
try:
    with open(input_file, mode='r', encoding='utf-8') as f:
        # 첫 줄(헤더) 분리 보관
        header_line = f.readline().strip()
        header = header_line.split(',')
        
        # 데이터 리스트 변환
        for line in f:
            if line.strip():
                inventory_list.append(line.strip().split(','))

    print("\n--- [과제 2] 리스트 객체 변환 완료 ---")
    for item in inventory_list[:5]: # 너무 길 수 있으니 5개만 샘플 출력
        print(item)
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")

# --- [과제 3] 인화성(index 4) 높은 순으로 정렬 ---
# 문자열인 인화성 지수를 float으로 변환하여 정렬
inventory_list.sort(key=lambda x: float(x[4]), reverse=True)

print("\n--- [과제 3] 인화성 높은 순 정렬 결과 (상위 5개) ---")
print(header)
for row in inventory_list[:5]:
    print(row)

# --- [과제 4] 인화성 지수 0.7 이상 목록 출력 ---
print("\n--- [과제 4] 인화성 지수 0.7 이상 목록 ---")
danger_list = [row for row in inventory_list if float(row[4]) >= 0.7]
print(header_line) # CSV 형식으로 출력하기 위해 원본 헤더 사용
for row in danger_list:
    print(",".join(row))

# --- [과제 5] 0.7 이상 목록을 CSV로 저장 ---
with open(output_danger_csv, mode='w', encoding='utf-8') as f:
    f.write(header_line + "\n")
    for row in danger_list:
        f.write(",".join(row) + "\n")
print(f"\n--- [과제 5] 위험 목록 저장 완료: {output_danger_csv} ---")

# --- [이진 파일 과제] 정렬된 내용을 .bin으로 저장하고 다시 읽기 ---
try:
    # 1. 이진 파일로 저장 (Write Binary)
    with open(output_bin, mode='wb') as f:
        # 헤더와 정렬된 전체 데이터를 합침
        full_text = header_line + "\n"
        for row in inventory_list:
            full_text += ",".join(row) + "\n"
        
        # 인코딩하여 이진 데이터로 변환 후 저장
        f.write(full_text.encode('utf-8'))
    print(f"\n--- 이진 파일 저장 완료: {output_bin} ---")

    # 2. 이진 파일 읽어서 출력 (Read Binary)
    with open(output_bin, mode='rb') as f:
        binary_data = f.read()
        decoded_text = binary_data.decode('utf-8')
        
        print("\n--- 이진 파일로부터 읽어온 내용 ---")
        print(decoded_text[:500]) # 내용이 많을 수 있어 앞부분만 출력
except Exception as e:
    print(f"이진 파일 처리 중 오류 발생: {e}")