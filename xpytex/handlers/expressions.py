from ast import expr

# Expressions handler
# Depends on the other handlers:
#   - Constants
#   - Names
#   - Attributes
#   - Comparisons
#   - Bool Operations
#   - Binary Operations
#   - Function Calls
class expressions:
    handlers = dict()

    @classmethod
    def register_handler(cls, t: type, handler: object): cls.handlers.update({t:handler})
    
    @classmethod
    def latexify(cls, e: expr) -> str:
        return cls.handlers[type(e)].latexify(e)