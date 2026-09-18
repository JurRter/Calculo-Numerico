from math import sqrt
import matplotlib.pyplot as plt

def f(x):
    return x**2 - 2


print("Método da Bisseção: f(x) = x² - 2")
a = float(input("Extremo a [1]: ") or 1)
b = float(input("Extremo b [2]: ") or 2)
n = int(input("Precisão n [3]: ") or 3)
tolerancia = 10**(-n)

if a >= b or not 1 <= n <= 15:
    raise SystemExit("Use a < b e n entre 1 e 15.")
if f(a) * f(b) > 0:
    raise SystemExit("Escolha um intervalo com f(a) e f(b) de sinais opostos.")

inicio, fim = a, b
pontos = []
anterior = None
iteracao = 1

print(f"\n{'i':>3} {'a':>10} {'b':>10} {'x':>10} {'f(x)':>12} {'Diferença':>12}")
if f(a) == 0:
    x = a
elif f(b) == 0:
    x = b
else:
    while True:
        x = (a + b) / 2
        fx = f(x)
        diferenca = abs(x - anterior) if anterior is not None else None
        pontos.append(x)
        texto = f"{diferenca:.6f}" if diferenca is not None else "-"
        print(f"{iteracao:3} {a:10.6f} {b:10.6f} {x:10.6f} {fx:12.6f} {texto:>12}")

        if fx == 0:
            break
        if x == a or x == b:
            raise SystemExit("Limite da precisão do computador atingido.")
        if diferenca is not None and diferenca < tolerancia:
            break

        if f(a) * fx < 0:
            b = x
        else:
            a = x
        anterior = x
        iteracao += 1

print(f"\nRaiz {'exata' if f(x) == 0 else 'aproximada'}: {x:.9f}")

raiz_exata = sqrt(2) if x > 0 else -sqrt(2)
valores = [inicio + (fim - inicio) * i / 200 for i in range(201)]
plt.plot(valores, [f(v) for v in valores], label="f(x) = x² - 2")
plt.axhline(0, color="gray", linewidth=0.8)
plt.scatter(pontos, [f(p) for p in pontos], color="orange", label="Iterações")
plt.axvline(raiz_exata, color="green", linestyle=":", label=f"Raiz exata ≈ {raiz_exata:.6f}")
plt.axvline(x, color="red", linestyle="--", label=f"Raiz calculada ≈ {x:.6f}")
plt.title("Método da Bisseção")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid()
plt.show()
