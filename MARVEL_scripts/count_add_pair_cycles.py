import re

def accumulate_consecutive_add_cycles(file_path):
    total_consecutive_add_cycles = 0
    current_function = None
    instruction_section = False
    instructions = []
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found.")
        return 0
    
    for line in lines:
        line = line.rstrip()
        # Detect function section start
        if line.startswith('Function detail:'):
            # Process previous function's instructions if any
            if instructions:
                total_consecutive_add_cycles += process_instructions(instructions)
            instructions = []
            current_function = line.split('Function detail: ')[1].strip()
            instruction_section = False
            continue
        # Detect instruction table start
        if line.startswith('    PC         Instruction Assembly'):
            instruction_section = True
            continue
        # Skip header, separator, or empty lines
        if line.startswith('    ----------') or not instruction_section or not line.strip():
            continue
        # Parse instruction line
        match = re.match(r'\s*(\d+)\s+([0-9a-f\s]+)\s+([a-zA-Z][a-zA-Z0-9\.]*)\s+([^\s].*?)?\s+(\d+)\s+(\d+)\s+(\d+)\s*(\*.*)?$', line)
        if match:
            pc, instruction_code, mnemonic, operands, exe_count, cycles, wait_states, stars = match.groups()
            instructions.append({
                'mnemonic': mnemonic,
                'exe_count': int(exe_count)
            })
        else:
            print(f"Failed to parse line: {line}")
    
    # Process the last function's instructions
    if instructions:
        total_consecutive_add_cycles += process_instructions(instructions)
    
    return total_consecutive_add_cycles

def process_instructions(instructions):
    consecutive_add_cycles = 0
    i = 0
    while i < len(instructions):
        if instructions[i]['mnemonic'] == instruction_looking_for:
            # Find the length of consecutive 'add'
            start = i
            while i < len(instructions) and instructions[i]['mnemonic'] == instruction_looking_for:
                i += 1
            length = i - start
            if length >= 2:
                # Sum cycles of all 'add' in this consecutive group
                for j in range(start, i):
                    consecutive_add_cycles += instructions[j]['exe_count']
        else:
            i += 1
    return consecutive_add_cycles

if __name__ == "__main__":
    # file_path = 'instruction_report_mobilebert.txt'
    # file_path = 'instruction_report_miniLM.txt'
    # file_path = 'instruction_report_squeezebert.txt'
    file_path = 'instruction_report_berttiny.txt'
    instruction_looking_for = 'add'
    total_cycles = accumulate_consecutive_add_cycles(file_path)
    print(f"Total cycles consumed by consecutive {instruction_looking_for} instructions (in pairs or longer): {total_cycles}")