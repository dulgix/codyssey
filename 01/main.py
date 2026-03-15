try:
    with open("mission_computer_main.log", "r", encoding="utf-8") as file:
        lines = file.readlines()
        
    for line in reversed(lines):
        print(line.strip())

    problems = []

    for line in lines:
        if "unstable" in line.lower() or "explosion" in line.lower():
            problems.append(line)

    if problems:
        with open("problem_log.log", "w", encoding="utf-8") as f:
            f.writelines(problems)
    else:
        print("문제 로그가 발견되지 않았습니다.")

except FileNotFoundError:
    print("오류: 로그 파일을 찾을 수 없습니다.")

except PermissionError:
    print("오류: 파일에 접근할 권한이 없습니다.")

except UnicodeDecodeError:
    print("오류: 파일 인코딩 문제로 읽을 수 없습니다.")

except Exception as e:
    print("알 수 없는 오류 발생:", e)