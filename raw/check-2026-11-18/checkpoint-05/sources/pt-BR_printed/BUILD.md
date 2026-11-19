# Compilação

Use XeLaTeX com os pacotes `geometry`, `fontspec`, `babel` (português brasileiro), `microtype`, `graphicx`, `mathtools`, `amsthm`, `unicode-math`, `bookmark` e `hyperref`. Fontes: TeX Gyre Pagella, Heros, Cursor e Latin Modern Math.

No diretório `pt_BR`, execute três vezes:

```text
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error FGA_PTBR_PRINTED.tex
```

A fonte direta pode ser compilada separadamente, com os mesmos pacotes e fontes. O documento contém texto e fórmulas editáveis; as exposições e suas erratas permanecem separadas.
