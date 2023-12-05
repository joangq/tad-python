from xpytex.defaults.constants.strs.str_handler import str_handler

def rule_LaTeXstr(x: str):
    return (r'\LaTeX' if x == 'LaTeX' else '')

str_handler.add_rule(rule_LaTeXstr)
# displaymath( str_handler.apply('LaTeX') )