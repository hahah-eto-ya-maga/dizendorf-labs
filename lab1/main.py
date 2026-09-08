import random
import math
from datetime import datetime
import matplotlib.pyplot as plt

n = 11
p = 0.07
simulations = 100

generated_values = []

for _ in range(simulations):
    successes = 0
    for _ in range(n):
        if random.random() <= p:
            successes += 1
    generated_values.append(successes)

current_time = datetime.now().strftime("%H-%M-%S")
filename = f"lab1_{current_time}.txt"

with open(filename, "w") as file:
    file.write(" ".join(map(str, generated_values)))

print(f"Данные успешно записаны в файл: {filename}")

sorted_values = sorted(generated_values)
print("\nВариационный ряд:")
print(sorted_values)

x_values = list(range(n + 1))
frequencies = []

for val in x_values:
    count = generated_values.count(val)
    rel_freq = count / simulations
    frequencies.append(rel_freq)

plt.figure(figsize=(8, 6))

max_visible_val = max(generated_values) + 1

x_edges = list(range(max_visible_val + 1))
y_heights = frequencies[:max_visible_val] + [0]

plt.step(x_edges, y_heights, where='post', color='black', linewidth=1.5)

plt.bar(list(range(max_visible_val)), frequencies[:max_visible_val], 
        align='edge', width=1.0, color='#3498db', edgecolor='black', alpha=0.7)

plt.title('Гистограмма относительных частот (Вариант 2)', fontsize=12, fontweight='bold')
plt.xlabel('значения', fontsize=12, loc='right')
plt.ylabel('относительные\nчастоты', fontsize=12, rotation=0, loc='top', labelpad=15)

plt.xticks(list(range(max_visible_val)))
plt.xlim(-0.5, max_visible_val + 0.5)
plt.ylim(0, max(frequencies) + 0.05)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('data', -0.1)) 
ax.spines['bottom'].set_position(('data', 0))

unique_freqs = sorted(list(set(frequencies[:max_visible_val])))
plt.yticks(unique_freqs, [f'{f:.2f}' for f in unique_freqs])

plt.savefig(f"histogram_notebook_{current_time}.png", dpi=300)
print(f"\nГрафик по конспекту успешно сохранен как 'histogram_notebook_{current_time}.png'!")

plt.show()