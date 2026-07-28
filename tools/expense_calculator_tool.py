from utils.expense_calculator import Calculator
from typing import List
from langchain.tools import tool

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""
        @tool
        def estimate_total_hotel_cost(price_per_night: str, total_days) -> float:
            """Calculate total hotel cost. Accepts numeric strings or numbers."""
            try:
                price = float(price_per_night)
            except Exception:
                raise ValueError("price_per_night must be a number or numeric string")
            try:
                days = float(total_days)
            except Exception:
                raise ValueError("total_days must be a number")
            return self.calculator.multiply(price, days)
        
        @tool
        def calculate_total_expense(*args, **kwargs) -> float:
            """Calculate total expense of the trip.

            Accepts either positional numeric args, a single `costs` list/tuple,
            or a comma-separated string of numbers in the `costs` keyword.
            """
            # Determine costs from kwargs or positional args
            if "costs" in kwargs:
                costs_raw = kwargs["costs"]
                if isinstance(costs_raw, str):
                    # parse comma-separated numbers
                    parts = [p.strip() for p in costs_raw.split(",") if p.strip()]
                    costs = []
                    for p in parts:
                        try:
                            costs.append(float(p))
                        except Exception:
                            raise ValueError(f"Invalid numeric value in costs: '{p}'")
                elif isinstance(costs_raw, (list, tuple)):
                    costs = []
                    for v in costs_raw:
                        try:
                            costs.append(float(v))
                        except Exception:
                            raise ValueError(f"Invalid numeric value in costs: '{v}'")
                else:
                    # single numeric value
                    try:
                        costs = [float(costs_raw)]
                    except Exception:
                        raise ValueError("`costs` must be a list, tuple, number, or comma-separated string")
            else:
                # positional args
                costs = []
                for v in args:
                    try:
                        costs.append(float(v))
                    except Exception:
                        raise ValueError(f"Invalid numeric value: '{v}'")

            return self.calculator.calculate_total(*costs)
        
        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """Calculate daily expense"""
            return self.calculator.calculate_daily_budget(total_cost, days)
        
        return [estimate_total_hotel_cost, calculate_total_expense, calculate_daily_expense_budget]