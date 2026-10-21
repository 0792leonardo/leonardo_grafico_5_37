#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gráfico 5.37 – Aldeídos - Perfil das concentrações diárias – Congonhas – 2025
================================================================================

Este script gera um gráfico interativo em HTML mostrando a evolução temporal
das concentrações de dois aldeídos atmosféricos:
- Formaldeído (HCHO)
- Acetaldeído (CH₃CHO)

DIFERENCIAL: O script detecta automaticamente os nomes das colunas no CSV,
tolerando variações como acentos, maiúsculas/minúsculas e idiomas diferentes.
Isso torna o script robusto para diferentes fontes de dados.

Formaldeído e Acetaldeído = Compostos Orgânicos Voláteis (COVs) que são
precursores do ozônio troposférico e têm efeitos adversos à saúde (irritantes
respiratórios e possíveis carcinogênicos).

Autor: Leonardo Rocha
Data: 2026-09-21
Versão: 1.0.0
"""

# =============================================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =============================================================================

from pathlib import Path  # Para manipulação de caminhos de arquivos de forma segura
import pandas as pd       # Para leitura e manipulação de dados em tabelas (DataFrames)
import plotly.graph_objects as go  # Para criação de gráficos interativos


# =============================================================================
# LEITURA DOS DADOS
# =============================================================================

# Define o caminho do arquivo CSV com os dados
CSV = Path("Dd_grafico_5_37.csv")

# Lê o arquivo CSV com parâmetros específicos para o padrão brasileiro:
# - sep=";": separador ponto-e-vírgula
# - decimal=",": vírgula como separador decimal
# - encoding="utf-8-sig": remove o BOM automaticamente
df = pd.read_csv(CSV, sep=";", decimal=",", encoding="utf-8-sig")

# Normaliza os nomes das colunas removendo espaços em branco extras
# Exemplo: " Data " → "Data", "formaldeído " → "formaldeído"
df.columns = [str(c).strip() for c in df.columns]


# =============================================================================
# DETECÇÃO AUTOMÁTICA DE COLUNAS
# =============================================================================

def find_col(candidates):
    """
    Encontra uma coluna no DataFrame baseado em uma lista de nomes candidatos.
    
    A função tenta em duas etapas:
    1. Correspondência EXATA (case-insensitive): "data" == "Data"
    2. Correspondência PARCIAL (substring): "data" in "data_coleta"
    
    Isso torna o script robusto a variações nos nomes das colunas, como:
    - "data", "Data", "DATA"
    - "formaldeído", "formaldeido", "Formaldehyde"
    - "acetaldeído", "acetaldeido", "Acetaldehyde"
    
    Args:
        candidates (list): Lista de nomes candidatos para a coluna
    
    Returns:
        str ou None: Nome real da coluna no DataFrame, ou None se não encontrada
    """
    # Cria um dicionário de nomes normalizados (minúsculos, sem espaços)
    # Exemplo: {"data": "Data", "formaldeído": "Formaldeído"}
    normalized = {str(c).strip().lower(): c for c in df.columns}
    
    # ETAPA 1: Tenta correspondência exata (case-insensitive)
    for cand in candidates:
        if cand.lower() in normalized:
            return normalized[cand.lower()]
    
    # ETAPA 2: Tenta correspondência parcial (substring)
    # Útil para nomes compostos como "data_coleta", "formaldeido_ppb"
    for c in df.columns:
        cl = str(c).strip().lower()
        if any(cand.lower() in cl for cand in candidates):
            return c
    
    # Não encontrou nenhuma coluna correspondente
    return None


# Detecta automaticamente as colunas no DataFrame
# Aceita variações em português, inglês e com/sem acentos
date_col = find_col(["data", "date"])                                    # Coluna de data
form_col = find_col(["formaldeído", "formaldeido", "formaldehyde"])      # Formaldeído
acet_col = find_col(["acetaldeído", "acetaldeido", "acetaldehyde"])      # Acetaldeído


# =============================================================================
# PREPARAÇÃO DOS DADOS
# =============================================================================

# --- Conversão da coluna de data para datetime ---
# dayfirst=True: interpreta "01/02/2024" como 1º de fevereiro (padrão brasileiro)
# errors="coerce": datas inválidas se tornam NaT (Not a Time)
df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce")

# --- Conversão das colunas de concentração para numérico ---
# Aceita vírgula como separador decimal (padrão brasileiro)
for c in [form_col, acet_col]:
    df[c] = pd.to_numeric(
        df[c].astype(str).str.replace(",", ".", regex=False),
        errors="coerce"  # Valores inválidos se tornam NaN
    )

# --- Ordenação cronológica ---
# Ordena o DataFrame pela data e reinicia o índice
# reset_index(drop=True) remove o índice antigo e cria um novo (0, 1, 2, ...)
df = df.sort_values(date_col).reset_index(drop=True)


# =============================================================================
# PREPARAÇÃO DOS RÓTULOS DO EIXO X
# =============================================================================

# Cria rótulos de data no formato brasileiro (DD/MM/AA) para o eixo X
# Exemplo: "15/03/24"
# Se a data for NaT (inválida), usa string vazia
xlabels = [
    d.strftime("%d/%m/%y") if pd.notna(d) else ""
    for d in df[date_col]
]


# =============================================================================
# CRIAÇÃO DO GRÁFICO
# =============================================================================

# Inicializa uma figura vazia
fig = go.Figure()


# -----------------------------------------------------------------------------
# TRAÇO 1: FORMALDEÍDO (LINHA AZUL)
# -----------------------------------------------------------------------------
fig.add_trace(go.Scatter(
    x=xlabels,                                # Eixo X: datas formatadas
    y=df[form_col],                           # Eixo Y: concentrações de formaldeído
    
    # Modo: linha conectando pontos + marcadores nos pontos
    mode="lines+markers",
    
    # Nome na legenda
    name="Formaldeído",
    
    # Não conecta gaps (NaN) - a linha terá interrupções onde faltam dados
    connectgaps=False,
    
    # Configuração da linha
    line=dict(
        color="#5B9BD5",                      # Azul claro
        width=2.2                             # Espessura da linha
    ),
    
    # Configuração dos marcadores
    marker=dict(
        color="#5B9BD5",                      # Cor azul
        symbol="circle",                      # Forma: círculo
        size=7                                # Tamanho do marcador
    ),
    
    # Dados customizados para o tooltip (formatados com vírgula decimal)
    customdata=[
        "" if pd.isna(v) else f"{float(v):.1f}".replace(".", ",")
        for v in df[form_col]
    ],
    
    # Template do tooltip usando customdata
    hovertemplate=(
        "<b>Formaldeído</b><br>"              # Título em negrito
        "Concentração: %{customdata} ppb<extra></extra>"  # Valor em ppb
    )
))


# -----------------------------------------------------------------------------
# TRAÇO 2: ACETALDEÍDO (LINHA MARROM)
# -----------------------------------------------------------------------------
fig.add_trace(go.Scatter(
    x=xlabels,                                # Eixo X: datas formatadas
    y=df[acet_col],                           # Eixo Y: concentrações de acetaldeído
    
    # Modo: linha conectando pontos + marcadores
    mode="lines+markers",
    
    # Nome na legenda
    name="Acetaldeído",
    
    # Não conecta gaps
    connectgaps=False,
    
    # Configuração da linha
    line=dict(
        color="#9E480E",                      # Marrom
        width=2.2                             # Espessura da linha
    ),
    
    # Configuração dos marcadores
    marker=dict(
        color="#9E480E",                      # Cor marrom
        symbol="triangle-up",                 # Forma: triângulo para cima
        size=8                                # Tamanho ligeiramente maior
    ),
    
    # Dados customizados para o tooltip
    customdata=[
        "" if pd.isna(v) else f"{float(v):.1f}".replace(".", ",")
        for v in df[acet_col]
    ],
    
    # Template do tooltip
    hovertemplate=(
        "<b>Acetaldeído</b><br>"
        "Concentração: %{customdata} ppb<extra></extra>"
    )
))


# =============================================================================
# CONFIGURAÇÃO DO LAYOUT (APARÊNCIA DO GRÁFICO)
# =============================================================================

fig.update_layout(
    # Tema claro com fundo branco
    template="plotly_white",
    
    # Altura da figura em pixels
    height=760,
    
    # Margens ao redor do gráfico
    # Margem inferior (185px) para acomodar rótulos rotacionados e legenda
    margin=dict(l=92, r=35, t=25, b=185),
    
    # Cor de fundo do papel (área externa ao gráfico)
    paper_bgcolor="#ffffff",                  # Branco
    
    # Cor de fundo da área do gráfico
    plot_bgcolor="#ffffff",                   # Branco
    
    # Modo de hover: exibe tooltip apenas da série mais próxima
    hovermode="x unified",
    
    # Configuração da fonte global
    font=dict(
        family="Arial, sans-serif",           # Fonte sans-serif
        size=14,                              # Tamanho padrão
        color="#555555"                       # Cinza escuro
    ),
    
    # Configuração do eixo X (horizontal)
    xaxis=dict(
        type="category",                      # Tipo categórico (rótulos de data)
        tickmode="array",                     # Ticks definidos manualmente
        tickvals=xlabels,                     # Posições dos ticks
        ticktext=xlabels,                     # Rótulos dos ticks
        tickangle=-90,                        # Rotação de -90° (vertical)
        showgrid=False,                       # Sem linhas de grade verticais
        zeroline=False,                       # Sem linha no zero
        showline=True,                        # Mostra a linha do eixo
        linecolor="#AAAAAA",                   # Cor da linha do eixo (cinza claro)
        ticks="inside",                            # Marcadores dentro do eixo
        range=[-0.0, len(xlabels) - 0.0],             # Cola o 1º ponto no eixo Y
        categoryorder="array",                         # Mantém ordem original
        categoryarray=xlabels,                         # Ordem das categorias
    ),
    
    # Configuração do eixo Y (vertical)
    yaxis=dict(
        title="Concentração (ppb)",           # Título do eixo
        range=[0, 8],                         # Limites: 0 a 8 ppb
        dtick=1,                              # Intervalo de 1 em 1 ppb
        
        # Ticks personalizados com formato brasileiro (vírgula decimal)
        tickvals=list(range(0, 9)),           # Posições: 0, 1, 2, ..., 8
        ticktext=[f"{i},0" for i in range(0, 9)],  # Rótulos: "0,0", "1,0", ..., "8,0"
        
        showgrid=True,                        # Mostra linhas de grade horizontais
        gridcolor="rgba(130,130,130,0.55)",   # Cinza com 55% de opacidade
        griddash="dot",                       # Linhas pontilhadas
        zeroline=False,                       # Sem linha no zero
        showline=True,                        # Mostra a linha do eixo
        linecolor="#AAAAAA",                   # Cor da linha do eixo
        ticks="outside"                           # Marcadores fora do eixo
    ),
    
    # Configuração da legenda
    legend=dict(
        orientation="h",                      # Horizontal
        yanchor="top",                        # Âncora no topo
        y=-0.17,                              # Posicionada abaixo do gráfico
        xanchor="center",                     # Centralizada horizontalmente
        x=0.5,                                # Centro do eixo X
        font=dict(size=12)                    # Tamanho da fonte da legenda
    )
)


# =============================================================================
# EXPORTAÇÃO DO GRÁFICO
# =============================================================================

# Salva o gráfico em um arquivo HTML (autônomo, com Plotly embutido)
fig.write_html(
    "index.html",                             # Nome do arquivo de saída
    include_plotlyjs=True,                    # Inclui a biblioteca Plotly (offline)
    full_html=True,                           # Gera um documento HTML completo
    config={                                  # Configurações do gráfico
        "responsive": True,                   # Gráfico se adapta à tela
        "displaylogo": False,                 # Remove o logo da Plotly
        "scrollZoom": True                    # Permite zoom com scroll
    }
)


# =============================================================================
# MENSAGEM DE CONFIRMAÇÃO
# =============================================================================

print("=" * 70)
print("✅ GRÁFICO DE ALDEÍDOS GERADO COM SUCESSO!")
print("=" * 70)
print(f"📊 Arquivo: index.html")
print(f"📍 Local: {Path.cwd()}")
print(f"📈 Registros: {len(df)}")
print(f"📅 Período: {df[date_col].min().strftime('%d/%m/%Y')} a {df[date_col].max().strftime('%d/%m/%Y')}")
print(f"🔍 Colunas detectadas automaticamente:")
print(f"   • Data: {date_col}")
print(f"   • Formaldeído: {form_col}")
print(f"   • Acetaldeído: {acet_col}")
print(f"📊 Formaldeído: {df[form_col].min():.2f} a {df[form_col].max():.2f} ppb")
print(f"📊 Acetaldeído: {df[acet_col].min():.2f} a {df[acet_col].max():.2f} ppb")
print("=" * 70)
print("🌐 Abra o arquivo no navegador para visualizar o gráfico interativo.")