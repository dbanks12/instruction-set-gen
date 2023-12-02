import sys
import json
from collections import OrderedDict


OPCODE_LEN = 8
INDIRECT_ARGS_LEN = 8
MODE_LEN = 8
OPERAND_LEN = 16
FULL_OPERAND_LEN = MODE_LEN + OPERAND_LEN
NUM_OPERANDS = 4
INSTR_LEN = OPCODE_LEN + 4*FULL_OPERAND_LEN


def print_sect_header(start_idx, header, options='', file=''):
    bit_idx = start_idx
    bit_idx = print_col(bit_idx, ' ', INSTR_LEN, ', style = none, fontsize = 32', file)
    bit_idx = print_col(bit_idx, header, INSTR_LEN, f', style = none, fontsize = 32, color = lightgray{options}', file)
    return bit_idx


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

#bit_formats = [
#    {"Opcode":{"code":"0x00","size":8},"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"bOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}]},
#    {"Opcode":{"code":"0x01","size":8},"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"bOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}]},
#]
#    {"Opcode":{"code":"0x02","size":8},"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"bOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}]},{"Opcode":{"code":"0x03","size":8},"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"bOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}]},{"Opcode":{"code":"0x04","size":8},"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"bOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}]},{"Opcode":{"code":"0x05","size":8},"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"bOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}]},{"Opcode":{"code":"0x06","size":8},"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"bOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}]},{"Opcode":{"code":"0x07","size":8},"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"bOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}]},{"Opcode":{"code":"0x08","size":8},"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"bOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}]},{"Opcode":{"code":"0x09","size":8},"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}]},{"Opcode":{"code":"0x0a","size":8},"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"bOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}]},{"Opcode":{"code":"0x0b","size":8},"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"bOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}]},{"Opcode":{"code":"0x0c","size":8},"Indirect":8,"Args":[{"name":"const","size":"N"},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}]},{"Opcode":{"code":"0x0d","size":8},"Indirect":8,"Args":[{"name":"srcOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x0e","size":8},"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"bOffset","size":24},{"name":"condOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x0f","size":8},"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[{"name":"dest-type","size":8}]},{"Opcode":{"code":"0x10","size":8},"Indirect":8,"Args":[{"name":"cdOffset","size":24},{"name":"size","size":24},{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x11","size":8},"Indirect":8,"Args":[{"name":"slotOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x12","size":8},"Indirect":8,"Args":[{"name":"srcOffset","size":24},{"name":"slotOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x13","size":8},"Indirect":8,"Args":[{"name":"keyOffset","size":24},{"name":"dstMsgOffset","size":24},{"name":"dstSibPathOffset","size":24},{"name":"dstLeafIndexOffset","size":24},{"name":"dstRootOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x14","size":8},"Indirect":8,"Args":[{"name":"keyOffset","size":24},{"name":"dstMsgOffset","size":24},{"name":"dstSibPathOffset","size":24},{"name":"dstLeafIndexOffset","size":24},{"name":"dstRootOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x15","size":8},"Indirect":8,"Args":[{"name":"loc","size":24}],"Flags":[]},{"Opcode":{"code":"0x16","size":8},"Indirect":8,"Args":[{"name":"loc","size":24},{"name":"condOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x17","size":8},"Indirect":8,"Args":[{"name":"offset","size":24},{"name":"size","size":24}],"Flags":[]},{"Opcode":{"code":"0x18","size":8},"Indirect":8,"Args":[{"name":"offset","size":24},{"name":"size","size":24}],"Flags":[]},{"Opcode":{"code":"0x19","size":8},"Indirect":8,"Args":[{"name":"l1GasOffset","size":24},{"name":"l2GasOffset","size":24},{"name":"addrOffset","size":24},{"name":"argsOffset","size":24},{"name":"argsSize","size":24},{"name":"retOffset","size":24},{"name":"retSize","size":24},{"name":"successOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x1a","size":8},"Indirect":8,"Args":[{"name":"l1GasOffset","size":24},{"name":"l2GasOffset","size":24},{"name":"addrOffset","size":24},{"name":"argsOffset","size":24},{"name":"argsSize","size":24},{"name":"retOffset","size":24},{"name":"retSize","size":24},{"name":"successOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x1b","size":8},"Indirect":8,"Args":[{"name":"offset","size":24},{"name":"size","size":24}],"Flags":[]},{"Opcode":{"code":"0x1c","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x1d","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x1e","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x1f","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x20","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x21","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x22","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x23","size":8},"Indirect":8,"Args":[{"name":"blockNumOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x24","size":8},"Indirect":8,"Args":[{"name":"blockNumOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x25","size":8},"Indirect":8,"Args":[{"name":"blockNumOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x26","size":8},"Indirect":8,"Args":[{"name":"blockNumOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x27","size":8},"Indirect":8,"Args":[{"name":"blockNumOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x28","size":8},"Indirect":8,"Args":[{"name":"blockNumOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x29","size":8},"Indirect":8,"Args":[{"name":"blockNumOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x2a","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x2b","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x2c","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x2d","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x2e","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x2f","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x30","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x31","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x32","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]},{"Opcode":{"code":"0x33","size":8},"Indirect":8,"Args":[{"name":"dstOffset","size":24}],"Flags":[]}]
for bit_format in bit_formats:
    for arg in bit_format['Flags'] + bit_format['Args']:
        if arg['size'] == 'N':
            arg['size'] = 128
    #bit_format = {"Opcode":8,"Indirect":8,"Args":[{"name":"const","size":"N"},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}]}
    #bit_format = {"Opcode":8,"Indirect":8,"Args":[{"name":"aOffset","size":24},{"name":"dstOffset","size":24}],"Flags":[{"name":"op-type","size":8}],"Total":"72"}

    #flags_size = INDIRECT_ARGS_LEN + arr_size(bit_format, 'Flags')
    flags_size = arr_size(bit_format, 'Flags')
    args_size = arr_size(bit_format, 'Args')
    avm_instr_size = OPCODE_LEN + flags_size + args_size

    avm_instr_summary = [
        ('opcode               ', OPCODE_LEN ),
    ]
    #('indirect-args        ', INDIRECT_ARGS_LEN ), # included under 'flags' for now
    if (flags_size > 0):
        avm_instr_summary.append(('flags', flags_size))
    avm_instr_summary.append(('args', args_size))

    instr_name = bit_format['Name'].strip('`')
    avm_instr = [
        (f"{bit_format['Opcode']['code']}", OPCODE_LEN ),
        #('indirect-args        ', INDIRECT_ARGS_LEN ),
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

          #colwidth = {INSTR_LEN}
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

## Instruction format
#print('\n#--------------------------------------------\n')
#bit_idx = print_group(bit_idx, 'highlevel_instr', highlevel_instr)
#print('\n#--------------------------------------------\n')
#bit_idx = print_group(bit_idx, 'detailed_instr', detailed_instr)
#print('\n#--------------------------------------------\n')
#############################################################################
## Legend
#bit_idx = print_col(bit_idx, ' ', INSTR_LEN, ', style = none, fontsize = 32')
#bit_idx = print_col(bit_idx, '"Legend:"', INSTR_LEN, ', style = none, fontsize = 32, colwidth = 8')
#bit_idx = print_col(bit_idx, '"imm: "', 10, ', style = none, fontsize = 32')
#bit_idx = print_col(bit_idx, '"operand is an immediate value. An immediate/constant value is present in the bytecode."', INSTR_LEN - 10, ', style = none, colwidth = 53')
#bit_idx = print_col(bit_idx, '"ind: "', 10, ', style = none, fontsize = 32')
#bit_idx = print_col(bit_idx, '"operand is an indirect value. An indirect value points to a location in memory which is itself an address."', INSTR_LEN - 10, ', style = none, colwidth = 65')
#bit_idx = print_col(bit_idx, '"res: "', 10, ', style = none, fontsize = 32')
#bit_idx = print_col(bit_idx, '"these bits are reserved and therefore unused by this instruction format"', INSTR_LEN - 10, ', style = none, colwidth = 45')
#bit_idx = print_col(bit_idx, '"X: "', 11, ', style = none, fontsize = 32')
#bit_idx = print_col(bit_idx, '"the value of this bit does not matter"', INSTR_LEN - 11, ', style = none, colwidth = 23')
#bit_idx = print_col(bit_idx, '"XXX: "', 10, ', style = none, fontsize = 32')
#bit_idx = print_col(bit_idx, '"the value of these bits does not matter"', INSTR_LEN - 10, ', style = none, colwidth = 26')
#bit_idx = print_col(bit_idx, '"RED: "', 10, ', style = none, fontsize = 32, textcolor = darkred')
#bit_idx = print_col(bit_idx, '"instruction is not yet supported"', INSTR_LEN - 10, ', style = none, colwidth = 22')
#############################################################################
## Basic ADD
#add_basic_prefix = [
#    ('ADD' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , 'no' , None , 'u8' , '<address>')) ,
#    ( 'sd' , gen_operand_arr(None , None , None , None , None))        ,
#    ( 's0' , gen_operand_arr(None , 'no' , None , None , '<address>')) ,
#    ( 's1' , gen_operand_arr(None , 'no' , None , None , '<address>')) ,
#]
#add_basic = [
#    ('ADD' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , '0'  , None , '000' , '7')) ,
#    ( 'sd' , gen_operand_arr(None , None , None , None  , None)) ,
#    ( 's0' , gen_operand_arr(None , '0'  , None , None  , '42'))  ,
#    ( 's1' , gen_operand_arr(None , '0'  , None , None  , '55')) ,
#]
#add_basic_example = [
#    'M₈[d0] = M₈[s0] + M₈[s1]',
#    'M₈[ 7] = M₈[42] + M₈[55]',
#]
#
#bit_idx = full_example(bit_idx, 'Basic ADD', add_basic_prefix, add_basic, add_basic_example)
#############################################################################
#print('\n#--------------------------------------------\n')
#############################################################################
## ADD with an indirect s0
#add_ind_prefix = [
#    ('ADD' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , 'no'  , None , 'u16' , '<address>')) ,
#    ( 'sd' , gen_operand_arr(None , None  , None , None  , None))        ,
#    ( 's0' , gen_operand_arr(None , 'yes' , None , None  , '<address>')) ,
#    ( 's1' , gen_operand_arr(None , 'no'  , None , None  , '<address>')) ,
#]
#add_ind = [
#    ('ADD' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , '0'  , None , '001' , '7')) ,
#    ( 'sd' , gen_operand_arr(None , None , None , None  , None)) ,
#    ( 's0' , gen_operand_arr(None , '1'  , None , None  , '42'))  ,
#    ( 's1' , gen_operand_arr(None , '0'  , None , None  , '55')) ,
#]
#add_ind_example = [
#    'M₁₆[d0] = M₁₆[M₃₂[s0]] + M₁₆[s1]',
#    'M₁₆[ 7] = M₁₆[M₃₂[42]] + M₁₆[55]',
#    'Any operand of any instruction can be an indirect value (as long as it is not an \'immediate\').',
#]
#
#bit_idx = full_example(bit_idx, 'ADD with an indirect s0', add_ind_prefix, add_ind, add_ind_example)
#############################################################################
#print('\n#--------------------------------------------\n')
#############################################################################
## Basic SET
#set_basic_prefix = [
#    ('SET' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None  , 'no'  , None , 'u64' , '<address>')) ,
#    ( 'sd' , gen_operand_arr(None  , None  , None , None  , None))        ,
#    ( 's0' , gen_operand_arr('yes' , None  , None , None  , '<64-bit-value>')) ,
#    ( 's1' , gen_operand_arr(None  , None  , None , None  , None)) ,
#]
#set_basic = [
#    ('SET' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , '0'  , None , '011' , '7')) ,
#    ( 'sd' , gen_operand_arr(None , None , None , None  , None)) ,
#    ( 's0' , gen_operand_arr('1'  , None , None , None  , '49')) ,
#    ( 's1' , gen_operand_arr(None , None , None , None  , None)) ,
#]
#set_basic_example = [
#    'M₆₄[d0] = s0',
#    'M₆₄[ 7] = 49',
#    'Instruction size depends on type since s0 contains a full value as opposed to an address.',
#]
#
#bit_idx = full_example(bit_idx, 'Basic SET', set_basic_prefix, set_basic, set_basic_example)
#############################################################################
#print('\n#--------------------------------------------\n')
#############################################################################
## Basic MOV
#mov_basic_prefix = [
#    ('MOV' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , 'no'  , None , 'field' , '<address>')) ,
#    ( 'sd' , gen_operand_arr(None , None  , None , None    , None))        ,
#    ( 's0' , gen_operand_arr(None , None  , None , None    , '<address>')) ,
#    ( 's1' , gen_operand_arr(None , None  , None , None    , None)) ,
#]
#mov_basic = [
#    ('MOV' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , '0'  , None , '100' , '7')) ,
#    ( 'sd' , gen_operand_arr(None , None , None , None  , None)) ,
#    ( 's0' , gen_operand_arr(None , None , None , '100' , '49')) ,
#    ( 's1' , gen_operand_arr(None , None , None , None  , None)) ,
#]
#mov_basic_example = [
#    'M_f[d0] = M_f[s0]',
#    'M_f[ 7] = M_f[49]',
#    'M_f here refers to the region of memory for \'fields\'',
#    'Since d0 and s0 share the \'field\' type, no type conversion is performed.'
#
#]
#
#bit_idx = full_example(bit_idx, 'Basic MOV', mov_basic_prefix, mov_basic, mov_basic_example)
#############################################################################
#print('\n#--------------------------------------------\n')
#############################################################################
## MOV with type conversion
#mov_conv_prefix = [
#    ('MOV' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , 'no'  , None , 'u64' , '<address>')) ,
#    ( 'sd' , gen_operand_arr(None , None  , None , None  , None))        ,
#    ( 's0' , gen_operand_arr(None , 'no'  , None , 'u16' , '<address>')) ,
#    ( 's1' , gen_operand_arr(None , None  , None , None  , None)) ,
#]
#mov_conv = [
#    ('MOV' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , '0'  , None , '011' , '7')) ,
#    ( 'sd' , gen_operand_arr(None , None , None , None  , None)) ,
#    ( 's0' , gen_operand_arr(None , '0'  , None , '010' , '49')) ,
#    ( 's1' , gen_operand_arr(None , None , None , None  , None)) ,
#]
#mov_conv_example = [
#    'M₆₄[d0] = M₁₆[s0]',
#    'M₆₄[ 7] = M₁₆[49]',
#    'Since d0 and s0 do NOT share the same type, this MOV converts from u16 to u64.',
#]
#
#bit_idx = full_example(bit_idx, 'MOV with type conversion', mov_conv_prefix, mov_conv, mov_conv_example)
#############################################################################
#print('\n#--------------------------------------------\n')
#############################################################################
## MOV with indirect d0
#mov_ind_prefix = [
#    ('MOV' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , 'yes' , None , 'u64' , '<address>')) ,
#    ( 'sd' , gen_operand_arr(None , None  , None , None  , None))        ,
#    ( 's0' , gen_operand_arr(None , 'no'  , None , 'u16' , '<address>')) ,
#    ( 's1' , gen_operand_arr(None , None  , None , None  , None)) ,
#]
#mov_ind = [
#    ('MOV' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , '1'  , None , '011' , '7')) ,
#    ( 'sd' , gen_operand_arr(None , None , None , None  , None)) ,
#    ( 's0' , gen_operand_arr(None , '0'  , None , '010' , '49')) ,
#    ( 's1' , gen_operand_arr(None , None , None , None  , None)) ,
#]
#mov_ind_example = [
#    'M₆₄[M₃₂[d0]] = M₁₆[s0]',
#    'M₆₄[M₃₂[ 7]] = M₁₆[49]',
#]
#
#bit_idx = full_example(bit_idx, 'MOV with indirect d0', mov_ind_prefix, mov_ind, mov_ind_example)
#############################################################################
#print('\n#--------------------------------------------\n')
#############################################################################
## Basic CMOV
#cmov_ind_prefix = [
#    ('CMOV' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , 'no'  , None , 'u16' , '<address>')) ,
#    ( 'sd' , gen_operand_arr(None , 'no'  , None , None  , '<address>')) ,
#    ( 's0' , gen_operand_arr(None , 'no'  , None , None  , '<address>')) ,
#    ( 's1' , gen_operand_arr(None , 'no'  , None , None  , '<address>')) ,
#]
#cmov_ind = [
#    ('CMOV' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , '0' , None , '011' , '7')) ,
#    ( 'sd' , gen_operand_arr(None , '0' , None , None  , '42')) ,
#    ( 's0' , gen_operand_arr(None , '0' , None , None  , '49')) ,
#    ( 's1' , gen_operand_arr(None , '0' , None , None  , '55')) ,
#]
#cmov_ind_example = [
#    'M₁₆[d0] = M₁₆[sd] ? M₁₆[s0] : M₁₆[s1]',
#    'M₁₆[ 7] = M₁₆[42] ? M₁₆[49] : M₁₆[55]',
#    'Conditional (ternary) move.',
#    'M₁₆[sd] is treated as 1 bit here.',
#]
#
#bit_idx = full_example(bit_idx, 'Basic CMOV', cmov_ind_prefix, cmov_ind, cmov_ind_example)
#############################################################################
#print('\n#--------------------------------------------\n')
#############################################################################
## XMUL [NOT YET SUPPORTED]
#xmul_basic_prefix = [
#    ('XMUL' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , 'no' , None , 'u16' , '<address>')) ,
#    ( 'sd' , gen_operand_arr(None , 'no' , None , None  , '<address>'))        ,
#    ( 's0' , gen_operand_arr(None , 'no' , None , None  , '<address>')) ,
#    ( 's1' , gen_operand_arr(None , 'no' , None , None  , '<address>')) ,
#]
#xmul_basic = [
#    ('XMUL' , OPCODE_LEN),
#    ( 'd0' , gen_operand_arr(None , '0' , None , '010' , '7')) ,
#    ( 'sd' , gen_operand_arr(None , '0' , None , None  , '42')) ,
#    ( 's0' , gen_operand_arr(None , '0' , None , None  , '49')) ,
#    ( 's1' , gen_operand_arr(None , '0' , None , None  , '55')) ,
#]
#xmul_basic_example = [
#    'M₁₆[d0] + (2^k)M₁₆[sd] = M₁₆[s0] * M₁₆[s1]',
#    'M₁₆[ 7] + (2^k)M₁₆[42] = M₁₆[49] * M₁₆[55]',
#]
#
#bit_idx = full_example(bit_idx, 'XMUL (NOT YET SUPPORTED)', xmul_basic_prefix, xmul_basic, xmul_basic_example, header_options=', textcolor = darkred')
#############################################################################
#print('\n#--------------------------------------------\n')
#############################################################################
#
#
#print('}')
