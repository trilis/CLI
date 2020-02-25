import os
import io

from src.context import Context


def echo(args, context=Context(), input_text=""):
    """
    prints arguments
    :param args: arguments
    :param context: not used
    :param input_text: not used
    :return: arguments separated by space
    """
    return " ".join(args) + "\n"


def cat(args, context=Context(), input_text=""):
    """
    print file(s) content
    :param args: files
    :param input_text: printed text if args=[]
    :return: files content
    """
    if args == []:
        return input_text
    else:
        answer = ""
        for file in args:
            with open(context.resolve_path(file), "r") as input:
                answer += input.read()
        return answer


def wc(args, context=Context(), input_text=""):
    """
    prints lines number, words number and bytes number of the file
    :param args: files
    :param input_text: used if files=[]
    :return: lines words bytes filename
    """

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
            answer += simple_wc(context.resolve_path(file))
        return answer


def pwd(args, context=Context(), input_text=""):
    """
    prints current directory
    :param args: not used
    :param input_text: not used
    :return: path to current directory
    """
    return context.get_current_path() + "\n"


def exit_(args, context=Context(), input_text=""):
    """
    exit program
    :param args: not used
    :param context: not used
    :param input_text: not used
    :return: exits
    """
    exit(0)


def cd(args, context=Context(), input_text=""):
    if args:
        context.change_directory(args[0])
    else:
        context.set_path_to_home()
    return ""


def ls(args, context=Context(), input_text=""):
    if args:
        path = context.resolve_path(args[0])
    else:
        path = context.get_current_path()
    return "\n".join(sorted(os.listdir(path)))
