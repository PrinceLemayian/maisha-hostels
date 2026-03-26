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


# Room class
class Room:
    def __init__(self, room_number, floor):
        self.room_number = room_number
        self.floor = floor
        self.occupants = []
        self.is_decommissioned = False

    def allowed_gender(self):
        if self.floor == 1:
            return "male"
        elif self.floor in (2, 3):
            return "female"
        return None

    def status(self):
        if self.is_decommissioned:
            return "Room is decommissioned"
        count = len(self.occupants)
        if count == 0:
            return "Room is vacant"
        elif count == 1:
            return "Room is partially occupied"
        else:
            return "Room is full"

    def rent_per_student(self):
        count = len(self.occupants)
        if count == 0:
            return 0
        elif count == 1:
            return 10000
        else:
            return 5000

    def is_full(self):
        return len(self.occupants) >= 2

    def has_occupant(self):
        return len(self.occupants) > 0

    def existing_occupant_gender(self):
        if self.occupants:
            return self.occupants[0].gender
        return None

    def __str__(self):
        occupant_names = (
            ", ".join(occupant.name for occupant in self.occupants)
            if self.occupants
            else "none"
        )
        return (
            f"Room {self.room_number} | Floor {self.floor} | "
            f"{self.status().upper()} | Occupants: {occupant_names} |"
            f"Rent per student: KES {self.rent_per_student():,}"
        )
