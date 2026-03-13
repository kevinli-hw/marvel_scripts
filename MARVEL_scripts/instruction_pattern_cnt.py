import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.ticker as mticker

plt.style.use('default')

saved_plt_path = "./instruction_pattern_cnt"
if not os.path.exists(saved_plt_path):
    os.makedirs(saved_plt_path)



# Data for the plots
models = ['BERT-Tiny', 'MobileBERT', 'MiniLM', 'SqueezeBERT']
sll2i_pattern = {
    'slli_count': [8523310, 227937595, 190425764, 229321903],
    'slli_slli_count': [6292056, 121639492, 176160884, 226492516]
}
add2i_pattern = {
    'addi_count': [343603612, 16819689335, 18399327703, 21277146073],
    'addi_addi_count': [214122104, 10791243204, 12573276888, 13954152984]
}
add2_pattern = {
    'add_count': [142406190, 5721739063, 825059112, 1513836848],
    'add_add_count': [33590514, 515961544, 743991190, 1217547220]
}
or2i_pattern = {
    'ori_count': [30531605, 388300819, 415236118, 981467156],
    'ori_ori_count': [20971520, 251658240, 377487360, 754974720]
}

total_instrcutions = [1293943706, 57540234319, 56218215129, 62960343399]

# Function to create a bar plot
def create_bar_plot(data, title, y_label=True, formatter_label=False, formatter_num=0):
    x = np.arange(len(models))
    width = 0.2

    fig, ax = plt.subplots(figsize=(20, 15))

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
        ax.set_yticks([0.000+i*0.001 for i in range(0, 8)])
    elif title == 'add2 pattern':
        ax.set_yticks([0.00+i*0.02 for i in range(0, 7)])
    elif title == 'or2i pattern':
        ax.set_yticks([0.000+i*0.005 for i in range(0, 6)])
    ax.set_title(title, fontsize=80, pad=20)
    ax.set_xticks(x + width * (len(data) - 1) / 2)
    ax.set_xticklabels(models)
    ax.tick_params(axis='x', labelsize=57, pad=15)
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

    plt.tight_layout()
    plt.savefig(saved_plt_path + "/" + title + ".svg", dpi=300, bbox_inches='tight') 
    plt.show()
   

# Create the plots
create_bar_plot(sll2i_pattern, 'sll2i pattern', y_label=True, formatter_label=True, formatter_num=3)
create_bar_plot(add2i_pattern, 'add2i pattern', y_label=False, formatter_label=True, formatter_num=1)
create_bar_plot(add2_pattern, 'add2 pattern', y_label=False, formatter_label=True, formatter_num=2)
create_bar_plot(or2i_pattern, 'or2i pattern', y_label=False, formatter_label=True, formatter_num=3)