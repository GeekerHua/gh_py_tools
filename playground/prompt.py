from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion.word_completer import WordCompleter
from prompt_toolkit.completion.fuzzy_completer import FuzzyWordCompleter


SQLCompleter = WordCompleter(['select', 'from', 'insert', 'update', 'delete', 'drop'],
                             ignore_case=True)

# SQLCompleter = FuzzyWordCompleter(['select', 'from', 'insert', 'update', 'delete', 'drop'])

while 1:
    user_input = prompt('SQL>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=SQLCompleter,
                        )
    print(user_input)
