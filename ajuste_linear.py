import matplotlib.pyplot as plt


def ler_par(texto):
    primeiro, segundo = texto.replace(",", ".").split()
    return float(primeiro), float(segundo)

entrada = input("Pontos (x y; x y; ...): ")
pontos = [ler_par(par) for par in entrada.split(";")]
x, y = zip(*pontos)

if min(x) == max(x):
    raise SystemExit("Informe pelo menos dois valores diferentes de x.")

a, b = ler_par(input("Reta A (a b): "))
c, d = ler_par(input("Reta B (c d): "))

media_x = sum(x) / len(x)
media_y = sum(y) / len(y)

soma_xy = sum((xi - media_x) * (yi - media_y) for xi, yi in pontos)
soma_xx = sum((xi - media_x) ** 2 for xi in x)

n = soma_xy / soma_xx
m = media_y - n * media_x

retas = [(a, b), (c, d), (m, n)]
totais = [0, 0, 0]
tabela = []

for i, (xi, yi) in enumerate(pontos, start=1):
    linha = [i, xi, yi]

    for j, (intercepto, inclinacao) in enumerate(retas):
        previsto = intercepto + inclinacao * xi
        desvio = yi - previsto
        totais[j] += desvio ** 2
        linha.extend([f"{previsto:.2f}", f"{desvio:.2f}"])

    tabela.append(linha)

tabela.append([
    "D", "", "",
    "", f"{totais[0]:.2f}",
    "", f"{totais[1]:.2f}",
    "", f"{totais[2]:.2f}"
])


colunas = [
    "i", "x", "y", "ŷ A", "Desvio A",
    "ŷ B", "Desvio B", "ŷ ajuste", "Desvio ajuste"
]
plt.figure(figsize=(10, max(3, len(pontos) * 0.35 + 1)))
plt.axis("off")
plt.table(cellText=tabela, colLabels=colunas, cellLoc="center", loc="center")


plt.figure()
plt.scatter(x, y, color="black", label="Pontos", zorder=3)
extremos = [min(x), max(x)]

for (intercepto, inclinacao), nome in zip(retas, ["A", "B", "Ajuste"]):
    alturas = [intercepto + inclinacao * xi for xi in extremos]
    plt.plot(extremos, alturas, label=f"{nome}: y = {intercepto:g} {inclinacao:+g}x")

plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()