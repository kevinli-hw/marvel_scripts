import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data
data_cycle_count = {
    "Model": ["BERT-Tiny", "MobileBERT", "MiniLM", "SqueezeBERT"],
    "trv32p3f_U": [351624807, 25314556100, 15787453938, 17313588594],
    "trv32p3fx": [354693734, 15171096151, 16351071311, 16469289221],
    "trv32p3f": [1494618035/2, 67165571446/2, 66433772829/2, 77226916025/2]
}

data_program_memory_in_bytes = {
    "Model": ["BERT-Tiny", "MobileBERT", "MiniLM", "SqueezeBERT"],
    "trv32p3f_U": [190084, 1055708, 437440, 840592],
    "trv32p3fx": [76808, 595880, 158648, 93640],
    "trv32p3f": [74536, 559276, 170664, 96064]
}

# Convert to DataFrames
df_cycles = pd.DataFrame(data_cycle_count)
df_memory = pd.DataFrame(data_program_memory_in_bytes)

# Normalize relative to trv32p3f (baseline = 100%)
df_norm = pd.DataFrame()
df_norm["Model"] = df_cycles["Model"]

df_norm["Cycle_trv32p3f"] = 1
df_norm["Cycle_trv32p3f_U"] = df_cycles["trv32p3f_U"] / df_cycles["trv32p3f"]
df_norm["Cycle_trv32p3fx"] = df_cycles["trv32p3fx"] / df_cycles["trv32p3f"]
print("cycle", df_norm["Cycle_trv32p3f_U"], df_norm["Cycle_trv32p3fx"])

df_norm["Mem_trv32p3f"] = 1
df_norm["Mem_trv32p3f_U"] = df_memory["trv32p3f_U"] / df_memory["trv32p3f"]
df_norm["Mem_trv32p3fx"] = df_memory["trv32p3fx"] / df_memory["trv32p3f"]
print("PM", df_norm["Mem_trv32p3f_U"], df_norm["Mem_trv32p3fx"])

# --- Plot ---
fig, ax1 = plt.subplots(figsize=(18, 13))
plt.tick_params(axis='x', labelsize=23)  # x轴字体大小
plt.tick_params(axis='y', labelsize=23)  # y轴字体大小


bar_width = 0.35
x = np.arange(len(df_norm["Model"]))

# Program memory (bars) - Excluding trv32p3f
rects1 = ax1.bar(x - bar_width/2, df_norm["Mem_trv32p3f_U"], width=bar_width, label="PM (trv32p3f_U)", zorder=1, color="#9ecae1")
rects2 = ax1.bar(x + bar_width/2, df_norm["Mem_trv32p3fx"], width=bar_width, label="PM (trv32p3fx)", zorder=1, color="#fdae6b")

# ax1.set_ylabel("PM Increase")
ax1.set_xticks(x)
ax1.set_xticklabels(df_norm["Model"])
#ax1.set_ylim(0, 900) # Adjust limits as needed

# Calculate acceleration (inverse of normalized cycle count, relative to trv32p3f)
df_norm["Accel_trv32p3f_U"] = df_norm["Cycle_trv32p3f"] / df_norm["Cycle_trv32p3f_U"]
df_norm["Accel_trv32p3fx"] = df_norm["Cycle_trv32p3f"] / df_norm["Cycle_trv32p3fx"]


# Cycle count (lines as acceleration) - Excluding trv32p3f
# ax2 = ax1.twinx()
# ax2.plot(x - bar_width/2, df_norm["Accel_trv32p3f_U"], marker='o', linestyle='-', color='red', label="Acceleration on trv32p3f_U")
# ax2.plot(x + bar_width/2, df_norm["Accel_trv32p3fx"], marker='o', linestyle='-', color='green', label="Acceleration on trv32p3fx")

scale_hi = (9 - 1) / (2.5 - 1)   # = 8 / 1.5 = 5.333...
def right_to_left(r):
    r = np.asarray(r)
    y = np.where(r <= 1, r, 1 + (r - 1) * scale_hi)
    return y

