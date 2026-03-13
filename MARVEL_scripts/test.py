import numpy as np
import matplotlib.pyplot as plt

# 配置边界
MAX_FIRST  = 1023
MAX_SECOND = 31
BASE = MAX_SECOND + 1
INSIDE_RIGHT = MAX_FIRST * BASE + MAX_SECOND  # 配置区间在 [0, INSIDE_RIGHT]

# 示例：把你的真实数据组织成这个 dict 结构
# data_by_model['BERT-Tiny'] = (first_array, second_array, count_array)
data_by_model = {
    # 'BERT-Tiny': (np.array([...]), np.array([...]), np.array([...])),
    # 'MobileBERT': (...),
    # 'MiniLM': (...),
    # 'SqueezeBERT': (...),
}

# 不同模型的点型（可改）
marker_map = {
    'BERT-Tiny': 'o',       # circle
    'MobileBERT': 's',      # square
    'MiniLM': '^',          # triangle_up
    'SqueezeBERT': 'D',     # diamond
}

# 给不同模型的轻微 x 偏移，避免同一 pattern_id 上完全重叠
offsets = np.linspace(-0.25, 0.25, num=len(marker_map))

fig, ax = plt.subplots(figsize=(18, 6))
handles = []
labels  = []

for (model, (first, second, count)), dx in zip(data_by_model.items(), offsets):
    first  = np.asarray(first)
    second = np.asarray(second)
    count  = np.asarray(count)

    # 一维展开
    pid = first * BASE + second

    # inside / outside 用不同描边或透明度做轻微区分（可选）
    inside = (first >= 0) & (first <= MAX_FIRST) & (second >= 0) & (second <= MAX_SECOND)

    # 画点：不同模型不同 marker，整体加一点透明度防重叠
    sc = ax.scatter(pid + dx, count, marker=marker_map.get(model, 'o'),
                    s=24, alpha=0.85, edgecolors='none', label=model, rasterized=True)
    handles.append(sc); labels.append(model)

    # 也可以叠一层空心点强调 outside（可选）
    # ax.scatter((pid+dx)[~inside], count[~inside], marker=marker_map.get(model,'o'),
    #            s=24, facecolors='none', edgecolors='black', linewidths=0.7, alpha=0.8, rasterized=True)

# 高亮配置区间：左边界 0，右边界 INSIDE_RIGHT
ax.axvspan(-0.5, INSIDE_RIGHT + 0.5, color='tab:green', alpha=0.08)
ax.axvline(-0.5,           ls='--', lw=1.2, color='gray')
ax.axvline(INSIDE_RIGHT+0.5, ls='--', lw=1.2, color='gray')
ax.text(INSIDE_RIGHT/2, ax.get_ylim()[1]*0.95, 'config included', ha='center', va='top', fontsize=11, color='tab:green')

# 轴与比例
ax.set_yscale('symlog', linthresh=10)   # 或 ax.set_yscale('log')
ax.set_xlim(-0.5, None)
ax.set_xlabel('pattern id = first * ({} ) + second'.format(BASE))
ax.set_ylabel('Execution Count')
ax.legend(handles, labels, ncol=4, loc='upper right', frameon=True, title='Model')

# x 轴不打密集刻度，只保留关键边界
ax.set_xticks([0, INSIDE_RIGHT])
ax.set_xticklabels(['0', str(INSIDE_RIGHT)])

plt.tight_layout()
plt.show()
