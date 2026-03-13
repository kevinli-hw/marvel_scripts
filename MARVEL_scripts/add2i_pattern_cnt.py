import numpy as np
import sys
import re
import pandas as pd
import os

generate_csv = False
seperate_bar_chart = False
union_bar_chart = True

def process_addi_patterns(filepath, out_csv_path, tag):
    try:
        # Read the file content
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # The double addi pattern to match
        pattern = r"""
        addi\s+\S+,\s+\S+,\s*(-?\d+)\s+.*?(\d+)
        (?:.*\n){0,1}?
        .*addi\s+\S+,\s+\S+,\s*(-?\d+)\s+.*?(\d+)
        """

        matches = re.finditer(pattern, content, re.VERBOSE | re.MULTILINE)
              
        double_addi_sequences = {}
        for match in matches:
            # check if addi instructions are executed the same number of times,
            # if not they are in different loops and therefore cannot be optimized
            # print(match)

            exec_count_1 = int(match.group(2))  # Convert to integer
            exec_count_2 = int(match.group(4))  # Convert to integer
            # if tag == 1:
            #     if int(match.group(1)) == 512:
            #         print(match)
            if exec_count_1 == exec_count_2: 
                sequence = str(match.group(1) + '_' + match.group(3))
                # add the execution count to the current number of times this pattern has been counted
                if sequence not in double_addi_sequences:
                    double_addi_sequences[sequence] = exec_count_1
                else:
                    double_addi_sequences[sequence] += exec_count_1 
            
        # Plot a bar chart
        df = pd.DataFrame.from_dict(double_addi_sequences, orient='index')
        # print(df)
        df.to_csv(out_csv_path, header=['execution count'], index_label='pattern')
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# generate pattern data
report_folder = "./model_instruction_report"
pattern_csv_folder = "./model_addi_pattern_data"
if not os.path.exists(pattern_csv_folder):
    os.makedirs(pattern_csv_folder)
if generate_csv:
    for root, dirs, files in os.walk(report_folder):
        for filename in files:
            input_report_path = os.path.join(root, filename)
            out_csv_path = pattern_csv_folder + "/" + filename.split(".")[0] + ".csv"
            print(input_report_path, out_csv_path)
            if filename == "instruction_report_squeezebert.txt":
                process_addi_patterns(input_report_path, out_csv_path, tag=1)
            else:
                process_addi_patterns(input_report_path, out_csv_path, tag=0)

import sys
import matplotlib.pyplot as plt
from adjustText import adjust_text
import re

# Function to check if a pattern is covered
def is_covered(pattern):
    try:
        first, second = map(int, pattern.split('_'))  # Split pattern into two numbers
        return (-2**9 <= first < 2**9) and (-2**4 <= second < 2**4)
    except ValueError:
        return False

file_path = "./model_addi_pattern_data/instruction_report_squeezebert.csv"
IMAGE_FOLDER = "./addi_pattern_cnt"
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)
if seperate_bar_chart:
    models = ['BERT-Tiny', 'MiniLM', 'SqueezeBERT', 'MobileBERT']
    for root, dirs, files in os.walk(pattern_csv_folder):
        for i in range(len(files)):
            input_csv_path = os.path.join(root, files[i])
            out_plt_path = IMAGE_FOLDER + "/" + models[i] + ".svg"
            print(input_csv_path, out_plt_path)

            df = pd.read_csv(input_csv_path)
            df.sort_values('execution count', inplace=True, ascending=False)
            # # Plot a bar chart
            plt.figure(figsize=(10, 6))
            top_N = 8
            y_data = [value/1e9 for value in df.head(top_N)['execution count']]
            plt.bar(df.head(top_N)['pattern'], y_data, color='skyblue')

            plt.xlabel('Pattern', fontsize=18)
            plt.ylabel('Execution count(Billions)', fontsize=18)

            plt.xticks(rotation=0, fontsize=18)
            plt.yticks(fontsize=18)
            title = str('execution count of top ' + str(top_N) + ' most used patterns in ' + models[i])
            # plt.title(title)
            plt.tight_layout()
            plt.savefig(str(IMAGE_FOLDER + "/" +  models[i] + ".svg"), bbox_inches='tight')
            plt.show()

            #====================================================
            # Apply the function to categorize each pattern
            df['covered'] = df['pattern'].apply(is_covered)

            # Aggregate the cycle counts for covered and not covered patterns
            coverage_counts = df.groupby('covered')['execution count'].sum()
            # print(coverage_counts)

            # Calculate total cycle count
            total_cycle_count = coverage_counts.sum()
            # print(total_cycle_count)

            # Compute percentages
            percentages = (coverage_counts / total_cycle_count) * 100
            print(percentages)

            labels = ['Covered', 'Not Covered']
            values = [percentages.get(True, 0), percentages.get(False, 0)]

            # Create the bar chart with percentages
            plt.figure(figsize=(6, 6))
            bars = plt.bar(labels, values, color=['green', 'red'])

            # Add percentage labels on top of bars
            # for bar, percent in zip(bars, values):
            #     plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() -4, f'{percent:.1f}%', ha='center', fontsize=12)

            plt.xlabel('Pattern Coverage', fontsize=12)
            plt.ylabel('Percentage of Cycle Count', fontsize=12)
            plt.title('Percentage of patterns covered by the add2i implementation range', fontsize=14)

            plt.ylim(0, 100)
            # Adjust fontsize
            plt.xticks(fontsize=14)
            plt.yticks(fontsize=14)

            plt.tight_layout()
            plt.savefig(str(IMAGE_FOLDER + "/" +  models[i] + '_coverage_bar.png'))
            plt.show()

            # display(df)
            # print(df['cycle_count'].sum())

