# SOLUÇÃO DOS EXERCÍCIOS DA LISTA 1 DE PESQUISA OPERACIONAL - UFF - 2024.2

from mip import Model, xsum, maximize, CONTINUOUS, INTEGER, OptimizationStatus
import matplotlib.pyplot as plt
import numpy as np

####################################### PROBLEMA 1 ####################################################################

# Criar o modelo
m = Model(sense=maximize)

# Definir variáveis de decisão
lbr = m.add_var(name="lbr", var_type=CONTINUOUS)
lar = m.add_var(name="lar", var_type=CONTINUOUS)

# Função objetivo (exemplo de maximização de lucro)
m.objective = maximize(xsum([3000 * lbr, 5000 * lar]))  # Ajuste os coeficientes conforme o problema

# Restrições do problema
m += 0.5*lbr + 0.2*lar <= 16  # Restrição do volume de vendas
m += 0.25*lbr + 0.3*lar <= 11            # Restrição de produção máxima de A
m += 0.25*lbr + 0.5*lar <= 15  # Restrição de matéria-prima

# Resolver o modelo
status = m.optimize()

# Exibir resultados
if m.status == OptimizationStatus.OPTIMAL:
    print(f"Quantidade de Liga de baixa resistência: {lbr.x}")
    print(f"Quantidade de Liga de alta resistência: {lar.x}")
    print(f"Lucro máximo: {m.objective_value}")
else:
    print("Solução não encontrada")


########################################## PROBLEMA 2 #################################################################

# Criar o modelo
m = Model(sense=maximize)

# Variáveis de decisão para cada tipo de petróleo em cada gasolina
S = [m.add_var(name=f"S_{i}", var_type=CONTINUOUS) for i in range(4)]
A = [m.add_var(name=f"A_{i}", var_type=CONTINUOUS) for i in range(4)]
M = [m.add_var(name=f"M_{i}", var_type=CONTINUOUS) for i in range(4)]

# Função objetivo: maximizar lucro
m.objective = maximize(xsum(35 * S[i] + 28 * A[i] + 22 * M[i] for i in range(4)) - \
              (19 * S[0] + 24 * S[1] + 20 * S[2] + 27 * S[3] + \
               19 * A[0] + 24 * A[1] + 20 * A[2] + 27 * A[3] + \
               19 * M[0] + 24 * M[1] + 20 * M[2] + 27 * M[3]))

# Restrições de disponibilidade de petróleo
max_disp = [3500, 2200, 4200, 1800]
for i in range(4):
    m += S[i] + A[i] + M[i] <= max_disp[i]

# Restrições de composição para Superazul
m += S[0] <= 0.3 * xsum(S)   # Não mais que 30% do tipo de petróleo 1
m += S[1] >= 0.4 * xsum(S)    # Não menos que 40% do tipo de petróleo 2
m += S[2] <= 0.5 * xsum(S)    # Não mais que 50% do tipo de petróleo 3

# Restrições de composição para Azul
m += A[0] <= 0.3 * xsum(A)    # Não mais que 30% do tipo de petróleo 1
m += A[1] >= 0.1 * xsum(A)    # Não menos que 10% do tipo de petróleo 2

# Restrições de composição para Amarela
m += M[0] <= 0.7 * xsum(M)    # Não mais que 70% do tipo de petróleo 1

# Resolver o modelo
status = m.optimize()

# Exibir resultados
if m.status == OptimizationStatus.OPTIMAL:
    for i in range(4):
        print(f"Quantidade de petróleo {i+1} em Superazul: {S[i].x}")
        print(f"Quantidade de petróleo {i+1} em Azul: {A[i].x}")
        print(f"Quantidade de petróleo {i+1} em Amarela: {M[i].x}")
    print(f"Lucro máximo: {m.objective_value}")
else:
    print("Solução não encontrada")


################################ EXERCICIO 5 ######################################################

# Criar o modelo
m = Model(sense=maximize)

# Definir variáveis de decisão
x_a = m.add_var(name="x_a", var_type=CONTINUOUS)
x_b = m.add_var(name="x_b", var_type=CONTINUOUS)

# Função objetivo (exemplo de maximização de lucro)
m.objective = maximize(xsum([20 * x_a, 50 * x_b]))  # Ajuste os coeficientes conforme o problema

# Restrições do problema
m += x_a <= 100  # Restrição de produção máxima de A
m += x_a >= 4*x_b # Restrição da proporção mínima da A
m += 2*x_a + 4*x_b <= 240  # Restrição de matéria-prima

# Resolver o modelo
status = m.optimize()

