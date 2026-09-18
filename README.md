# Método da Bisseção

Programa em Python que encontra uma raiz aproximada de **f(x) = x² − 2**,
mostrando a tabela das iterações e um gráfico.

## Como executar

Com o Python instalado, abra o terminal na pasta do projeto.

1. Instale a biblioteca usada no gráfico:

   ```bash
   python -m pip install matplotlib
   ```

2. Execute o programa:

   ```bash
   python bissecao.py
   ```

3. Informe os valores solicitados ou pressione **Enter** para usar os padrões:

   | Entrada | Significado | Padrão |
   | --- | --- | --- |
   | `a` | Início do intervalo | `1` |
   | `b` | Fim do intervalo | `2` |
   | `n` | Define a tolerância como `10⁻ⁿ` | `3` |

Use ponto para números decimais, como `1.5`. O valor de `a` deve ser menor
que `b`, e `n` deve ser um inteiro entre 1 e 15. As extremidades devem ter
valores da função com sinais opostos, ou uma delas já deve ser uma raiz.

## Exemplo do roteiro

Pressione **Enter nas três perguntas** para usar `[1, 2]` e tolerância `0.001`.
O resultado será:

```text
Raiz aproximada: 1.415039063
```

São feitas **10 iterações**. A tabela mostra os extremos, o ponto médio `x`,
o valor `f(x)` e a diferença entre os pontos médios consecutivos.
O programa para quando essa diferença é menor que a tolerância ou `f(x)` é zero.

O gráfico abre em uma janela, mostrando a função, as iterações, a raiz
calculada e a raiz exata de referência (`√2` neste exemplo). Feche a janela
para encerrar o programa.

A função está definida em `f(x)` no arquivo `bissecao.py`. Se alterá-la,
ajuste também os textos do gráfico e a variável `raiz_exata`, e escolha
um intervalo em que a nova função seja contínua.
