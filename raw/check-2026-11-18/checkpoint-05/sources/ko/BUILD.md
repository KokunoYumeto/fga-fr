# 한국어 누적판의 소스

이 소스는 여덟 FGA 강연과 정오표 및 1962년 논평을 포함합니다.
`source/main.tex`는 모듈식 소스이고 `FGA_Korean_Current_Direct.tex`는
같은 내용을 한 파일에 모은 직접 편집용 소스입니다.

XeLaTeX와 표준 LaTeX 패키지, Malgun Gothic 및 Malgun Gothic Bold,
TeX Gyre Cursor, Latin Modern Math 글꼴이 필요합니다. 글꼴은 이 묶음에
포함되지 않으며 해당 시스템과 패키지의 조건에 따라 설치해야 합니다.

`source` 디렉터리에서 `xelatex -no-shell-escape main.tex`를 실행하고
목차와 참조가 안정될 때까지 반복하십시오. 직접 편집용 파일도 같은
XeLaTeX 명령으로 컴파일할 수 있습니다.
