import matplotlib.pyplot as plt
import numpy as np
import os

versions = ['v0', 'v1', 'v2', 'v3']
types = ['LUT', 'MUX', 'Registers', 'Power']
resources = [
    [7650, 8010, 9134, 9548], # LUTS
    [530, 558, 748, 722], # MUX
    [2111, 2109, 2132, 2132], # Registers
    [31, 37, 49, 47] # Power
]

# 4 in 1
def plot_acceleration_factors(models, resources):
  num_models = len(models)
  fig, axes = plt.subplots(2, 2, figsize=(10, 8))  # Create a 2x2 grid of subplots
  axes = axes.flatten()  # Flatten the axes array for easier iteration

  
  for i, model in enumerate(models):

    ax = axes[i]
    acceleration_factors = [count / resources[i][0] for count in resources[i]]  # Normalize to v0

    ax.plot(versions, acceleration_factors, marker='o', linestyle='--')  # Plot acceleration factors

    # Format y-axis ticks as multiples of 'x'
    ax.set_yticklabels(['{:.3f}x'.format(tick) for tick in ax.get_yticks()])

   # ax.set_ylabel("Acceleration Factor (v0 = 1x)")
   # ax.set_title(f"Acceleration Factors for {model}")

    # Box the plot
    for spine in ['top', 'bottom', 'left', 'right']:
        ax.spines[spine].set_linewidth(1)

  plt.tight_layout()  # Adjust subplot params for a tight layout
  #plt.show()
  plt.savefig(f'{model}_count.eps', format='eps')

# seperate
saved_plt_path = "./fpga_resources_factor"
if not os.path.exists(saved_plt_path):
    os.makedirs(saved_plt_path)

for i in range(len(types)):
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    acceleration_factors = [count / resources[i][0] for count in resources[i]]  # Normalize to v0
    ax.plot(range(len(versions)), acceleration_factors, linestyle='--', marker='o')
    ax.set_xticks(range(len(versions)))
    ax.set_xticklabels(versions, fontsize=18)
    ax.set_yticklabels(['{:.3f}x'.format(tick) for tick in ax.get_yticks()], fontsize=18)
    for spine in ['top', 'bottom', 'left', 'right']:
        ax.spines[spine].set_linewidth(1)
    plt.tight_layout()  # Adjust subplot params for a tight layout
    # plt.show()
    plt.savefig(saved_plt_path + "/" + types[i] + ".svg")

# plot_acceleration_factors(types, resources)