# SOLUÇÃO DOS EXERCÍCIOS DA LISTA 1 DE PESQUISA OPERACIONAL - UFF - 2024.2

from mip import Model, xsum, maximize, CONTINUOUS, INTEGER, OptimizationStatus
import matplotlib.pyplot as plt
import numpy as np

################################ EXERCICIO 15 ######################################################

# Criar o modelo
m = Model(sense=maximize)

# Definir variáveis de decisão para o número de comerciais de rádio (x_r) e TV (x_t)
x_r = m.add_var(name="radio", var_type=INTEGER)
x_t = m.add_var(name="tv", var_type=INTEGER)

# Função objetivo: maximizar o alcance total
m.objective = maximize(3000 * x_r + 3000 * x_t + 2000)

# Restrições do problema
m += 300 * x_r + 2000 * x_t <= 20000          # Restrição orçamentária
m += 300 * x_r <= 0.8 * 20000                 # Limite máximo de orçamento para rádio
m += 2000 * x_t <= 0.8 * 20000                # Limite máximo de orçamento para TV
m += x_r >= 1                                 # Pelo menos um comercial de rádio
m += x_t >= 1                                 # Pelo menos um anúncio de TV

# Resolver o modelo
status = m.optimize()

# Obter a solução ótima, se existir
if m.status == OptimizationStatus.OPTIMAL:
    sol_x_r = x_r.x
    sol_x_t = x_t.x
    print(f"Quantidade de comerciais de rádio: {sol_x_r}")
    print(f"Quantidade de comerciais de TV: {sol_x_t}")
    print(f"Alcance máximo: {m.objective_value}")
else:
    print("Solução não encontrada")

# Gráficos das restrições
x_vals = np.linspace(0, 70, 200)

# Restrição orçamentária total: 300 * x_r + 2000 * x_t <= 20000, rearranjada para x_t em função de x_r
y1 = (20000 - 300 * x_vals) / 2000
y1 = np.clip(y1, 0, None)  # Limitar para valores não negativos

# Restrição de orçamento para rádio (máximo de 80% do orçamento total): x_r <= 0.8 * 20000 / 300
x_max_radio = 0.8 * 20000 / 300
y2 = np.full_like(x_vals, x_max_radio)

# Restrição de orçamento para TV (máximo de 80% do orçamento total): x_t <= 0.8 * 20000 / 2000
y3 = np.full_like(x_vals, 0.8 * 20000 / 2000)

# Plotar as restrições
plt.figure(figsize=(8, 6))
plt.plot(x_vals, y1, label=r"$300 \cdot x_r + 2000 \cdot x_t \leq 20000$", color="blue")
plt.axhline(0.8 * 20000 / 2000, color="purple", linestyle="--", label=r"$x_t \leq \frac{0.8 \cdot 20000}{2000}$")
plt.axvline(x_max_radio, color="green", linestyle="--", label=r"$x_r \leq \frac{0.8 \cdot 20000}{300}$")

# Preencher a região viável
plt.fill_between(x_vals, 0, np.minimum(y1, y3), where=(x_vals <= x_max_radio), color="gray", alpha=0.3)

# Plotar a solução ótima
if m.status == OptimizationStatus.OPTIMAL:
    plt.plot(sol_x_r, sol_x_t, 'ro', label="Solução Ótima")
    plt.text(sol_x_r, sol_x_t, f"({sol_x_r:.1f}, {sol_x_t:.1f})", fontsize=12, ha="right")

# Configurações do gráfico
plt.xlabel("Quantidade de Comerciais de Rádio (x_r)")
plt.ylabel("Quantidade de Comerciais de TV (x_t)")
plt.title("Região Viável e Solução Ótima para a Campanha Publicitária")
plt.legend()
plt.xlim(0, 70)
plt.ylim(0, 12)
plt.grid(True)
plt.show()

################################ EXERCICIO 16 ######################################################

# Criar o modelo
m1 = Model(sense=maximize)

# Variáveis de decisão
x = m1.add_var(name="camisas", var_type=INTEGER)
y = m1.add_var(name="blusas", var_type=INTEGER)

# Função objetivo: maximizar o lucro
m1.objective = maximize(8 * x + 12 * y)

# Restrições de tempo para cada etapa do processo
m1 += 20 * x + 60 * y <= 60000   # Restrição de corte
m1 += 70 * x + 60 * y <= 84000   # Restrição de costura
m1 += 12 * x + 4 * y <= 12000    # Restrição de embalagem

# Resolver o modelo
m1.optimize()

