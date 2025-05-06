import subprocess
from .conjure_cache import Cache
from os.path import join
from os import listdir
import json

MODEL = 'EssenceModel.essence'
INSTANCE = 'EssenceInstance.json'
SOLUTION_DIR = "ConjureSolution"

class Conjure:
    """
    Main class for interacting with Conjure.

    Args:
        **kwargs: Optional keyword arguments
            cache_dir (str): Custom cache directory path
    """
    def __init__(self, **kwargs):
        """
        Initialize the Conjure instance with optional cache directory.

        Args:
            **kwargs: Optional keyword arguments
                cache_dir (str): Custom cache directory path
        """
        self.cache = Cache(cache_dir= kwargs['cache_dir'] if 'cache_dir' in kwargs else None)

    def solve(self, model:str, parameter:str|None=None, *args) -> list[dict]:
        """
        Solve a constraint problem using Conjure.

        Args:
            model (str): Essence model string
            parameter (str, optional): Essence instance parameters
            *args: Additional arguments to pass to Conjure

        Returns:
            list[dict]: List of solution dictionaries

        Raises:
            Exception: If Conjure execution fails
        """
        self.cache.empty()
        self.cache.create_file(MODEL, model)
        model_file = join(self.cache.cache_dir, MODEL)
        if parameter is not None:
            self.cache.create_file(INSTANCE, parameter)
            instance_file = join(self.cache.cache_dir, INSTANCE)
            cmd = ['conjure', 
                   'solve', 
                   model_file, 
                   instance_file, 
                   '--output-format=json', 
                   '--solutions-in-one-file', 
                   f'--output-directory={join(self.cache.cache_dir, SOLUTION_DIR)}']
        else:
            cmd = ['conjure', 
                   'solve', 
                   model_file, 
                   '--output-format=json', 
                   '--solutions-in-one-file', 
                   f'--output-directory={join(self.cache.cache_dir, SOLUTION_DIR)}']

        for arg in args:
            cmd.append(str(arg))

        output = subprocess.run(" ".join(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if output.returncode != 0:
            raise Exception(output.stderr.decode('utf-8'))
        return self.__load_solution()

    def get_model_parameters(self, model: str) -> list[dict]:
        """
        Get parameters from an Essence model.

        Args:
            model (str): Essence model string

        Returns:
            list[dict]: List of parameter declarations

        Raises:
            Exception: If Conjure execution fails
        """
        self.cache.empty()
        self.cache.create_file(MODEL, model)
        model_file = join(self.cache.cache_dir, MODEL)
        cmd = ['conjure', 
               'ide', 
               '--dump-declarations',
               model_file]

        output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if output.returncode != 0:
            raise Exception(output.stderr.decode('utf-8'))
        return json.loads(output.stdout.decode('utf-8'))

    def __load_solution(self) -> list[dict]:
        """
        Load and return solutions from the solution directory.

        Returns:
            list[dict]: List of solution dictionaries

        Raises:
            Exception: If solution file is not found
        """
        for file in listdir(join(self.cache.cache_dir, SOLUTION_DIR)):
            if "solutions.json" in file:
                f = open(join(self.cache.cache_dir, SOLUTION_DIR, file))
                solutions = json.load(f)
                f.close()
                return solutions
        raise Exception("Solution not found")

    def pretty_print(self, code:str, output_type:str) -> str:
        """
        Pretty print Essence code in specified format.

        Args:
            code (str): Essence code to format
            output_type (str): Desired output format

        Returns:
            str: Formatted Essence code

        Raises:
            Exception: If Conjure execution fails
        """
        self.cache.empty()

        self.cache.create_file(MODEL, code)
        shell_output = subprocess.run(["conjure", "pretty", f"--output-format={output_type}", join(self.cache.cache_dir, MODEL)], 
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if shell_output.returncode != 0:
            raise Exception(shell_output.stderr.decode('utf-8'))
        return shell_output.stdout.decode('utf-8')

    def get_infos(self) -> dict:
        """
        Get information about the solution from .eprime-info file.

        Returns:
            dict: Dictionary containing solution information

        Raises:
            Exception: If info file is not found or reading fails
        """
        try:
            for file in listdir(join(self.cache.cache_dir, SOLUTION_DIR)):
                if file.endswith(".eprime-info"):
                    f = open(join(self.cache.cache_dir, SOLUTION_DIR, file))
                    info_file_content = f.read()
                    f.close()
                    info = {}
                    for info_line in info_file_content.splitlines():
                        k_v_pair = info_line.split(':')
                        info[k_v_pair[0].strip()] = k_v_pair[1].strip()
                    return info
            raise Exception("info file not found")
        except Exception as e:
            raise Exception(f"issue reading info file: {e}")

    @staticmethod
    def available() -> bool:
        """
        Check if Conjure is available on the system.

        Returns:
            bool: True if Conjure is available, False otherwise
        """
        try:
            shell_out = subprocess.run(["conjure", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return_code = shell_out.returncode
            return return_code == 0
        except:
            return False

def is_conjure_available() -> bool:
    """
    Check if Conjure is available on the system.

    Returns:
        bool: True if Conjure is available, False otherwise
    """
    return Conjure.available()