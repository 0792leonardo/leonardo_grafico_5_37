# Gráfico 5.37 — Formaldeído e Acetaldeído

Gráfico interativo em Python + Plotly baseado no `Dd_grafico_5_37.csv`.

## Visual

- Formaldeído: linha azul com marcadores circulares.
- Acetaldeído: linha marrom com marcadores triangulares.
- Eixo Y: 0–8 ppb.
- Intervalos: 1 ppb.
- Separador decimal exibido como **vírgula**.
- Datas no eixo X no formato `dd/mm/yy`, inclinadas verticalmente.
- Fundo `#DDE9F4`.
- Grade horizontal pontilhada.
- Tooltip interativo.
- Zoom.
- HTML autocontido para GitHub Pages.

## CSV

O pacote preserva o CSV original, utilizando `;` como separador de campos e `,` como separador decimal.

## Gerar

```bash
pip install pandas plotly
python gerar_grafico.py
```

## Publicar

```bash
git init
git add .
git commit -m "Adicionar grafico 5.37"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

No GitHub:
**Settings → Pages → Build and deployment → Source → GitHub Actions**
