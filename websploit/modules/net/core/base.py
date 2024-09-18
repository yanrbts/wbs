import json
import sys
import yaml
from websploit.modules.net.config import version_info, Config
from websploit.modules.net.core.ip import (
    is_single_ipv4,
    is_single_ipv6,
    is_ipv4_cidr,
    is_ipv6_range,
    is_ipv6_cidr,
    is_ipv4_range,
    generate_ip_range,
)
from websploit.core.utils import CPrint
from .utils import common as utils
from .templates import TemplateLoader



class Base:
    cp = CPrint()

    def __init__(self) -> None:
        self.graphs = self.load_graphs()
        
        self.modules = self.load_modules(full_details=True)
        self.cp.info(text=f"loaded modules {len(self.modules)}")
    
    @staticmethod
    def load_graphs():
        """
        load all available graphs

        Returns:
            an array of graph names
        """

        graph_names = []
        for graph_library in Config.path.graph_dir.glob("*/engine.py"):
            graph_names.append(str(graph_library).split("/")[-2] + "_graph")
        return list(set(graph_names))
    
    @staticmethod
    def load_modules(limit=-1, full_details=False):
        """
        load all available modules

        limit: return limited number of modules
        full: with full details

        Returns:
            an array of all module names
        """
        # Search for Modules

        module_names = {}
        for module_name in sorted(Config.path.modules_dir.glob("**/*.yaml")):
            library = str(module_name).split("/")[-1].split(".")[0]
            category = str(module_name).split("/")[-2]
            module = f"{library}_{category}"
            contents = yaml.safe_load(TemplateLoader(module).open().split("payload:")[0])
            module_names[module] = contents["info"] if full_details else None

            if len(module_names) == limit:
                module_names["..."] = {}
                break
        module_names = utils.sort_dictionary(module_names)
        module_names["all"] = {}

        return module_names
    
    @staticmethod
    def load_profiles(limit=-1):
        """
        load all available profiles

        Returns:
            an array of all profile names
        """
        all_modules_with_details = Base.load_modules(full_details=True).copy()
        profiles = {}