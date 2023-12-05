from xpytex import bool_operations
from ast import And, Or

def bool_and_handler(values: list[str]) -> str: return r' \land{} '.join(str(x) for x in values)
def bool_or_handler(values: list[str]) -> str: return r' \lor{} '.join(str(x) for x in values)

bool_operations.register_handler(And, bool_and_handler)
bool_operations.register_handler(Or, bool_or_handler)