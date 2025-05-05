import subprocess
from .conjure_cache import Cache
from os.path import join
from os import listdir
import json

MODEL = 'EssenceModel.essence'
INSTANCE = 'EssenceInstance.json'
SOLUTION_DIR = "ConjureSolution"

class Conjure:
    def __init__(self, **kwargs):
        self.cache = Cache(cache_dir= kwargs['cache_dir'] if 'cache_dir' in kwargs else None)

    def solve(self, model:str, parameter:str|None=None, *args) -> list[dict]:
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

    def get_model_parameters(self, model:str) -> list[dict]:
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
        for file in listdir(join(self.cache.cache_dir, SOLUTION_DIR)):
            if "solutions.json" in file:
                f = open(join(self.cache.cache_dir, SOLUTION_DIR, file))
                solutions = json.load(f)
                f.close()
                return solutions
        raise Exception("Solution not found")

    def pretty_print(self, code: str, output_type: str) -> str:
        self.cache.empty()

        self.cache.create_file(MODEL, code)
        shell_output = subprocess.run(["conjure", "pretty", f"--output-format={output_type}", join(self.cache.cache_dir, MODEL)], 
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if shell_output.returncode != 0:
            raise Exception(shell_output.stderr.decode('utf-8'))
        return shell_output.stdout.decode('utf-8')

    @staticmethod
    def available() -> bool:
        try:
            shell_out = subprocess.run(["conjure", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return_code = shell_out.returncode
            return return_code == 0
        except:
            return False

def is_conjure_available() -> bool:
    return Conjure.available()