def load_pmf(path: str) -> pd.DataFrame:
    """Load one CSV and return a DataFrame with columns: pattern, p (probability)."""
    df = pd.read_csv(path)
    # Normalize column names and aggregate duplicates
    if 'execution count' not in df.columns or 'pattern' not in df.columns:
        raise ValueError(f"CSV {path} must contain columns: 'pattern' and 'execution count'")
    df = df[['pattern','execution count']].copy()
    df = df.groupby('pattern', as_index=False)['execution count'].sum()
    total = df['execution count'].sum()
    df['p'] = df['execution count'] / total if total > 0 else 0.0
    df = df[['pattern','p']].sort_values('p', ascending=False).reset_index(drop=True)
    return df

def build_union_matrix(model_to_path: dict, topk: int) -> pd.DataFrame:
    """Return a matrix DataFrame: rows=models, cols=union of Top-K patterns (+ 'others')."""
    # Top-K per model
    pmfs = {model: load_pmf(path) for model, path in model_to_path.items()}

    # 把四个模型的 PMF 合并，按 pattern 汇总概率并排序
    pool = pd.concat([df.assign(model=model) for model, df in pmfs.items()],
                    ignore_index=True)
    global_rank = (pool.groupby('pattern')['p']
                        .sum()
                        .sort_values(ascending=False))

    # 选出全局 Top-K pattern（比如 K=5）
    selected_patterns = global_rank.head(topk).index.tolist()

    # Build matrix
    cats = selected_patterns + ['others']
    M = pd.DataFrame(index=list(model_to_path.keys()), columns=cats, dtype=float)

    for model, path in model_to_path.items():
        pmf = load_pmf(path)
        pmap = dict(zip(pmf['pattern'], pmf['p']))
        vals = [pmap.get(p, 0.0) for p in selected_patterns]
        others = max(0.0, 1.0 - float(np.sum(vals)))  # clamp to avoid negative due to rounding
        M.loc[model, :] = vals + [others]

    # Order columns by global mass (sum across models), keep 'others' last
    if 'others' in M.columns:
        order = M.drop(columns=['others']).sum(axis=0).sort_values(ascending=False).index.tolist() + ['others']
        M = M[order]
    return M

def plot_grouped_bars(M: pd.DataFrame, out_path: str, title: str = None):
    """Plot a single grouped-bar PMF chart from matrix M (rows=models, cols=patterns)."""
    fig, ax = plt.subplots(figsize=(max(14, 1.2 * len(M.columns)), 7))

    x = np.arange(len(M.columns))
    n_models = len(M.index)
    width = 0.8 / max(n_models, 1)  # keep total group width reasonable
    # Center the bars around ticks
    offsets = (np.arange(n_models) - (n_models - 1) / 2.0) * width

    for j, model in enumerate(M.index):
        ax.bar(x + offsets[j], M.loc[model].values.astype(float), width=width, label=model)

    ax.set_xticks(x)
    ax.set_xticklabels(M.columns.astype(str), fontsize=30)
    ax.set_ylabel('Probability', fontsize=30)
    ax.tick_params(axis='y', labelsize=30) 
    # if title:
    #     ax.set_title(title)
    ymax = float(np.nanmax(M.values)) if M.size > 0 else 1.0
    ax.set_ylim(0, max(0.5, ymax * 1.15))
    ax.legend(ncol=2, loc='upper right', frameon=True, fontsize=24)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"Saved figure to: {out_path}")

if union_bar_chart:
    model_to_path = {}
    topk = 5
    output_path = "./addi_pattern.svg"

    model_to_path['BERT-Tiny'] = "./model_addi_pattern_data/instruction_report_berttiny.csv"
    model_to_path['MobileBERT'] = "./model_addi_pattern_data/instruction_report_mobilebert.csv"
    model_to_path['MiniLM'] = "./model_addi_pattern_data/instruction_report_miniLM.csv"
    model_to_path['SqueezeBERT'] = "./model_addi_pattern_data/instruction_report_squeezebert.csv"

    M = build_union_matrix(model_to_path, topk)

    title = f"Top-{topk} pattern PMF per model (+ others) — single combined chart"
    plot_grouped_bars(M, output_path, title)