# Resultados
if m1.status == OptimizationStatus.OPTIMAL:
    sol_x = x.x
    sol_y = y.x
    print(f"Quantidade de camisas: {sol_x}")
    print(f"Quantidade de blusas: {sol_y}")
    print(f"Lucro máximo: {m1.objective_value}")
else:
    print("Solução não encontrada")

# Plotando as restrições e a região viável
x_vals = np.linspace(0, 3000, 200)

# Restrição de corte: 20x + 60y <= 60000
y1 = (60000 - 20 * x_vals) / 60

# Restrição de costura: 70x + 60y <= 84000
y2 = (84000 - 70 * x_vals) / 60

# Restrição de embalagem: 12x + 4y <= 12000
y3 = (12000 - 12 * x_vals) / 4

# Plot
plt.figure(figsize=(8, 6))
plt.plot(x_vals, y1, label=r"$20x + 60y \leq 60000$", color="blue")
plt.plot(x_vals, y2, label=r"$70x + 60y \leq 84000$", color="green")
plt.plot(x_vals, y3, label=r"$12x + 4y \leq 12000$", color="purple")

# Região viável preenchida
plt.fill_between(x_vals, 0, np.minimum(np.minimum(y1, y2), y3), where=(x_vals >= 0), color="gray", alpha=0.3)

# Solução ótima
if m1.status == OptimizationStatus.OPTIMAL:
    plt.plot(sol_x, sol_y, 'ro', label="Solução Ótima")
    plt.text(sol_x, sol_y, f"({sol_x:.0f}, {sol_y:.0f})", fontsize=12, ha="right")

# Configurações do gráfico
plt.xlabel("Quantidade de Camisas")
plt.ylabel("Quantidade de Blusas")
plt.title("Região Viável e Solução Ótima para Camisas e Blusas")
plt.legend()
plt.xlim(0, 3000)
plt.ylim(0, 1500)
plt.grid(True)
plt.show()

################################ EXERCICIO 17 ######################################################

# Criar o modelo
m2 = Model(sense=maximize)

# Variáveis de decisão
x_m = m2.add_var(name="mesas", var_type=INTEGER)
x_c = m2.add_var(name="cadeiras", var_type=INTEGER)

# Função objetivo: maximizar o lucro
m2.objective = maximize(50 * x_c + 100 * x_m)

# Restrições de tempo para cada etapa do processo
m2 += x_c <= 120                # Restrição de montagem para cadeiras
m2 += x_m <= 60                 # Restrição de montagem para mesas
m2 += x_c / 150 + x_m / 110 <= 1  # Restrição de pintura

# Resolver o modelo
m2.optimize()

# Resultados
if m2.status == OptimizationStatus.OPTIMAL:
    sol_x_m = x_m.x
    sol_x_c = x_c.x
    print(f"Quantidade de cadeiras: {sol_x_c}")
    print(f"Quantidade de mesas: {sol_x_m}")
    print(f"Lucro máximo: {m2.objective_value}")
else:
    print("Solução não encontrada")

# Plotando as restrições e a região viável
x_vals = np.linspace(0, 150, 200)

# Restrição de montagem para cadeiras: x_c <= 120
y1 = np.full_like(x_vals, 120)

# Restrição de montagem para mesas: x_m <= 60
x_max_mesas = np.full_like(x_vals, 60)

# Restrição de pintura: x_c / 150 + x_m / 110 <= 1, rearranjada para y = f(x)
y3 = 150 * (1 - x_vals / 110)

# Plot
plt.figure(figsize=(8, 6))
plt.plot(x_vals, y1, label=r"$x_c \leq 120$", color="blue")
plt.axvline(60, color="green", linestyle="--", label=r"$x_m \leq 60$")
plt.plot(x_vals, y3, label=r"$\frac{x_c}{150} + \frac{x_m}{110} \leq 1$", color="purple")

# Região viável preenchida
plt.fill_between(x_vals, 0, np.minimum(y1, y3), where=(x_vals <= 60), color="gray", alpha=0.3)

# Solução ótima
if m2.status == OptimizationStatus.OPTIMAL:
    plt.plot(sol_x_m, sol_x_c, 'ro', label="Solução Ótima")
    plt.text(sol_x_m, sol_x_c, f"({sol_x_m:.0f}, {sol_x_c:.0f})", fontsize=12, ha="right")

# Configurações do gráfico
plt.xlabel("Quantidade de Mesas")
plt.ylabel("Quantidade de Cadeiras")
plt.title("Região Viável e Solução Ótima para Mesas e Cadeiras")
plt.legend()
plt.xlim(0, 150)
plt.ylim(0, 150)
plt.grid(True)
plt.show()
