from typing import Any, Literal
from essenceTypes import EssenceType

SAT = "SAT"
UNSAT = "UNSAT"

class EssenceSolution:
    def __init__(self, raw_solutions: list[dict], python_solution:list[dict[str,EssenceType]], mode:Literal["raw", "python"]="python") -> None:
        self.raw = raw_solutions
        self.python_solution = python_solution
        self.state = SAT if len(raw_solutions) > 0 else UNSAT
        self.mode = mode

    def __call__(self, idx:tuple[int,str]|int) -> dict|EssenceType|Any:
        if type(idx) == int:
            return self.raw[idx] if self.mode == "raw" else self.python_solution[idx]
        assert isinstance(idx, tuple), f'expected tuple or int, got {type(idx)}'
        return self.raw[idx[0]][idx[1]] if self.mode == "raw" else self.python_solution[idx[0]][idx[1]]

    def update_mode(self, new_mode:Literal["raw", "python"]) -> None:
        self.mode = new_mode

    def __str__(self) -> str:
        if self.state == UNSAT:
            return UNSAT
        chosen_version = self.python_solution if self.mode == "python" else self.raw
        solution_strs = []
        for i, solution in enumerate(chosen_version):
            sol_str = '\n'.join([f'{k} : {v}' for k,v in solution.items()])
            solution_strs.append(f"solution {i}: \n {sol_str}")
        return "\n".join(solution_strs)
