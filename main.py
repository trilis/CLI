from src.interpreter import perform, Context
from src.parser import parse


def main():
    context = Context()
    while True:
        print('$', end=' ')
        string = input()
        commands_parts = parse(string)
        output = perform(commands_parts, context)
        print(output)


if __name__ == "__main__":
    main()
