#Check against random input, buffer overflow 
# Test: authentification , usename and passowrd are tested, code from Arduino is tested
 

import random

# easy fuzzer to start with
def fuzzer_xxs():
    return

def fuzzer_buff_overflow():
    return 

def fuzzer_form(max_length: int = 100, char_start: int = 32, char_range: int = 32) -> str:
    """A string of up to `max_length` characters
       in the range [`char_start`, `char_start` + `char_range`)"""
    string_length = random.randrange(0, max_length + 1)
    out = ""
    for i in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return out





def fuzzer_code(max_length: int = 100, char_start: int = 32, char_range: int = 32) -> str:
    pass
    
    
