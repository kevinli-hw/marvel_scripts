import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.ticker as mticker

plt.style.use('default')

saved_plt_path = "./instruction_pattern_cnt"
if not os.path.exists(saved_plt_path):
    os.makedirs(saved_plt_path)



# Data for the plots
# models = ['BERT-Tiny', 'MobileBERT', 'MiniLM', 'Electra', 'Deberta']
models = ['B-Ty', 'N-Bt', 'M-Lm', 'E-Lt', 'D-Bt']

sll2i_pattern = {
    'slli_count': [8523310, 227937595, 190425764, 122267695, 720050349],
    'sll2i_count': [6292056, 121639492, 176160884, 75497580, 717236440]
}
add2i_pattern = {
    'addi_count': [343603612, 16819689335, 18399327703, 7970572611, 19182902366],
    'add2i_count': [214122104, 10791243204, 12573276888, 5051200728, 13093089240]
}
add2_pattern = {
    'add_count': [142406190, 5721739063, 825059112, 2925284855, 3825751837],
    'add2_count': [33590514, 515961544, 743991190, 403084644, 3625377104]
}
or2i_pattern = {
    'ori_count': [30531605, 388300819, 415236118, 353214485, 2302672914],
    'or2i_count': [20971520, 251658240, 377487360, 251658240, 2189426688]
}

add3i_pattern = {
    'addi_count': [343603612, 16819689335, 18399327703, 7970572611, 19182902366],
    'add3i_count': [285021696, 14574570496, 17080502272, 6826644736, 17054451712]
}

total_instrcutions = [1293943706, 57540234319, 56218215129, 32886763314, 79987267520]

# Function to create a bar plot
def create_bar_plot(data, title, y_label=True, formatter_label=False, formatter_num=0):
    x = np.arange(len(models))
    width = 0.2

    fig, ax = plt.subplots(figsize=(18, 15))

    # Create bars for each category
    for i, (category, values) in enumerate(data.items()):
        for j in range(len(values)):
            values[j] = values[j]/total_instrcutions[j]
        ax.bar(x + i * width, values, width, label=category)

    
    # ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    # ax.yaxis.get_offset_text().set_size(12) 
    # ax.set_ylabel('Normalized instruction execution count')
    if y_label:
        ax.set_ylabel('Instruction count (Norm)', fontsize=80)
    if title == 'add2i pattern':
        ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    elif title == 'sll2i pattern':
        ax.set_yticks([0.000+i*0.003 for i in range(0, 6)])
    elif title == 'add2 pattern':
        ax.set_yticks([0.00+i*0.03 for i in range(0, 6)])
    elif title == 'or2i pattern':
        # ax.set_yticks([0.000+i*0.005 for i in range(0, 6)])
        ax.set_yticks([0.00+i*0.01 for i in range(0, 6)])
    elif title == 'add3i pattern':
        ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax.set_title(title, fontsize=100, pad=20)
    ax.set_xticks(x + width * (len(data) - 1) / 2)
    ax.set_xticklabels(models)
    ax.tick_params(axis='x', labelsize=80, pad=15)
    ax.tick_params(axis='y', labelsize=80, pad=20)
    ax.legend(loc='upper right', fontsize=60)
    # if title == 'sll2i pattern' or title == 'add2 pattern':
    #     ax.legend(loc='upper right', fontsize=35)
    # else:
    #     ax.legend(loc='upper left', fontsize=35)

    if formatter_label:
        formatter = mticker.ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-formatter_num, -formatter_num))   # 固定为 10^-3
        ax.yaxis.set_major_formatter(formatter)
        off = ax.yaxis.get_offset_text()
        off.set_fontsize(60)  
        off.set_y(1.5) 

    plt.tight_layout()
    plt.savefig(saved_plt_path + "/" + title + ".svg", dpi=300, bbox_inches='tight') 
    plt.show()
   

# Create the plots
create_bar_plot(sll2i_pattern, 'sll2i pattern', y_label=True, formatter_label=True, formatter_num=3)
create_bar_plot(add2i_pattern, 'add2i pattern', y_label=False, formatter_label=True, formatter_num=1)
create_bar_plot(add2_pattern, 'add2 pattern', y_label=False, formatter_label=True, formatter_num=2)
create_bar_plot(or2i_pattern, 'or2i pattern', y_label=False, formatter_label=True, formatter_num=2)
create_bar_plot(add3i_pattern, 'add3i pattern', y_label=False, formatter_label=True, formatter_num=1)