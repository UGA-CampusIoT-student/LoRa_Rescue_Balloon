
from random import randint

def convert (input_float):
    print ('input_float:', input_float)
    input_int = int (input_float * 10000)
    print ('input_int:', input_int)
    print ('input_hex:', hex (input_int))
    hex_0 = 0xff0000
    hex_1 = 0x00ff00
    hex_2 = 0x0000ff
    print ('output_list:', [hex ((input_int & hex_0) >> 4 * 4), hex ((input_int & hex_1) >> 4 * 2), hex (input_int & hex_2)])
    return [hex ((input_int & hex_0) >> 4 * 4), hex ((input_int & hex_1) >> 4 * 2), hex (input_int & hex_2)]

lis = convert(-54.65)

print(lis)