# Exibir resultados
if m.status == OptimizationStatus.OPTIMAL:
    print(f"Quantidade de A: {x_a.x}")
    print(f"Quantidade de B: {x_b.x}")
    print(f"Lucro máximo: {m.objective_value}")
else:
    print("Solução não encontrada")

############################### EXERCICIO 6 #######################################################

# Criar o modelo
m = Model(sense=maximize)

# Definir variáveis de decisão
x_c = m.add_var(name="x_c", var_type=INTEGER)
x_b = m.add_var(name="x_b", var_type=INTEGER)

# Função objetivo (exemplo de maximização de lucro)
m.objective = maximize(xsum([40 * x_c, 35 * x_b]))  # Ajuste os coeficientes conforme o problema

# Restrições do problema
m += x_c/800 + x_b/600 <= 1  # Restrição da proporção de produção de chapas e barras
m += x_c <= 550 # Restrição da produção de chapas
m += x_b <= 580  # Restrição da produção de barras

# Resolver o modelo
status = m.optimize()

# Exibir resultados
if m.status == OptimizationStatus.OPTIMAL:
    sol_x_c = x_c.x
    sol_x_b = x_b.x
    print(f"Quantidade de Chapas: {x_c.x}")
    print(f"Quantidade de Barras: {x_b.x}")
    print(f"Lucro máximo: {m.objective_value}")
else:
    print("Solução não encontrada")

# Gráficos das restrições
x_vals = np.linspace(0, 600, 200)

# Restrição de capacidade conjunta: x_c / 800 + x_b / 600 <= 1
y1 = 600 * (1 - x_vals / 800)
y1 = np.clip(y1, 0, 600)  # Limitando o valor para a visualização

# Restrição de produção máxima de chapas
y2 = np.full_like(x_vals, 580)

# Restrição de produção máxima de barras
x3 = np.full_like(x_vals, 550)

# Plotar as restrições
plt.figure(figsize=(8, 6))
plt.plot(x_vals, y1, label=r"$\frac{x_c}{800} + \frac{x_b}{600} \leq 1$", color="blue")
plt.axhline(580, color="purple", linestyle="--", label=r"$x_b \leq 580$")
plt.axvline(550, color="green", linestyle="--", label=r"$x_c \leq 550$")

# Preencher a região viável
plt.fill_between(x_vals, 0, np.minimum(y1, y2), where=(x_vals <= 550), color="gray", alpha=0.3)

# Plotar a solução ótima
if m.status == OptimizationStatus.OPTIMAL:
    plt.plot(sol_x_c, sol_x_b, 'ro', label="Solução Ótima")
    plt.text(sol_x_c, sol_x_b, f"({sol_x_c:.1f}, {sol_x_b:.1f})", fontsize=12, ha="right")

# Configurações do gráfico
plt.xlabel("Produção de Chapas (x_c)")
plt.ylabel("Produção de Barras (x_b)")
plt.title("Região Viável e Solução Ótima")
plt.legend()
plt.xlim(0, 600)
plt.ylim(0, 600)
plt.grid(True)
plt.show()

############################### EXERCICIO 7 #######################################################

# Criar o modelo
m = Model(sense=maximize)

# Definir variáveis de decisão
x_a = m.add_var(name="x_a", var_type=INTEGER)
x_b = m.add_var(name="x_b", var_type=INTEGER)

# Função objetivo (exemplo de maximização de lucro)
m.objective = maximize(xsum([1.05 * x_a, 1.08 * x_b]))  # Ajuste os coeficientes conforme o problema

# Restrições do problema
m += x_a + x_b <= 5000  # Restrição do montante disponível
m += x_a >= 0.25*5000 # Restrição da proporção de x_a
m += x_b <= 0.5*5000  # Restrição da proporção de x_b
m += x_a >= x_b/2

# Resolver o modelo
status = m.optimize()

# Exibir resultados
if m.status == OptimizationStatus.OPTIMAL:
    print(f"Investimento em A: {x_a.x}")
    print(f"Investimento em A: {x_b.x}")
    print(f"Lucro máximo: {m.objective_value}")
else:
    print("Solução não encontrada")

############################### EXERCICIO 9 #######################################################

# Criar o modelo
m = Model(sense=maximize)

# Definir variáveis de decisão
x_a = m.add_var(name="x_a", var_type=INTEGER)
x_b = m.add_var(name="x_b", var_type=INTEGER)

# Função objetivo (exemplo de maximização de lucro)
m.objective = maximize(xsum([8 * x_a, 10 * x_b]))  # Ajuste os coeficientes conforme o problema

