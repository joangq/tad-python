from xpytex import attributes

def empty_set_attribute_rule(parent, attribute) -> str:
    return '' if parent != 'Conjunto' else r'\{\}' if attribute == 'vacio' else ''

def empty_seq_attribute_rule(parent, attribute) -> str:
    return '' if parent != 'Secuencia' else r'\langle\rangle' if attribute == 'vacia' else ''

attributes.add_rule(empty_set_attribute_rule)
attributes.add_rule(empty_seq_attribute_rule)