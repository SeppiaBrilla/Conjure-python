import json
from copy import deepcopy
from typing import Any
from .conjure import Conjure
from .solution import EssenceSolution
from .essenceTypes import EssenceFunction, EssenceMatrix, EssenceType

class EssenceModel:
    def __init__(self, model:str="", raise_exceptions:bool=True, **kwargs) -> None:
        self.model = model
        self.raise_exceptions = raise_exceptions
        self.conjure = Conjure(raise_exceptions=raise_exceptions, **kwargs)
        assert self.conjure.available(), "conjure not available, please install it"
        self.params = {}

    def append(self, new_constraint:str) -> None:
        if self.model != '':
            self.model += '\n' + new_constraint
        else:
            self.model = new_constraint

    def clear_model(self) -> None:
        self.model = ""

    def clear_parameters(self) -> None:
        self.params = {}
    
    def clear(self) -> None:
        self.clear_model()
        self.clear_parameters()

    def add_parameters(self, name:str, value:Any) -> None:
        self.params[name] = value

    def __get_essence_representation(self) -> tuple[list[dict], list[dict]]:
        essence_params = self.conjure.get_model_parameters(self.model)
        params, out = [], []
        for param in essence_params:
            if param['kind'] == "Given":
                params.append({'name': param['name'], 'domain': param['domain']})
            else:
                assert param['kind'] == 'Find', f'Unknown parameter kind {param["kind"]}'
                out.append({'name': param['name'], 'domain': param['domain']})
        return params, out


    def solve(self, parameters:dict|None=None) -> EssenceSolution:
        params = self.params if parameters is None else parameters
        essence_in, essence_out = self.__get_essence_representation()
        if not self.check_params(params, essence_in):
            if self.raise_exceptions:
                raise Exception('missing parameters')
            return EssenceSolution([], [])
        if len(params.keys()) > 0:
            raw_solution = self.conjure.solve(self.model, json.dumps(params))
            python_essence_solution = self.__build_essence_solution(raw_solution, (essence_in, essence_out))
            return EssenceSolution(raw_solution, python_essence_solution)
        raw_solution = self.conjure.solve(self.model)
        python_essence_solution = self.__build_essence_solution(raw_solution, (essence_in, essence_out))
        return EssenceSolution(raw_solution, python_essence_solution)

    def __build_essence_solution(self, solution:list[dict], essence_representation:tuple[list[dict], list[dict]]) -> list[dict[str, EssenceType]]:
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
                if 'matrix' in dom:
                    new_sol[name] = EssenceMatrix(sol[name], dom)
                elif 'function' in dom:
                    new_sol[name] = EssenceFunction(sol[name], dom)
                elif 'int' in dom:
                    new_sol[name] = int(sol[name])
                elif 'bool' in dom:
                    new_sol[name] = bool(sol[name])
            solutions.append(new_sol)
        return solutions

    def check_params(self, params:dict, essence_params:list[dict]) -> bool:
        param_names = [p['name'] for p in essence_params]
        for p_name in param_names:
            if not p_name in params:
                return False
        return True

if __name__ == "__main__":
    print(EssenceModel(model="""language Essence 1.3
    given t : int(1..) $ strength (size of subset of rows)
    given k : int(1..) $ rows
    given g : int(2..) $ number of values
    given b : int(1..) $ columns
    where k>=t, b>=g**t
    find CA: matrix indexed by [int(1..k), int(1..b)] of int(1..g)
    such that
        forAll rows : sequence (size t) of int(1..k) .
            (forAll i : int(2..t) . rows(i-1) < rows(i)) ->
            forAll values : sequence (size t) of int(1..g) .
                exists column : int(1..b) .
                    forAll i : int(1..t) .
                        CA[rows(i), column] = values(i)

    such that forAll i : int(2..k) . CA[i-1,..] <=lex CA[i,..]
    such that forAll i : int(2..b) . CA[..,i-1] <=lex CA[..,i]
    """).solve({'t' : 3, 'g' : 2, 'k' : 4, 'b' : 8}))
#sat instance {'t' : 3, 'g' : 2, 'k' : 4, 'b' : 8}
#unsat instance {'t' : 3, 'g' : 2, 'k' : 5, 'b' : 8}