def left_to_right(y):
    y = np.asarray(y)
    r = np.where(y <= 1, y, 1 + (y - 1) / scale_hi)
    return r
# line1, = ax1.plot(x - bar_width/2, right_to_left(df_norm["Accel_trv32p3f_U"]),
#                   marker='o', linestyle='-', label="Acceleration on trv32p3f_U", zorder=3)
# line2, = ax1.plot(x + bar_width/2, right_to_left(df_norm["Accel_trv32p3fx"]),
#                   marker='o', linestyle='--', label="Acceleration on trv32p3fx", zorder=3)

line1, = ax1.plot(x, right_to_left(df_norm["Accel_trv32p3f_U"]),
                  marker='o', linestyle='-', label="Acc. on trv32p3f_U", zorder=3, color="#08519c", linewidth=3.0)
line2, = ax1.plot(x, right_to_left(df_norm["Accel_trv32p3fx"]),
                  marker='o', linestyle='--', label="Acc. on trv32p3fx", zorder=3, color="#e6550d", linewidth=3.0)


right_sec = ax1.secondary_yaxis('right', functions=(left_to_right, right_to_left))
right_sec.set_ylabel("Acceleration", fontsize=40, labelpad=15)
right_sec.tick_params(axis='y', labelsize=40)    #
# 右轴刻度：0, 1, 1.1, ..., 2.5
ticks_r = [0, 1] + [round(1.0 + 0.2*i, 1) for i in range(1, 10)]  # 到 2.5
right_sec.set_yticks(ticks_r)

# 左轴标签与刻度
ax1.set_ylabel("PM (Compared to trv32p3f)", fontsize=40)
ax1.set_yticks(range(0, 12))  # 0~9 线性

ax1.tick_params(axis='x', labelsize=40) 
ax1.tick_params(axis='y', labelsize=40) 

# 基准虚线：y=1（在左轴画即可，右轴的 1 会自动对齐）
ax1.axhline(1, linestyle="--", color="black", linewidth=1, label="trv32p3f")

# # 统一 y 范围到 0–2（右轴的硬性要求）
# ax1.set_ylim(0, 9.0)         # 左轴主轴保持线性“倍数”，但不显示标签
# ax1.set_ylabel("PM")
# ax2.set_ylim(0.0, 2.5)         # 右轴 0–2

# # 右轴刻度：0,1,1.1,...,2
# ax2.set_ylabel("Acceleration")
# ax2.set_yticks([0, 1] + [round(1.0 + 0.2*i, 1) for i in range(1, 8)])

# # x 轴
# ax1.set_xticks(x)
# ax1.set_xticklabels(df_norm["Model"], rotation=20)

# # “1”的虚线：按右轴画，确保对齐
# ax2.axhline(1.0, linestyle="--", linewidth=1, color="black", zorder=1, label="trv32p3f")

# ax2.set_ylabel("Acceleration")
# ax2.set_ylim(0, df_norm[["Accel_trv32p3f_U", "Accel_trv32p3fx"]].max().max() * 1.1) # Adjust limits dynamically

# # Set the same y-limits for both axes
# max_y_limit = max(df_norm["Mem_trv32p3f_U"].max(), df_norm["Mem_trv32p3fx"].max(), df_norm["Accel_trv32p3f_U"].max(), df_norm["Accel_trv32p3fx"].max()) * 1.1
# ax1.set_ylim(0, max_y_limit)
# ax2.set_ylim(0, max_y_limit)

# # Add a horizontal line at 100% for the baseline
# ax1.axhline(100, color="black", linestyle="--", linewidth=1, label="trv32p3f")


# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
# lines2, labels2 = ax1.get_legend_handles_labels()
ax1.legend(lines1, labels1, loc='upper left', fontsize=30)

plt.tight_layout()
plt.savefig('normalized_comparison_swapped_types.svg')
plt.show()
