# Student class
class Student:
    def __init__(self, name, registration_number, gender, year, status="active"):
        self.name = name
        self.registration_number = registration_number
        self.gender = gender
        self.year = year
        self.status = status

        self.current_room = None
        self.previous_room = None
        self.assigned_before = False

        self.total_billed = 0.0
        self.total_paid = 0.0

    def is_cleared(self):
        return self.total_paid >= self.total_billed

    def outstanding_balance(self):
        return self.total_billed - self.total_paid

    def __str__(self):
        status_str = f"[{self.status.upper()}]"
        cleared_str = (
            "CLEARED"
            if self.is_cleared()
            else f"Owes KES {self.outstanding_balance():,.0f}"
        )
        return (
            f"{status_str} {self.name} ({self.registration_number}) |"
            f"{self.gender} | Year {self.year} | {cleared_str}"
        )

