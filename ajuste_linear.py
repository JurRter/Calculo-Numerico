"""Ajuste linear simples por mínimos quadrados.

Instale a dependência com: python -m pip install matplotlib
Execute: python ajuste_linear.py
Para gerar as imagens sem abrir janelas: python ajuste_linear.py --sem-janela
"""

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt


def ler_par(texto):
    campos = texto.replace(",", ".").split()
    if len(campos) != 2:
        raise ValueError("Digite dois números separados por espaço.")
    u, v = map(float, campos)
    if not (math.isfinite(u) and math.isfinite(v)):
        raise ValueError("Os valores precisam ser finitos.")
    return u, v


def ler_pontos(texto):
    pontos = [ler_par(par) for par in texto.split(";")]
    if len({x for x, y in pontos}) < 2:
        raise ValueError("Informe pelo menos dois valores distintos de x.")
    return pontos


def avaliar_reta(pontos, intercepto, inclinacao):
    previsoes = [intercepto + inclinacao * x for x, y in pontos]
    desvios = [y - previsto for (x, y), previsto in zip(pontos, previsoes)]
    total = sum(d ** 2 for d in desvios)
    return previsoes, desvios, total


def ajustar_reta(pontos):
    xs, ys = zip(*pontos)
    x_medio = sum(xs) / len(xs)
    y_medio = sum(ys) / len(ys)
    sxx = sum((x - x_medio) ** 2 for x in xs)
    sxy = sum((x - x_medio) * (y - y_medio) for x, y in pontos)
    n = sxy / sxx
    m = y_medio - n * x_medio
    return m, n


def numero(valor):
    arredondado = round(valor, 2)
    return f"{arredondado if arredondado else 0:.2f}".replace(".", ",")


def equacao(intercepto, inclinacao):
    sinal = "+" if inclinacao >= 0 else "−"
    return f"y = {numero(intercepto)} {sinal} {numero(abs(inclinacao))}x"


def montar_tabela(pontos, resultados):
    linhas = []
    for i, (x, y) in enumerate(pontos):
        linha = [str(i + 1), numero(x), numero(y)]
        for previsoes, desvios, total in resultados:
            linha.extend([numero(previsoes[i]), numero(desvios[i])])
        linhas.append(linha)
    return linhas


CORES = ("#BA560F", "#416ABE", "#00776E")
ESTILOS = ("--", ":", "-")
ROTULOS = ("Reta A", "Reta B", "Ajuste")


def plotar_grafico(pontos, retas):
    fig, ax = plt.subplots(figsize=(9, 5.6), layout="constrained")
    xs, ys = zip(*pontos)
    margem = (max(xs) - min(xs)) * 0.08
    limites = [min(xs) - margem, max(xs) + margem]
    for (p, q), nome, cor, estilo in zip(retas, ROTULOS, CORES, ESTILOS):
        ax.plot(limites, [p + q * x for x in limites], estilo,
                color=cor, lw=2.8, label=f"{nome}   {equacao(p, q)}")
    ax.scatter(xs, ys, s=65, color="#182637", edgecolors="white",
               linewidths=1.1, zorder=5, label="Pontos amostrados")
    ax.set(xlabel="x", ylabel="y", title="Pontos amostrados e três retas")
    ax.grid(alpha=0.18)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=9)
    return fig


def plotar_tabela(linhas, retas, resultados):
    altura = max(3.3, 1.5 + len(linhas) * 0.38)
    fig, ax = plt.subplots(figsize=(12, altura), layout="constrained")
    ax.axis("off")
    titulos = ["i", "xᵢ", "yᵢ"]
    totais = ["", "", "D"]
    for nome, (p, q), (_, _, total) in zip(ROTULOS, retas, resultados):
        titulos.extend([f"{nome}\nŷᵢ", f"{nome}\ndᵢ"])
        totais.extend(["", numero(total)])
    tabela = ax.table(cellText=[*linhas, totais], colLabels=titulos,
                      cellLoc="center", bbox=[0, 0.02, 1, 0.80])
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(11)
    for (i, j), celula in tabela.get_celld().items():
        cor = "#203347" if j < 3 else CORES[(j - 3) // 2]
        celula.set_edgecolor("#DEE5EA")
        if i == 0:
            celula.set_facecolor(cor)
            celula.set_text_props(color="white", weight="bold")
        elif i == len(linhas) + 1:
            celula.set_facecolor("#E6F1F0")
            celula.set_text_props(weight="bold")
    ax.set_title("Previsões, desvios e soma dos quadrados", weight="bold")
    legenda = "     •     ".join(f"{r}   {equacao(*pq)}" for r, pq in zip(ROTULOS, retas))
    ax.text(0.5, 0.92, legenda, transform=ax.transAxes, ha="center", fontsize=10)
    return fig


def pedir(mensagem, converter):
    while True:
        try:
            return converter(input(mensagem))
        except ValueError as erro:
            print(erro)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sem-janela", action="store_true")
    args = parser.parse_args()
    pontos = pedir("Pontos (x y; x y; ...): ", ler_pontos)
    reta_a = pedir("Reta A (a b): ", ler_par)
    reta_b = pedir("Reta B (c d): ", ler_par)
    retas = [reta_a, reta_b, ajustar_reta(pontos)]
    resultados = [avaliar_reta(pontos, *reta) for reta in retas]
    linhas = montar_tabela(pontos, resultados)
    print("\n" + " | ".join(["i", "x", "y", "ŷ A", "d A", "ŷ B", "d B", "ŷ ajuste", "d ajuste"]))
    for linha in linhas:
        print(" | ".join(linha))
    print()
    for nome, reta, (_, _, total) in zip(ROTULOS, retas, resultados):
        print(f"{nome:6}  {equacao(*reta)}    D = {numero(total)}")
    tabela = plotar_tabela(linhas, retas, resultados)
    grafico = plotar_grafico(pontos, retas)
    for figura, arquivo in [(tabela, "tabela_ajuste.png"), (grafico, "grafico_ajuste.png")]:
        figura.savefig(arquivo, dpi=160)
        print(f"Imagem salva em {Path(arquivo).resolve()}")
    if not args.sem_janela:
        plt.show()
    plt.close("all")


if __name__ == "__main__":
    main()
