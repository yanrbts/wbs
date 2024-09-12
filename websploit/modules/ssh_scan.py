import asyncio
import asyncssh
from datetime import datetime
from os import path
from websploit.core import base
from websploit.core.utils import CPrint


class Main(base.Module):
    """SSH Brute Force"""

    parameters = {
        "username": "root",
        "password": "root",
        "userfile": "",
        "passfile": ""
    }
    completions = list(parameters.keys())

    def do_execute(self, line):
        """Execute current module"""
        
        tasks = []
        pwds = []
        users = []
        found_flag = asyncio.Event()
        concurrency_limit = 10
        counter = 0
        
        username = self.parameters.get("username", "").strip('"')
        if username:
            self.cp.info(text=f"SSH Username ({username})")
        else:
            userfile = self.parameters.get("userfile", "")
            if userfile == "":
                self.cp.warning(text=f"SSH cracking requires setting a username or username storage file")
                return
            with open(userfile, 'r') as f:
                for user in f.readlines():
                    user = user.strip()
                    users.append(user)

        