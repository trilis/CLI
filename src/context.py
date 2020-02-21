import os


class Context:
    __current_path = os.path.abspath(os.getcwd())

    def get_current_path(self):
        return self.__current_path

    def change_directory(self, next_folder):
        new_path = self.__current_path + "/" + next_folder
        if os.path.isdir(new_path):
            self.__current_path = os.path.abspath(new_path)
        else:
            raise FileNotFoundError(new_path + " does not exist or is not a directory")

    def set_path_to_home(self):
        self.__current_path = os.path.expanduser("~")

    def resolve_path(self, path):
        expanded_path = os.path.expanduser(path)
        if os.path.isabs(expanded_path):
            return expanded_path
        else:
            return self.__current_path + "/" + expanded_path
