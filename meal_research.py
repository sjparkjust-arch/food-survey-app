import pymysql
import re

conn = pymysql.connect(
    host='192.168.32.74',
    port=3306,
    user='testuser',
    password='test1234',
    database='testdb',
    charset='utf8mb4'
)
cursor = conn.cursor()
로그인유저 = None

while True:
    print("╔═══════════════════════════════════╗")
    print("║  ★ 좋아하는 음식 종류 설문조사 ★  ║")
    print("╠═══════════════════════════════════╣")
    if 로그인유저 is None:
        print("║  1. 회원가입                      ║")
        print("║  2. 로그인                        ║")
        print("║  3. 설문 현황보기                 ║")
        print("║  0. 종료                          ║")
    else:
        print(f"║  [{로그인유저}님 로그인 중]             ║")
        print("║  1. 설문 참여하기                 ║")
        print("║  2. 설문 현황보기                 ║")
        print("║  3. 내 투표 기록                  ║")
        print("║  4. 내 투표 취소                  ║")
        print("║  0. 로그아웃                      ║")
    print("╚═══════════════════════════════════╝")
    선택 = input("선택: ")
    print()
    
    if 로그인유저 is None:
        if 선택 == "1":  
            print("[ 회원가입 ]")
            이름 = input("이름 (한글 2~4자): ")
            if not re.match("^[가-힣]{2,4}$", 이름):
                print("이름은 한글 2~4자만 가능합니다!")
            else:
                비번 = input("비밀번호 (숫자 4자리): ")
                if not re.match("^\d{4}$", 비번):
                    print("비밀번호는 숫자 4자리만 가능합니다!")
                else:
                    나이 = input("나이 (숫자만 입력): ")
                    성별 = input("성별 (남/여): ")
                    cursor.execute("SELECT * FROM users WHERE nickname = %s AND age = %s AND gender = %s", (이름, 나이, 성별))
                    if cursor.fetchone():
                        print("이미 가입된 회원입니다!")
                    else:
                        cursor.execute("INSERT INTO users (nickname, password, age, gender) VALUES (%s, %s, %s, %s)", (이름, 비번, 나이, 성별))
                        conn.commit()
                        print(f"{이름}님 회원가입 완료!")
        elif 선택 == "2":
            print("[ 로그인 ]")
            이름 = input("이름: ")
            비번 = input("비밀번호: ")
            나이 = input("나이: ")
            성별 = input("성별 (남/여): ")
            cursor.execute("SELECT * FROM users WHERE nickname = %s AND age = %s AND gender = %s AND password = %s", (이름, 나이, 성별, 비번))
            if cursor.fetchone():
                로그인유저 = 이름
                print(f"{이름}님 환영합니다!")
            else:
                print("정보가 일치하지 않습니다!")
        elif 선택 == "3":  
            print("[ 설문 결과 ]")
            cursor.execute("SELECT COUNT(*) FROM survey")
            total = cursor.fetchone()[0]
            음식목록 = ['한식', '중식', '일식', '양식']
            for i, 음식 in enumerate(음식목록, 1):
                cursor.execute("SELECT COUNT(*) FROM survey WHERE food = %s", (음식,))
                count = cursor.fetchone()[0]
                퍼센트 = round(count/total*100) if total > 0 else 0
                print(f"{i}. {음식} ===> {count}표 ({퍼센트}%)")
            print()
            cursor.execute("SELECT food, COUNT(*) FROM survey WHERE food NOT IN ('한식','중식','일식','양식') GROUP BY food")
            기타결과 = cursor.fetchall()
            print("[기타 항목]")
            for 행 in 기타결과:
                퍼센트 = round(행[1]/total*100) if total > 0 else 0
                print(f"{행[0]} ===> {행[1]}표 ({퍼센트}%)")
            print(f"총 {total}명 참여")
            print()
            cursor.execute("SELECT food, COUNT(*) FROM survey GROUP BY food ORDER BY COUNT(*) DESC")
            firstfood = cursor.fetchall()
            if firstfood:
                최고표수 = firstfood[0][1]
                최다목록 = [행 for 행 in firstfood if 행[1] == 최고표수]
                print("[현재 1위]")
                for 행 in 최다목록:
                    퍼센트 = round(행[1]/total*100) if total > 0 else 0
                    print(f"{행[0]} ===> {행[1]}표 ({퍼센트}%)") 
            print()
            while True:
                상세보기 = input("더 자세한 통계를 보시겠습니까? (예/아니오): ")
                if 상세보기 == "예":
                    print()
                    print("[ 성별 통계 ]")
                    for 성별 in ['남', '여']:
                        cursor.execute("""
                            SELECT food, COUNT(*) as cnt FROM survey 
                            WHERE nickname IN (SELECT nickname FROM users WHERE gender = %s)
                            GROUP BY food ORDER BY cnt DESC LIMIT 1
                        """, (성별,))
                        결과 = cursor.fetchone()
                        if 결과:
                            print(f"{성별}성 ===> {결과[0]} 선호 ({결과[1]}명)")
                        else:
                            print(f"{성별}성 ===> 데이터 없음")
                    print()
                    print("[ 연령대 통계 ]")
                    for 연령대 in [10, 20, 30, 40, 50]:
                        cursor.execute("""
                            SELECT food, COUNT(*) as cnt FROM survey 
                            WHERE nickname IN (SELECT nickname FROM users WHERE age >= %s AND age < %s)
                            GROUP BY food ORDER BY cnt DESC LIMIT 1
                        """, (연령대, 연령대+10))
                        결과 = cursor.fetchone()
                        if 결과:
                            print(f"{연령대}대 ===> {결과[0]} 선호 ({결과[1]}명)")
                        else:
                            print(f"{연령대}대 ===> 데이터 없음")
                    break
                elif 상세보기 == "아니오":
                    print("메인 메뉴로 돌아갑니다.")
                    break
                else:
                    print("예 또는 아니오만 입력해주세요!")
                    
        elif 선택 == "0":
            print("종료합니다.")
            conn.close()
            break
        
    else:  
        if 선택 == "1":  
            cursor.execute("SELECT * FROM survey WHERE nickname = %s", (로그인유저,))
            if cursor.fetchone():
                print("이미 투표하셨습니다!")
            else:
                print("좋아하는 음식을 선택해주세요.")
                print()
                print("1. 한식")
                print("2. 중식")
                print("3. 일식")
                print("4. 양식")
                print("5. 기타")
                print()
                음식선택 = input("선택(숫자만 입력): ")
                if 음식선택 == "1":
                    cursor.execute("INSERT INTO survey (nickname, food) VALUES (%s, %s)", (로그인유저, '한식'))
                    conn.commit()
                    print("설문 완료!")
                elif 음식선택 == "2":
                    cursor.execute("INSERT INTO survey (nickname, food) VALUES (%s, %s)", (로그인유저, '중식'))
                    conn.commit()
                    print("설문 완료!")
                elif 음식선택 == "3":
                    cursor.execute("INSERT INTO survey (nickname, food) VALUES (%s, %s)", (로그인유저, '일식'))
                    conn.commit()
                    print("설문 완료!")
                elif 음식선택 == "4":
                    cursor.execute("INSERT INTO survey (nickname, food) VALUES (%s, %s)", (로그인유저, '양식'))
                    conn.commit()
                    print("설문 완료!")
                elif 음식선택 == "5":
                    기타입력 = input("어떤 음식 종류를 좋아하십니까?: ")
                    cursor.execute("INSERT INTO survey (nickname, food) VALUES (%s, %s)", (로그인유저, 기타입력))
                    conn.commit()
                    print("설문 완료!")
        elif 선택 == "2":  
            print("[ 설문 결과 ]")
            cursor.execute("SELECT COUNT(*) FROM survey")
            total = cursor.fetchone()[0]
            음식목록 = ['한식', '중식', '일식', '양식']
            for i, 음식 in enumerate(음식목록, 1):
                cursor.execute("SELECT COUNT(*) FROM survey WHERE food = %s", (음식,))
                count = cursor.fetchone()[0]
                퍼센트 = round(count/total*100) if total > 0 else 0
                print(f"{i}. {음식} ===> {count}표 ({퍼센트}%)")
            print()
            cursor.execute("SELECT food, COUNT(*) FROM survey WHERE food NOT IN ('한식','중식','일식','양식') GROUP BY food")
            기타결과 = cursor.fetchall()
            print("[기타 항목]")
            for 행 in 기타결과:
                퍼센트 = round(행[1]/total*100) if total > 0 else 0
                print(f"{행[0]} ===> {행[1]}표 ({퍼센트}%)")
            print(f"총 {total}명 참여")
            print()
            cursor.execute("SELECT food, COUNT(*) FROM survey GROUP BY food ORDER BY COUNT(*) DESC")
            firstfood = cursor.fetchall()
            if firstfood:
                최고표수 = firstfood[0][1]
                최다목록 = [행 for 행 in firstfood if 행[1] == 최고표수]
                print("[현재 1위]")
                for 행 in 최다목록:
                    퍼센트 = round(행[1]/total*100) if total > 0 else 0
                    print(f"{행[0]} ===> {행[1]}표 ({퍼센트}%)")
            print()
            while True:
                상세보기 = input("더 자세한 통계를 보시겠습니까? (예/아니오): ")
                if 상세보기 == "예":
                    print()
                    print("[ 성별 통계 ]")
                    for 성별 in ['남', '여']:
                        cursor.execute("""
                            SELECT food, COUNT(*) as cnt FROM survey 
                            WHERE nickname IN (SELECT nickname FROM users WHERE gender = %s)
                            GROUP BY food ORDER BY cnt DESC LIMIT 1
                        """, (성별,))
                        결과 = cursor.fetchone()
                        if 결과:
                            print(f"{성별}성 ===> {결과[0]} 선호 ({결과[1]}명)")
                        else:
                            print(f"{성별}성 ===> 데이터 없음")
                    print()
                    print("[ 연령대 통계 ]")
                    for 연령대 in [10, 20, 30, 40, 50]:
                        cursor.execute("""
                            SELECT food, COUNT(*) as cnt FROM survey 
                            WHERE nickname IN (SELECT nickname FROM users WHERE age >= %s AND age < %s)
                            GROUP BY food ORDER BY cnt DESC LIMIT 1
                        """, (연령대, 연령대+10))
                        결과 = cursor.fetchone()
                        if 결과:
                            print(f"{연령대}대 ===> {결과[0]} 선호 ({결과[1]}명)")
                        else:
                            print(f"{연령대}대 ===> 데이터 없음")
                    break
                elif 상세보기 == "아니오":
                    print("메인 메뉴로 돌아갑니다.")
                    break
                else:
                    print("예 또는 아니오만 입력해주세요!")
                 
                    
        elif 선택 == "3":  
            cursor.execute("SELECT food, voted_at FROM survey WHERE nickname = %s", (로그인유저,))
            내기록 = cursor.fetchone()
            if 내기록:
                print(f"[ {로그인유저}님의 투표 기록 ]")
                print(f"투표 음식: {내기록[0]}")
                print(f"투표 시간: {내기록[1]}")
            else:
                print("아직 투표하지 않으셨습니다!")
        elif 선택 == "4":  
            cursor.execute("SELECT food FROM survey WHERE nickname = %s", (로그인유저,))
            내기록 = cursor.fetchone()
            if 내기록:
                print(f"현재 투표: {내기록[0]}")
                확인 = input("정말 취소하시겠습니까? (예/아니오): ")
                if 확인 == "예":
                    cursor.execute("INSERT INTO cancel_log (nickname, food) VALUES (%s, %s)", (로그인유저, 내기록[0]))
                    cursor.execute("DELETE FROM survey WHERE nickname = %s", (로그인유저,))
                    conn.commit()
                    print("투표가 취소되었습니다.")
            else:
                print("취소할 투표가 없습니다!")
        elif 선택 == "0":  
            print(f"{로그인유저}님 로그아웃 됩니다.")
            로그인유저 = None