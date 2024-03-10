from .version import version


def logo():

    return f"""\033[92m
    ____    __    ____
    \   \  /  \  /   /     |   \033[95m Welcome to wbs \033[92m
     \   \/    \/   /      |   \033[95m Version : {version} \033[92m
      \            /       |   \033[95m https://github.com/yanrbts/wbs.git \033[92m
       \    /\    /        |   \033[95m Author : yanrbts \033[92m
        \__/  \__/         |   \033[95m Codename : wbs \033[92m

    \033[0m
    """