# Restrições do problema
m += 0.5 * x_a + 0.5 * x_b <= 150  # Restrição de matéria-prima
m += 0.6 * x_a + 0.4 * x_b <= 145 # Restrição de matéria-prima
m += x_a >= 30  # Restrição de demanda
m += x_a <= 150  # Restrição de demanda
m += x_b >= 40  # Restrição de demanda
m += x_b <= 200  # Restrição de demanda

# Resolver o modelo
status = m.optimize()

# Exibir resultados
if m.status == OptimizationStatus.OPTIMAL:
    print(f"Quantidde produto A: {x_a.x}")
    print(f"Quantidde produto B: {x_b.x}")
    print(f"Lucro máximo: {m.objective_value}")
else:
    print("Solução não encontrada")


############################### EXERCICIO 10 #######################################################

# Criar o modelo
m = Model(sense=maximize)

# Definir variáveis de decisão
x_g = m.add_var(name="grano", var_type=INTEGER)
x_w = m.add_var(name="weathie", var_type=INTEGER)

# Função objetivo (exemplo de maximização de lucro)
m.objective = maximize(xsum([1 * x_g, 1.35 * x_w]))  # Ajuste os coeficientes conforme o problema

# Restrições do problema
m += 0.2 * x_g + 0.4 * x_w <= 60  # Restrição de espaço
m += x_g <= 200  # Restrição de demanda
m += x_w <= 120  # Restrição de demanda

# Resolver o modelo
status = m.optimize()

# Exibir resultados
if m.status == OptimizationStatus.OPTIMAL:
    sol_x_g = x_g.x
    sol_x_w = x_w.x
    print(f"Quantidde de Grano: {x_g.x}")
    print(f"Quantidde de Weathie: {x_w.x}")
    print(f"Lucro máximo: {m.objective_value}")
else:
    print("Solução não encontrada")

# Gráficos das restrições
x_vals = np.linspace(0, 220, 200)

# Restrição de espaço: 0.2 * x_g + 0.4 * x_w <= 60, rearranjada para y = f(x)
y1 = (60 - 0.2 * x_vals) / 0.4
y1 = np.clip(y1, 0, 120)  # Limitar o valor para a demanda máxima de Wheatie

# Limite máximo de demanda para Wheatie (linha horizontal)
y2 = np.full_like(x_vals, 120)

# Limite máximo de demanda para Grano (linha vertical)
x3 = np.full_like(x_vals, 200)

# Plotar as restrições
plt.figure(figsize=(8, 6))
plt.plot(x_vals, y1, label=r"$0.2 \times x_g + 0.4 \times x_w \leq 60$", color="blue")
plt.axhline(120, color="purple", linestyle="--", label=r"$x_w \leq 120$")
plt.axvline(200, color="green", linestyle="--", label=r"$x_g \leq 200$")

# Preencher a região viável
plt.fill_between(x_vals, 0, np.minimum(y1, y2), where=(x_vals <= 200), color="gray", alpha=0.3)

# Plotar a solução ótima
if m.status == OptimizationStatus.OPTIMAL:
    plt.plot(sol_x_g, sol_x_w, 'ro', label="Solução Ótima")
    plt.text(sol_x_g, sol_x_w, f"({sol_x_g:.1f}, {sol_x_w:.1f})", fontsize=12, ha="right")

# Configurações do gráfico
plt.xlabel("Quantidade de Grano (x_g)")
plt.ylabel("Quantidade de Wheatie (x_w)")
plt.title("Região Viável e Solução Ótima")
plt.legend()
plt.xlim(0, 220)
plt.ylim(0, 130)
plt.grid(True)
plt.show()

############################### EXERCICIO 11 #######################################################

# Criar o modelo
m = Model(sense=maximize)

# Definir variáveis de decisão
t_e = m.add_var(name="estudo", var_type=INTEGER)
t_d = m.add_var(name="diversao", var_type=INTEGER)

# Função objetivo (exemplo de maximização de lucro)
m.objective = maximize(xsum([1 * t_e, 2 * t_d]))  # Ajuste os coeficientes conforme o problema

# Restrições do problema
m += t_d + t_e <= 10  # Restrição de tempo
m += t_d <= t_e  # Restrição de proporção estudo e diversão
m += t_d <= 4  # Restrição de tempo

# Resolver o modelo
status = m.optimize()

# Exibir resultados
if m.status == OptimizationStatus.OPTIMAL:
    sol_t_d = t_d.x
    sol_t_e = t_e.x
    print(f"Quantidde de diversão: {t_d.x}")
    print(f"Quantidde de estudo: {t_e.x}")
    print(f"Lucro máximo: {m.objective_value}")
