1. 라이브러리 설치
	sudo apt install g++-multilib            
	sudo apt install make

2. 실습 방법
	2.1 datalab-handout 디렉터리로 이동
	2.2 bits.c 파일을 에디터로 오픈 
	2.2 비어있는 함수의 내용을 수정(함수 위의 주석을 참고) 후 저장
	2.3 ./driver.pl bits.c 실행
	2.4 실행 결과를 확인 

	주의사항 : 각 함수별 사용 가능한 연산자만 사용 해야 함. (연산자 개수 제한 있음)

	풀이 예제 : bits_sample.c 의 bitOr 참고.

3. 유틸리티 사용법 (비트 확인)	
	1. datalab-handout 디렉터리로 이동
	2. make 실행
	3. ishow, fshow 생성
	ex) 
	./ishow 1
	결과 값 : Hex = 0x00000001,	Signed = 1,	Unsigned = 1
	
	./ishow -1
	결과 값 : Hex = 0xffffffff,	Signed = -1,	Unsigned = 4294967295

	./fshow 2080374784
	결과 값: Floating point value 2.658455992e+36	Bit Representation 0x7c000000, 
	sign = 0, exponent = f8, fraction = 000000
	Normalized. 1.0000000000 X 2ˆ(121)
