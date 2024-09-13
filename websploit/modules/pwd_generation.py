import argparse
import math
import os
import os.path
import random
import re
import sys
from io import open

from websploit.core import base

DEFAULT_FOLDER = "wordlist"
DEFAULT_WORDFILE = "eff-long"
DEFAULT_DELIMITERS = [" ", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
                      "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

class Main(base.Module):
    """Password Generation"""
    
    parameters = {
        "SecLists": "https://github.com/danielmiessler/SecLists.git",
        "RockYou": "https://github.com/praetorian-inc/Hob0Rules.git",
        "SkullSecurity Wordlists": "https://github.com/berzerk0/Probable-Wordlists.git",
        "hashesorg": "https://github.com/rarecoil/hashes.org-list.git",
        "CustomURLs": ""
    }
    completions = list(parameters.keys())

    def do_execute(self, line):
        """Execute current module"""

        if self.validate_options() == False:
            return


    def validate_options(self):
        """Given a parsed collection of options, performs various validation checks."""

        wordlist = self.parameters.get("wordlist", "").strip('"')
        if wordlist == "":
            self.cp.error(text=f"The full path of the password file cannot be empty.")
            return False

        if int(self.parameters["maxlength"]) < int(self.parameters["minlength"]):
            self.cp.error(text=f"Warning: maximum word length less than minimum.")
            return False
        return True
    
    def locate_wordfile(self, wordfile=None):
        """
        Locates or creates a wordfile. If `wordfile` is None, creates 'wordlist.txt' 
        in the 'wordlist' folder under the current working directory. 
        If `wordfile` is a full path, it ensures the file exists, creating it if necessary.
        
        Parameters:
            wordfile (str): The full path of the wordfile. If None, a default 'wordlist.txt' is created.
            
        Returns:
            str: The path to the located or created wordfile.
        """

        if wordfile is None:
            folder = os.path.join(os.getcwd(), DEFAULT_FOLDER)
            if not os.path.exists(folder):
                os.makedirs(folder)
            wordfile = os.path.join(folder, "wordlist.txt")
        elif not os.path.isabs(wordfile):
            folder = os.path.join(os.getcwd(), DEFAULT_FOLDER)
            if not os.path.exists(folder):
                os.makedirs(folder)
            wordfile = os.path.join(folder, wordfile)

        if not os.path.exists(wordfile):
            with open(wordfile, 'w') as f:
                f.write("")
            self.cp.info(f"File '{wordfile}' has been created.")
        else:
            self.cp.warning(f"File '{wordfile}' already exists.")
        
        return wordfile
