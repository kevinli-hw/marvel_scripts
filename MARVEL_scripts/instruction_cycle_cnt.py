import matplotlib.pyplot as plt
import numpy as np
import os

bar_chart=False
line_chart=True
two_sub_plts=False

plt.style.use('default')
plt.rcParams.update({
    'font.size':18
})

# saved_plt_path = "./instruction_cycle_cnt"
# if not os.path.exists(saved_plt_path):
#     os.makedirs(saved_plt_path)


# Sample data (replace with your actual data)
models = ['BERT-Tiny', 'MobileBERT', 'MiniLM', 'SqueezeBERT']
processor_versions = ['v0', 'v1', 'v2', 'v3', 'v3_U']


cycle_counts = [
    [1494618035, 1491462659, 1478873705, 1375214550, 699923908],    # Cycle counts for BERT-Tiny
    [67165571446, 67102285770, 66926591726, 61611241273, 47501030949],  # Cycle counts for MobileBERT
    [66433772829, 66339400797, 66075202731, 60509376602, 31551710622],  # Cycle counts for MiniLM
    [77226916025, 77113669633, 76660729688, 69802678367, 34598941341] # Cycle counts for SqueezeBERT
]

instruction_counts = [
    [1293943706, 1290788315, 1278199361, 1174540205, 686911631], #Instructions for BERT-Tiny
    [57540234319, 57476948627, 57301254583, 51985904129, 41909814429], # Instructions for MobileBERT
    [56218215129, 56123843083, 55859645017, 50293818887, 31153224831],  # Instructions for MiniLM
    [62960343399, 62847096993, 62394157048, 55536105726, 34277757952]  # Instructions for SqueezeBERT
]

if bar_chart:

    for i in range(len(cycle_counts)):
        cycle_counts[i] = [value/1e9 for value in cycle_counts[i]]

    for i in range(len(instruction_counts)):
        instruction_counts[i] = [value/1e9 for value in instruction_counts[i]]

    # Set the width of the bars
    width = 0.35

    # Set the positions of the bars on the x-axis
    x = np.arange(len(processor_versions))

    # Create subplots for each model
    fig, axes = plt.subplots(2, 2, figsize=(40, 30), sharex=True)  # 2x2 grid
    axes = axes.flatten()

    # Iterate through each model and create a subplot
    for i, model in enumerate(models):
        ax = axes[i]

        # Plot the bars for the current model
        rects1 = ax.bar(x - width/2, cycle_counts[i], width, label='Cycle Count')
        rects2 = ax.bar(x + width/2, instruction_counts[i], width, label='Instruction Execution Count')
        # Add labels and title for the subplot
        ax.set_xticks(x)
        labels = ax.set_xticklabels(processor_versions, fontsize=40)
        
        for lab in labels:
            if lab.get_text() == 'v3+unroll':
                lab.set_color('blue')
                lab.set_fontstyle('italic')
                lab.set_weight('bold')
                break 
        ax.tick_params(axis='y', labelsize=40)
        ax.legend(fontsize=30, loc='upper right')
        if(model == 'BERT-Tiny' or model == 'MobileBERT'):
            ax.text(0.5, -0.04, f"{model}", ha='center', fontsize=40, transform=ax.transAxes)
        else:
            ax.text(0.5, -0.10, f"{model}", ha='center', fontsize=40, transform=ax.transAxes)


    # Add a common x-axis label
    fig.text(0.5, -0.02, 'Processor Version', ha='center', fontsize=40)
    fig.text(-0.02, 0.5, 'Count (Billions)', va='center', rotation='vertical', fontsize=40)

    plt.tight_layout()
    plt.savefig('cycle_and_instruction_count.svg', format='svg', bbox_inches='tight')
    plt.show()

