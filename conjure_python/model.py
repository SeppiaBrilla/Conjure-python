import json
from copy import deepcopy
from typing import Any

from .conjure import Conjure
from .solution import EssenceSolution
from .essence_types import EssenceFunction, EssenceMatrix, EssenceRecord, EssenceRelation, EssenceType, EssenceTuple, EssenceSet, EssenceSequence, is_bool, is_function, is_int, is_matrix, is_record, is_relation, is_tuple, is_set, is_sequence

class EssenceModel:
    """
    Class representing an Essence model and its solver configuration.

    Args:
        model (str, optional): Initial Essence model string
        solver (str, optional): Solver name
        **kwargs: Additional arguments for Conjure initialization
    """
    def __init__(self, model:str="", solver:str|None=None, **kwargs) -> None:
        """
        Initialize the EssenceModel instance.

        Args:
            model (str, optional): Initial Essence model string
            solver (str, optional): Solver name
            **kwargs: Additional arguments for Conjure initialization
        """
        self.__model = model
        self.__solver = solver
        self.__time_limit = None
        self.__seed = None
        self.__threads = None
        self.__conjure = Conjure(**kwargs)
        assert self.__conjure.available(), "conjure not available, please install it"
        self.__params = {}

    def append(self, new_constraint:str) -> None:
        """
        Append a new constraint to the model.

        Args:
            new_constraint (str): New constraint to add
        """
        if self.__model != '':
            self.__model += '\n' + new_constraint
        else:
            self.__model = new_constraint

    def set_solver(self, solver_name:str) -> None:
        """
        Set the solver for the model.

        Args:
            solver_name (str): Name of the solver
        """
        self.__solver = solver_name

    def set_random_seed(self, random_seed:int) -> None:
        """
        Set the random seed for the solver.

        Args:
            random_seed (int): Random seed value
        """
        self.__seed = str(random_seed)

    def set_time_limit(self, time_limit:int) -> None:
        """
        Set the time limit for the solver.

        Args:
            time_limit (int): Time limit in seconds
        """
        self.__time_limit = time_limit
    
    def set_threads(self, threads:int) -> None:
        """
        Set the number of threads for the solver.

        Args:
            threads (int): Number of threads
        """
        self.__threads = str(threads)

    def clear_model(self) -> None:
        """
        Clear the current model string.
        """
        self.__model = ""

    def clear_parameters(self) -> None:
        """
        Clear all parameters.
        """
        self.__params = {}
    
    def clear(self) -> None:
        """
        Clear both model and parameters.
        """
        self.clear_model()
        self.clear_parameters()

    def add_parameters(self, name:str, value:Any) -> None:
        """
        Add a parameter to the model.

        Args:
            name (str): Parameter name
            value (Any): Parameter value
        """
        self.__params[name] = value

    def __get_essence_representation(self) -> tuple[list[dict], list[dict]]:
        essence_params = self.__conjure.get_model_parameters(self.__model)
        params, out = [], []
        for param in essence_params:
            if param['kind'] == "Given":
                params.append({'name': param['name'], 'domain': param['domain']})
            elif param['kind'] == "Find":
                out.append({'name': param['name'], 'domain': param['domain']})
        return params, out

    def solve(self, parameters:dict|None=None, solver_arguments:str|None=None) -> EssenceSolution:
        """
        Solve the model with given parameters and solver arguments. 
        if no parameters are given, the ones set in the model are used. if no solver arguments are given, the ones set in the model are used. 
        if no solver is set, the default solver is used.
        Args:
            parameters (dict, optional): Parameters for the model
            solver_arguments (str, optional): Additional solver arguments

        Returns:
            EssenceSolution: Solution object containing results

        Raises:
            Exception: If parameters are missing
        """
        params = self.__params if parameters is None else parameters
        essence_in, essence_out = self.__get_essence_representation()
        if not self.check_params(params, essence_in):
            raise Exception('missing parameters')
        if solver_arguments is None:
            solver_arguments = self.__build_solver_args()
        solver_args = []
        if self.__solver is not None:
            solver_args += [f"--solver={self.__solver}"]
        if solver_arguments != "":
            solver_args += [f'--solver-options="{solver_arguments}"']
        if len(params.keys()) > 0:
            raw_solution = self.__conjure.solve(self.__model, json.dumps(params), *solver_args)
            python_essence_solution = self.__build_essence_solution(raw_solution, (essence_in, essence_out))
            return EssenceSolution(raw_solution, python_essence_solution)
        raw_solution = self.__conjure.solve(self.__model, None, *solver_args)
        python_essence_solution = self.__build_essence_solution(raw_solution, (essence_in, essence_out))
        return EssenceSolution(raw_solution, python_essence_solution)

    def __build_solver_args(self) -> str:
        """
        Build solver-specific arguments string.

        Returns:
            str: Solver arguments string

        Raises:
            Exception: If invalid solver configuration is provided
        """
        if self.__time_limit is None and self.__threads is None and self.__seed is None:
            return ""
        if self.__solver is None:
            if self.__threads is not None:
                raise Exception("thread configuration not available for Minion solver")
            if self.__seed is not None:
                raise Exception("random seed configuration not available for Minion solver")
            solver_str = "" if self.__time_limit is None else f"-cpulimit {self.__time_limit} "
            return solver_str + "-varorder domoverwdeg -preprocess GAC"
        elif self.__solver == "chuffed":
            if self.__threads is not None:
                raise Exception("thread configuration not available for Chuffed solver")
            solver_str = "" if self.__time_limit is None else f"-t {self.__time_limit}000"
            solver_str += "" if self.__seed is None else f" --rnd-seed {self.__seed}"
            return solver_str if solver_str[0] != " " else solver_str[1:]
        elif self.__solver == "lingeling":
            if self.__threads is not None:
                raise Exception("thread configuration not available for Lingeling solver")
            solver_str = "" if self.__time_limit is None else f"-t {self.__time_limit}"
            solver_str += "" if self.__seed is None else f" --seed {self.__seed}"
            return solver_str if solver_str[0] != " " else solver_str[1:]
        elif self.__solver == "kissat":
            if self.__threads is not None:
                raise Exception("thread configuration not available for Kissat solver")
            solver_str = "" if self.__time_limit is None else f"--time={self.__time_limit}"
            solver_str += "" if self.__seed is None else f" --seed={self.__seed}"
            return solver_str if solver_str[0] != " " else solver_str[1:]
        elif self.__solver == "or-tools":
            solver_str =  "" if self.__time_limit is None else f"--time_limit={self.__time_limit}"
            solver_str += "" if self.__seed is None else f" --cp_random_seed {self.__seed} --fz_seed {self.__seed}"
            solver_str += "" if self.__threads is None else f" --threads={self.__threads}"
            return solver_str if solver_str[0] != " " else solver_str[1:]
        elif self.__solver == "cplex":
            if self.__threads is not None:
                raise Exception("thread configuration not available for Cplex solver")
            if self.__seed is not None:
                raise Exception("random seed configuration not available for Cplex solver")
            return "" if self.__time_limit is None else f"-time-limit {self.__time_limit}"
        else:
            if self.__time_limit is not None or self.__threads is not None or self.__seed is not None:
                raise Exception(f"cannot set solver arguments for unknown solver {self.__solver}")
            return ""

    def __build_essence_solution(self, solution:list[dict], essence_representation:tuple[list[dict], list[dict]]) -> list[dict[str, EssenceType]]:
        """
        Convert raw solution to Essence types.

        Args:
            solution (list[dict]): Raw solution data
            essence_representation (tuple): Tuple of input/output parameters

        Returns:
            list[dict[str, EssenceType]]: List of solutions with Essence types
        """
        essence_in, essence_out = essence_representation
        essence_out = deepcopy(essence_out)
        out_param_dict = {}
        for out_param in essence_out:
            for in_param in essence_in:
                if in_param['name'] in out_param['domain']:
                    if 'int' in in_param['domain'] or 'bool' in in_param['domain']:
                        out_param['domain'].replace(in_param['name'], in_param['domain'])
                        out_param['to_replace'] = False
                    else:
                        out_param['to_replace'] = True
            out_param_dict[out_param['name']] = out_param
        solutions = []
        for sol in solution:
            new_sol = {}
            for name in sol.keys():
                dom = out_param_dict[name]['domain']
                if is_matrix(dom):
                    new_sol[name] = EssenceMatrix(sol[name], dom)
                elif is_function(dom):
                    new_sol[name] = EssenceFunction(sol[name], dom)
                elif is_relation(dom):
                    new_sol[name] = EssenceRelation(sol[name], dom)
                elif is_tuple(dom):
                    new_sol[name] = EssenceTuple(sol[name], dom)
                elif is_record(dom):
                    new_sol[name] = EssenceRecord(sol[name], dom)
                elif is_int(dom):
                    new_sol[name] = int(sol[name])
                elif is_bool(dom):
                    new_sol[name] = bool(sol[name])
                elif is_set(dom):
                    new_sol[name] = EssenceSet(sol[name], dom)
                elif is_sequence(dom):
                    new_sol[name] = EssenceSequence(sol[name], dom)
                else:
                    new_sol[name] = sol[name]
            solutions.append(new_sol)
        return solutions

    def getStats(self) -> dict|None:
        try:
            stats = self.__conjure.get_infos()
            return stats
        except Exception as e:
            return None

    def check_params(self, params:dict, essence_params:list[dict]) -> bool:
        """
        Check if all required parameters are present.

        Args:
            params (dict): Provided parameters
            essence_params (list[dict]): Required parameters from model

        Returns:
            bool: True if all parameters are present, False otherwise
        """
        param_names = [p['name'] for p in essence_params]
        for p_name in param_names:
            if not p_name in params:
                return False
        return True

    def get_all_model_params(self, model:str="") -> list[dict]:
        return self.__conjure.get_model_parameters(model if model != "" else self.__model)
    
    def get_required_params(self, model:str="") -> list[str]:
        return self.__conjure.get_required_parameters(model if model != "" else self.__model)