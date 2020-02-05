import os
import io


def echo(args, input_text):
    return " ".join(args) + "\n"


def cat(args, input_text):
    if args == []:
        return input_text
    else:
        answer = ""
        for file in args:
            with open(file, "r") as input:
                answer += input.read()
        return answer


def wc(args, input_text):
    def simple_wc(file):
        with open(file, "r") as input:
            lines = input.readlines()
            lines_num = len(lines)
            words_num = sum([len(line.split()) for line in lines])
            size = os.stat(file).st_size
            return str(lines_num) + " " + str(words_num) + " " + str(size) + " " + file + "\n"

    if args == []:
        with io.StringIO(input_text) as input:
            lines = input.readlines()
            lines_num = len(lines)
            words_num = sum([len(line.split()) for line in lines])
            size = len(input_text.encode("utf-8"))
            return str(lines_num) + " " + str(words_num) + " " + str(size) + "\n"

    else:
        answer = ""
        for file in args:
            answer += simple_wc(file)
        return answer


def pwd(args, input_text):
    return os.path.abspath(os.getcwd()) + "\n"


def exit_(args, input_text):
    exit(0)
