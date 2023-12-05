from xpytex.defaults.constants.ints.int_handler import int_handler

def googol_rule(x: int) -> str: return r'\text{Googol}' if x == int( '1'+''.join(['0']*100) ) else ''
int_handler.add_rule(googol_rule)