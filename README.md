# CLI

Software Design homeworks

Data flow diagram:
![Data flow diagram](https://github.com/Andreev-Nikita-1/CLI/raw/cli/graf.jpg)

С консоли последовательно считываются строки.
Каждая строка парсится (src/parser):
Сначала происходит разбиение на команды.
Затем в каждую команду проставляются значения переменных.
Далее команды разбиваются на отдельные аргументы.
После этого каждая для каждой команды создается экземпляр класса Command.
Это может быть встроенная команда из src/commands, присваивание переменной, или внешняя команда.
Затем в perform происходит последовательное выполнение команд, после чего последняя из них возвращает результат.
