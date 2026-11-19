# Biên dịch nguồn

Dùng LuaLaTeX với fontspec, polyglossia, unicode-math và các gói LaTeX tiêu chuẩn
được nêu trong nguồn. Cần TeX Gyre Pagella, TeX Gyre Heros, TeX Gyre Cursor và
Latin Modern Math; các phông không nằm trong gói nguồn.

Trong thư mục gốc, chạy `lualatex -no-shell-escape FGA_vi_diplomatic.tex`, lặp lại
tới khi mục lục và dẫn chiếu ổn định. Tệp `FGA_vi_diplomatic_direct.tex` chứa cùng
nội dung trong một tệp và có thể biên dịch bằng cùng công cụ.
