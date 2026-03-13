import re
from collections import defaultdict

def accumulate_cycles(file_path):
    """Accumulate total cycle count for each unique instruction mnemonic and print the top 10."""
    total_cycles = defaultdict(int)
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found.")
        return
    
    instruction_section = False
    i = 0
    for line in lines:
        line = line.rstrip()
        # Detect instruction table start
        if line.startswith('    PC         Instruction Assembly'):
            instruction_section = True
            continue
        # Skip headers, separators, or empty lines
        if line.startswith('    ----------') or not instruction_section or not line.strip():
            continue
        # Parse instruction line
        match = re.match(r'\s*(\d+)\s+([0-9a-f\s]+)\s+([a-zA-Z][a-zA-Z0-9\.]*)\s+([^\s].*?)?\s+(\d+)\s+(\d+)\s+(\d+)\s*(\*.*)?$', line)
        if match:
            pc, instruction_code, mnemonic, operands, exe_count, cycles, wait_states, stars = match.groups()
            # total_cycles[mnemonic] += int(cycles)
            total_cycles[mnemonic] += int(exe_count)
        else:
            print(f"Failed to parse line: {line}")
    
    # Sort by total cycles and get top 10
    top_instructions = sorted(total_cycles.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print("\nTop 10 Instructions by Total Cycle Count in instruction_report.txt:")
    if not top_instructions:
        print("No instructions found in the report.")
    else:
        for i, (mnemonic, cycles) in enumerate(top_instructions, 1):
            print(f"{i}. {mnemonic}: {cycles:,} exe_count")


file_path = 'instruction_report_berttiny.txt'
accumulate_cycles(file_path)