if line_chart:
    # acceleration line graph
    cycle_acc = []
    instr_acc = []
    for i in range(len(models)):
        base_c = cycle_counts[i][0]
        base_i = instruction_counts[i][0]
        cycle_acc.append([base_c / v for v in cycle_counts[i]])
        instr_acc.append([base_i / v for v in instruction_counts[i]])
    
    print("cycle_acc: ", cycle_acc)
    print("instr_acc: ", instr_acc)

    x = np.arange(len(processor_versions))

    # fig, axes = plt.subplots(2, 2, figsize=(35, 35), sharex=True)
    fig, axes = plt.subplots(2, 2, figsize=(35, 35))
    axes = axes.flatten()

    for i, model in enumerate(models):
        ax = axes[i]

        # 折线：Cycle / Instruction 的加速比
        ax.plot(x, cycle_acc[i], marker='o', markersize=12, linewidth=3, label='Cycle Acc.')
        ax.plot(x, instr_acc[i], marker='s', markersize=12, linewidth=3, label='Instruction Acc.')

        # x 轴刻度与高亮 v3+unroll
        ax.set_xticks(x)
        labels = ax.set_xticklabels(processor_versions, fontsize=60)
        for lab in labels:
            if lab.get_text() == 'v3_U':
                lab.set_color('blue'); lab.set_fontstyle('italic'); lab.set_weight('bold'); break

        # y 轴从 1 起（v0 基线）
        ymax = max(max(cycle_acc[i]), max(instr_acc[i]))
        # ax.set_ylim(0.8, 2.4)
        ax.set_yticks([0.8+i*0.2 for i in range(0, 9)])
        ax.axhline(1, linestyle='--', linewidth=1.5)  # baseline 参考线

        ax.tick_params(axis='x', labelsize=80)
        ax.tick_params(axis='y', labelsize=80)
        ax.legend(loc='upper left', fontsize=70)

        # 子图下方写模型名（与你原来一致）
        if model in ('BERT-Tiny', 'MobileBERT'):
            ax.text(0.5, -0.15, model, ha='center', fontsize=80, transform=ax.transAxes)
        else:
            ax.text(0.5, -0.14, model, ha='center', fontsize=80, transform=ax.transAxes)

    # 全局轴标签
    fig.text(0.5, -0.03, 'Processor Version', ha='center', fontsize=80)
    fig.text(-0.05, 0.5, 'Acceleration', va='center', rotation='vertical', fontsize=80)
    fig.tight_layout(h_pad=1.0)

    plt.tight_layout()
    plt.savefig('cycle_and_instruction_acceleration.svg', format='svg', bbox_inches='tight')
    plt.show()

if two_sub_plts:
    # --- 颜色与 marker（每个模型固定一套风格）---
    colors  = {'BERT-Tiny':'C0', 'MobileBERT':'C1', 'MiniLM':'C2', 'SqueezeBERT':'C3'}
    markers = {'BERT-Tiny':'o',  'MobileBERT':'s',  'MiniLM':'^',  'SqueezeBERT':'D'}
    x = np.arange(len(processor_versions))

    # acceleration line graph
    cycle_acc = []
    instr_acc = []
    for i in range(len(models)):
        base_c = cycle_counts[i][0]
        base_i = instruction_counts[i][0]
        cycle_acc.append([base_c / v for v in cycle_counts[i]])
        instr_acc.append([base_i / v for v in instruction_counts[i]])

    def style_xticks(ax):
        ax.set_xticks(x)
        labels = ax.set_xticklabels(processor_versions, fontsize=16)
        for lab in labels:
            if lab.get_text() == 'v3+unroll':
                lab.set_color('blue'); lab.set_fontstyle('italic'); lab.set_weight('bold')
                break

    def finish(ax, title):
        # y 从 1 起；添加基线
        ymax = max(line.get_ydata().max() for line in ax.lines) if ax.lines else 1.1
        ax.set_ylim(0.8, 2.4)
        ax.axhline(1.0, linestyle='--', linewidth=1.2)
        ax.set_ylabel('Acceleration')
        style_xticks(ax)
        ax.grid(axis='y', linestyle=':', linewidth=1, alpha=0.6)
        ax.set_title(title)
        # 图例上方居中、两行
        ax.legend(ncol=4, loc='upper right',
                frameon=True, fontsize=16, columnspacing=1.0, handlelength=2.0)

    # -------- 图 1：Instruction Acceleration --------
    fig1, ax1 = plt.subplots(figsize=(14, 8))
    for i, model in enumerate(models):
        ax1.plot(x, instr_acc[i],
                marker=markers[model], color=colors[model],
                linewidth=2, markersize=10, markeredgewidth=1.2,
                label=model)
    fig1.tight_layout(rect=[0, 0, 1, 0.92])
    fig1.savefig('instruction_acceleration_by_model.svg', format='svg', bbox_inches='tight')

    # -------- 图 2：Cycle Acceleration --------
    fig2, ax2 = plt.subplots(figsize=(14, 8))
    for i, model in enumerate(models):
        ax2.plot(x, cycle_acc[i],
                marker=markers[model], color=colors[model],
                linewidth=2, markersize=10, markeredgewidth=1.2,
                label=model)
    fig2.tight_layout(rect=[0, 0, 1, 0.92])
    fig2.savefig('cycle_acceleration_by_model.svg', format='svg', bbox_inches='tight')

    plt.show()