else:
    print("Solução não encontrada")

# Gráficos das restrições
x_vals = np.linspace(0, 10, 100)

# Restrição de tempo total: t_d + t_e <= 10, rearranjada para t_d em função de t_e
y1 = 10 - x_vals

# Restrição de estudo >= diversão: t_d <= t_e
y2 = x_vals

# Restrição de diversão máxima: t_d <= 4
y3 = np.full_like(x_vals, 4)

# Plotar as restrições
plt.figure(figsize=(8, 6))
plt.plot(x_vals, y1, label=r"$t_d + t_e \leq 10$", color="blue")
plt.plot(x_vals, y2, label=r"$t_d \leq t_e$", linestyle="--", color="green")
plt.axhline(4, color="purple", linestyle="--", label=r"$t_d \leq 4$")

# Preencher a região viável
plt.fill_between(x_vals, 0, np.minimum(y1, np.minimum(y2, y3)), color="gray", alpha=0.3)

# Plotar a solução ótima
if m.status == OptimizationStatus.OPTIMAL:
    plt.plot(sol_t_e, sol_t_d, 'ro', label="Solução Ótima")
    plt.text(sol_t_e, sol_t_d, f"({sol_t_e:.1f}, {sol_t_d:.1f})", fontsize=12, ha="right")

# Configurações do gráfico
plt.xlabel("Horas de Estudo (t_e)")
plt.ylabel("Horas de Diversão (t_d)")
plt.title("Região Viável e Solução Ótima")
plt.legend()
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.grid(True)
plt.show()

############################### EXERCICIO 12 #######################################################

# Criar o modelo
m = Model(sense=maximize)

# Definir variáveis de decisão para os tipos de chapéu
x_1 = m.add_var(name="chapeu1", var_type=INTEGER)
x_2 = m.add_var(name="chapeu2", var_type=INTEGER)

# Função objetivo: maximizar lucro
m.objective = maximize(8 * x_1 + 5 * x_2)

# Restrições do problema
m += x_1 + x_2 / 2 <= 200  # Restrição de mão-de-obra reformulada
m += x_1 <= 150            # Restrição de demanda para chapéu tipo 1
m += x_2 <= 200            # Restrição de demanda para chapéu tipo 2

# Resolver o modelo
status = m.optimize()

# Obter a solução ótima, se existir
if m.status == OptimizationStatus.OPTIMAL:
    sol_x_1 = x_1.x
    sol_x_2 = x_2.x
    print(f"Quantidade de chapéu tipo 1: {sol_x_1}")
    print(f"Quantidade de chapéu tipo 2: {sol_x_2}")
    print(f"Lucro máximo: {m.objective_value}")
else:
    print("Solução não encontrada")

# Gráficos das restrições
x_vals = np.linspace(0, 200, 200)

# Restrição de mão-de-obra reformulada: x_1 + x_2 / 2 <= 200, rearranjada para x_2 em função de x_1
y1 = 2 * (200 - x_vals)

# Limite máximo de demanda para chapéu tipo 2 (linha horizontal)
y2 = np.full_like(x_vals, 200)

# Limite máximo de demanda para chapéu tipo 1 (linha vertical)
x3 = np.full_like(x_vals, 150)

# Plotar as restrições
plt.figure(figsize=(8, 6))
plt.plot(x_vals, y1, label=r"$x_1 + \frac{x_2}{2} \leq 200$", color="blue")
plt.axhline(200, color="purple", linestyle="--", label=r"$x_2 \leq 200$")
plt.axvline(150, color="green", linestyle="--", label=r"$x_1 \leq 150$")

# Preencher a região viável
plt.fill_between(x_vals, 0, np.minimum(y1, y2), where=(x_vals <= 150), color="gray", alpha=0.3)

# Plotar a solução ótima
if m.status == OptimizationStatus.OPTIMAL:
    plt.plot(sol_x_1, sol_x_2, 'ro', label="Solução Ótima")
    plt.text(sol_x_1, sol_x_2, f"({sol_x_1:.1f}, {sol_x_2:.1f})", fontsize=12, ha="right")

# Configurações do gráfico
plt.xlabel("Quantidade de chapéu tipo 1 (x_1)")
plt.ylabel("Quantidade de chapéu tipo 2 (x_2)")
plt.title("Região Viável e Solução Ótima")
plt.legend()
plt.xlim(0, 200)
plt.ylim(0, 220)
plt.grid(True)
plt.show()
