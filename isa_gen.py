import sys
import json
from collections import OrderedDict


def print_text_col(start_idx, text, bit_len, options='', file=''):
    options = options + f', colwidth = {len(text)}'
    return print_col(start_idx, text, bit_len, options, file)

def print_col(start_idx, name, bit_len, options='', file=''):
    assert bit_len > 0
    last_bit_idx = start_idx+bit_len-1
    end_idx_str = f'-{last_bit_idx}' if bit_len > 1 else ''  # form S:E-1
    # TODO conditionally rotate_str
    size_rotate_str = ''
    if bit_len == 1 and len(name) > 1:
        size_rotate_str = ', rotate = 270, fontsize = 16'
    print(f'{start_idx}{end_idx_str}:\t\t{name}\t\t[len = {bit_len}{size_rotate_str}{options}]', file=file)
    return start_idx + bit_len


# group is an array of tuples
def print_group(start_idx, group_name, group, file=''):
    bit_idx = start_idx
    for name, val, *options in group:
        print(f'# {name}: {val}', file=file)
        if isinstance(val, int):
            bit_idx = print_col(bit_idx, name, val, options[0] if options else '', file)
        else:
            bit_idx = print_group(bit_idx, name, val, file)
    return bit_idx


def arr_size(instr, key):
    return sum([arg['size'] for arg in instr[key]])

with open(sys.argv[1]) as json_file:
    bit_formats = json.load(json_file)

for bit_format in bit_formats:
    for arg in bit_format['Flags'] + bit_format['Args']:
        if arg['size'] == 'N':
            arg['size'] = 128

    opcode_size = bit_format['Opcode']['size']
    reserved_size = bit_format['Reserved']['size']
    flags_size = arr_size(bit_format, 'Flags')
    args_size = arr_size(bit_format, 'Args')
    avm_instr_size = opcode_size + reserved_size + flags_size + args_size

    avm_instr_summary = [
        ('opcode               ', opcode_size ),
        ('reserved             ', reserved_size ),
    ]
    if (flags_size > 0):
        avm_instr_summary.append(('flags', flags_size))
    avm_instr_summary.append(('args', args_size))

    instr_name = bit_format['Name'].strip('`')
    avm_instr = [
        (f"{bit_format['Opcode']['code']}", opcode_size ),
        ("XXX", opcode_size ),
    ]

    for flag in bit_format['Flags']:
        name = flag['name']
        size = flag['size']
        avm_instr.append((name, size))

    for arg in bit_format['Args']:
        name = arg['name']
        size = arg['size']
        if size == 'N':
            size = 128
        avm_instr.append((name, size))

    bit_idx = 0

    with open(f'gen/{instr_name}.diag', 'w') as file:
        print('packetdiag {', file=file)
        diag_settings = f'''
          #node_width = 160;
          #node_height = 160;
          #span_width = 32;
          span_height = 1;  # height of space for each row - increasing will add space between rows
          default_fontsize = 28;
          #default_shape = diamond
          #default_node_style = dotted
          #default_node_color = red
          #default_group_color = blue
          #default_linecolor = pink
          #default_textcolor = green
          #default_label_orientation = vertical

          colwidth = {avm_instr_size}
          #scale_direction = rtl  # 0th bit on left or right
          scale_interval = 8  # label tick for every 8th bit
        '''
        print(diag_settings, file=file)


        ############################################################################
        bit_idx = print_group(bit_idx, 'avm_instr_summary', avm_instr_summary, file=file)
        bit_idx = print_group(bit_idx, 'avm_instr', avm_instr, file=file)
        ############################################################################
        print('\n#--------------------------------------------\n', file=file)
        print('}', file=file)
