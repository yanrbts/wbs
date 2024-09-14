import argparse
import math
import os
import os.path
import random
import re
import sys
import git
import requests
from io import open
from websploit.core import base

DEFAULT_FOLDER = "wordlist"

class Main(base.Module):
    """Password Generation"""
    
    parameters = {
        "link_file": "",  # Path to the txt file containing download links
        "download_dir": "wordlists"  # Directory where downloads will be saved
    }
    completions = list(parameters.keys())

    def do_execute(self, line):
        """Execute current module"""

        link_file = self.parameters.get("link_file", "").strip()
        download_dir = os.path.join(os.getcwd(), self.parameters.get("download_dir", "wordlists"))

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        if not link_file:
            self.cp.warning(text="No link file provided.")
            return
        
        if not os.path.exists(link_file):
            self.cp.warning(text=f"Link file not found: {link_file}")
            return
        
        # Read the link file and process each link
        with open(link_file, 'r') as f:
            links = f.readlines()
        
        for link in links:
            link = link.strip()
            if not link:
                continue

            if link.endswith(".git"):
                self.cp.info(text=f"Cloning Git repository from {link}...")

                try:
                    repo_name = os.path.basename(link).replace('.git', '')
                    target_dir = os.path.join(download_dir, repo_name)
                    if not os.path.exists(target_dir):
                        try:
                            # Attempt to clone the repository
                            git.Repo.clone_from(link, target_dir, progress=self.show_progress)
                            self.cp.success(text=f"{repo_name} downloaded successfully!")
                        except git.exc.GitCommandError as e:
                            # Handle Git-specific errors
                            self.cp.error(text=f"Git command failed while cloning {repo_name}: {e}")
                        except Exception as e:
                            # Handle other potential errors
                            self.cp.error(text=f"Failed to clone {repo_name}: {e}")
                    else:
                        self.cp.info(text=f"{repo_name} already exists, skipping download.")
                except Exception as e:
                    self.cp.error(text=f"Unexpected error while processing {repo_name}: {e}")
            else:
                self.cp.info(text=f"Downloading file from {link}...")
                try:
                    file_name = os.path.basename(link)
                    target_path = os.path.join(download_dir, file_name)
                    response = requests.get(link, stream=True)
                    response.raise_for_status()
                    
                    with open(target_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    self.cp.success(text=f"{file_name} downloaded successfully!")
                except requests.RequestException as e:
                    self.cp.error(text=f"Failed to download file from {link}: {e}")

        # end
        # download_dir = os.path.join(os.getcwd(), "wordlists")

        # if not os.path.exists(download_dir):
        #     os.makedirs(download_dir)

        # for key, repo_url in self.parameters.items():
        #     if repo_url:
        #         self.cp.info(text=f"Downloading {key} from {repo_url}...")

        #         try:
        #             target_dir = os.path.join(download_dir, key)
        #             if not os.path.exists(target_dir):
        #                 try:
        #                     # Attempt to clone the repository
        #                     git.Repo.clone_from(repo_url, target_dir, progress=self.show_progress)

        #                     self.cp.success(text=f"{key} downloaded successfully!")
        #                 except git.exc.GitCommandError as e:
        #                     # Handle Git-specific errors
        #                     self.cp.error(text=f"Git command failed while downloading {key}: {e}")
        #                 except Exception as e:
        #                     # Handle other potential errors
        #                     self.cp.error(text=f"Failed to download {key}: {e}")
        #             else:
        #                 self.cp.info(text=f"{key} already exists, skipping download.")
        #         except Exception as e:
        #             self.cp.error(text=f"Unexpected error while processing {key}: {e}")
        #     else:
        #         self.cp.warning(text=f"Skipping {key}, no URL provided.")
    
    
    def show_progress(self, op_code, cur_count, max_count=None, message=''):
        """Progress callback function"""
        if max_count:
            percent = (cur_count / max_count) * 100
            # self.cp.info(text=f'Progress: {percent:.2f}% ({cur_count}/{max_count})')
            print(f'\r\033[34;m[𝓲]\033[0m \033[1;96mProgress: {percent:.2f}% ({cur_count}/{max_count})\033[0m', end='', flush=True)

            if cur_count >= max_count:
                print()
        else:
            # self.cp.info(text=f'Progress: {cur_count} objects transferred')
            print(f'\r\033[34;m[𝓲] \033[0m\033[1;96mProgress: {cur_count} objects transferred\033[0m', end='', flush=True)
            print()
    
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
