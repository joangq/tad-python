from IPython.display import display, Math, Markdown

def displaymd(text): display(Markdown(text))

def display_code(code, language='python'):
    display(Markdown(f"""```{language}\n{code}\n```"""))

def displaymath(math: str): display(Math(math))