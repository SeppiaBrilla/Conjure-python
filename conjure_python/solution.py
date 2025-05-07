from typing import Any, Literal
from .essence_types import EssenceType

SAT = "SAT"
UNSAT = "UNSAT"

class EssenceSolution:
    """
    Class representing a solution to an Essence problem.

    Args:
        raw_solutions (list[dict]): Raw (in basic dict format) solutions from Conjure
        python_solution (list[dict[str,EssenceType]]): Solutions converted to EssenceType python objects
        mode (Literal["raw", "python"]) : Mode for accessing solutions
    """
    def __init__(self, raw_solutions:list[dict], python_solution:list[dict[str,EssenceType]], mode:Literal["raw", "python"]="python") -> None:
        """
        Initialize the EssenceSolution instance.

        Args:
            raw_solutions (list[dict]): Raw (in basic dict format) solutions from Conjure
            python_solution (list[dict[str,EssenceType]]): Solutions converted to EssenceType python objects
            mode (Literal["raw", "python"]) : Mode for accessing solutions
        """
        self.raw = raw_solutions
        self.python_solution = python_solution
        self.state = SAT if len(raw_solutions) > 0 else UNSAT
        self.__mode = mode
        self.__current_idx = 0

    def __getitem__(self, idx:tuple[int,str]|int) -> dict|EssenceType|Any:
        """
        Get solution item by index or key.

        Args:
            idx (tuple[int, str] | int): Index or (index, key) tuple

        Returns:
            dict | EssenceType | Any: Solution item

        Raises:
            AssertionError: If idx is not tuple or int
        """
        if type(idx) == int:
            return self.raw[idx] if self.__mode == "raw" else self.python_solution[idx]
        assert isinstance(idx, tuple), f'expected tuple or int, got {type(idx)}'
        return self.raw[idx[0]][idx[1]] if self.__mode == "raw" else self.python_solution[idx[0]][idx[1]]

    def set_mode(self, new_mode: Literal["raw", "python"]) -> None:
        """
        Set the access mode for solutions.

        Args:
            new_mode (Literal["raw", "python"]): New mode

        Raises:
            AssertionError: If mode is not 'raw' or 'python'
        """
        assert new_mode in ["raw", "python"], f"supported modes are 'raw' and 'python'. Got {new_mode}"
        self.__mode = new_mode

    def get_mode(self) -> str:
        """
        Get the current access mode.

        Returns:
            str: Current mode ('raw' or 'python')
        """
        return self.__mode

    def __iter__(self):
        """
        Initialize iteration over solutions.

        Returns:
            EssenceSolution: Self instance
        """
        self.__current_idx = 0
        return self

    def __next__(self):
        """
        Get next solution in iteration.

        Returns:
            dict | dict[str, EssenceType]: Next solution

        Raises:
            StopIteration: When no more solutions are available
        """
        if self.__current_idx >= len(self):
            raise StopIteration
        elem = self[self.__current_idx]
        self.__current_idx += 1
        return elem

    def __len__(self):
        """
        Get number of solutions.

        Returns:
            int: Number of solutions
        """
        return len(self.python_solution)

    def __str__(self) -> str:
        """
        Get string representation of solutions. UNSAT if no solutions are available.

        Returns:
            str: Formatted string of solutions
        """
        if self.state == UNSAT:
            return UNSAT
        chosen_version = self.python_solution if self.__mode == "python" else self.raw
        solution_strs = []
        for i, solution in enumerate(chosen_version):
            sol_str = '\n'.join([f'{k} : {v}' for k,v in solution.items()])
            solution_strs.append(f"solution {i}: \n {sol_str}")
        return "\n".join(solution_strs)
    
    def __dict__(self):
        return self.raw