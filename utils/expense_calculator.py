class Calculator:
    @staticmethod
    def multiply(a, b):
        """
        Multiply two numbers. Accepts ints, floats, or numeric strings.

        Args:
            a: The first number or numeric string.
            b: The second number or numeric string.

        Returns:
            float: The product of a and b.
        """
        try:
            a_num = float(a)
            b_num = float(b)
        except Exception:
            raise TypeError("Both operands must be numbers or numeric strings")
        return a_num * b_num
    
    @staticmethod
    def calculate_total(*x: float) -> float:
        """
        Calculate sum of the given list of numbers

        Args:
            x (list): List of floating numbers

        Returns:
            float: The sum of numbers in the list x
        """
        return sum(x)
    
    @staticmethod
    def calculate_daily_budget(total: float, days: int) -> float:
        """
        Calculate daily budget

        Args:
            total (float): Total cost.
            days (int): Total number of days

        Returns:
            float: Expense for a single day
        """
        return total / days if days > 0 else 0
    
    
