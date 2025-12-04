import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir,'secret.daz')

with open(file_path,'r',encoding = 'utf-8') as f :
    content = f.read()

hex_list = []
split_result = content.split('X')
for item in split_result:
    if item:
        hex_list.append(item)

decoded_chars = []
for hex_str in hex_list:
    try:
        char_code = int(hex_str,16)
        decoded_chars.append(chr(char_code))
    except ValueError:
        continue

S = ''.join(decoded_chars)

visible_chars = [c for c in S if c not in [' ','\t','\n']]
visible_count = len(visible_chars)

student_id = '2025090912004'
S1 = f"<解密人>{student_id}<情报总字数>{visible_count}"

interpretation_path = os.path.join(script_dir, 'interpretation.txt')

with open(interpretation_path, 'w', encoding='utf-8') as f:
    f.write(S)
    f.write('\n')
    f.write(S1)