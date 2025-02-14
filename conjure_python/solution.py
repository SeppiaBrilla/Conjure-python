from typing import Any, Literal
from .essenceTypes import EssenceType

SAT = "SAT"
UNSAT = "UNSAT"

class EssenceSolution:
    def __init__(self, raw_solutions: list[dict], python_solution:list[dict[str,EssenceType]], mode:Literal["raw", "python"]="python") -> None:
        self.raw = raw_solutions
        self.python_solution = python_solution
        self.state = SAT if len(raw_solutions) > 0 else UNSAT
        self.__mode = mode
        self.__current_idx = 0

    def __getitem__(self, idx:tuple[int,str]|int) -> dict|EssenceType|Any:
        if type(idx) == int:
            return self.raw[idx] if self.__mode == "raw" else self.python_solution[idx]
        assert isinstance(idx, tuple), f'expected tuple or int, got {type(idx)}'
        return self.raw[idx[0]][idx[1]] if self.__mode == "raw" else self.python_solution[idx[0]][idx[1]]

    def set_mode(self, new_mode:Literal["raw", "python"]) -> None:
        assert new_mode in ["raw", "python"], f"supported modes are 'raw' and 'python'. Got {new_mode}"
        self.__mode = new_mode

    def get_mode(self) -> str:
        return self.__mode

    def __iter__(self):
        self.__current_idx = 0
        return self

    def __next__(self):
        elem = self[self.__current_idx]
        self.__current_idx += 1
        return elem
    def __str__(self) -> str:
        if self.state == UNSAT:
            return UNSAT
        chosen_version = self.python_solution if self.__mode == "python" else self.raw
        solution_strs = []
        for i, solution in enumerate(chosen_version):
            sol_str = '\n'.join([f'{k} : {v}' for k,v in solution.items()])
            solution_strs.append(f"solution {i}: \n {sol_str}")
        return "\n".join(solution_strs)
