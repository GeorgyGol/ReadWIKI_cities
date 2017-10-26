import re

def get_code(strX):
    strT = re.match(r'(\d+)', strX.replace(' ', '')).group(0)
    return strT

print(get_code('07 222 501 000'))

def get_num(strX, to_type=int):
    strT=re.sub(r'\s', '', strX).replace(',', '.')
    return to_type(re.search(r'\d+\.?\d*', strT).group(0))

print(get_num('140 м'))

strX='17.5'

if '.' in strX:
    print(True)
