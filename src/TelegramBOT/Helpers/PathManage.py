import os
from telegram import InlineKeyboardButton


class PathManage:

    def create_dir(path) -> None:
        if not os.path.exists(path):
            os.makedirs(path)

    def merge_path(path, dir) -> str:
        if dir == '..':
            path = os.path.realpath(os.path.join(path, '..'))
        else:
            path = os.path.join(path, dir)

        return path

    def get_dir_list(path) -> str:
        dirs = []
        for name in os.listdir(path):
            d = os.path.join(path, name)
            if os.path.isdir(d):
                dirs.append(f'{os.path.basename(d)}')

        return dirs

    def GetInlineAllDirectories(path, root_path):
        inline_button = []
        row_button = []
        i = 1
        directories = PathManage.get_dir_list(path)

        if not PathManage.is_path_contained(path, root_path):
            raise Exception(f"The path '{path}' is not contained in '{root_path}'")
        
        row_button.append(InlineKeyboardButton(text='..', callback_data='..'))
        for row in directories:
            if i < 2:
                row_button.append(InlineKeyboardButton(text=row, callback_data=row))
                i += 1
            
            if (i >= 2) or (directories[-1] == row_button[-1].text):
                inline_button.append(row_button)
                row_button = []
                i = 0
        
        if len(directories) == 0:
            inline_button.append(row_button)
        return inline_button

    def is_path_contained(inner_path, outer_path):
        common_path = os.path.commonpath([inner_path, outer_path])
        return os.path.samefile(common_path, outer_path)
