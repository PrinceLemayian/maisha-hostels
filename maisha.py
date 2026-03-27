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


class Hostel:
    def __init__(self, name):
        self.name = name
        self.rooms = {}
        self.students = {}

    def add_room(self, room):
        self.rooms[room.room_number] = room

    def add_student(self, student):
        self.students[student.registration_number] = student

    def get_room(self, room_number):
        return self.rooms.get(room_number)

    def get_student(self, registration_number):
        return self.students.get(registration_number)

    # Rent calculations

    def calculate_charges(self, student, room):
        charges = {}

        # Security deposit for only first room assignment

        if not student.assigned_before:
            charges["Security Deposit"] = 3000

        # Caution fee for every time a student moves to a different room

        if student.previous_room is None or student.previous_room != room:
            charges["Caution Fee"] = 500

        # Fixed charges every semester

        charges["Utility Levy"] = 1500
        charges["Amenity Fee"] = 800

        # Room rent
        # Adding the student temporarily to get the correct rent split
        room.occupants.append(student)
        charges["Room Rent"] = room.rent_per_student()

        # Bill the student
        total = sum(charges.values())
        student.total_billed += total

        return charges

        # Room assignment

    def assign_room(self, student, room):

        # Check status of student
        if student.status == "suspended":
            return (
                False,
                f"Rejected: {student.name} has been suspended hence cannot be allocated a room.",
                None,
            )

        if student.status == "graduated":
            return (
                False,
                f"Rejected: {student.name} has graduated hence cannot be allocated a room.",
                None,
            )

        # Check if student already has a room
        if student.current_room is not None:
            return (
                False,
                f"Rejected: {student.name} has already occupied a room. Vacate first.",
                None,
            )

        # Check if room is decommissioned
        if room.is_decommissioned:
            return (
                False,
                f"Rejected: Room {room.room_number} has been decommissioned.",
                None,
            )

        # Check gender policy
        if room.allowed_gender() != student.gender:
            return (
                False,
                f"Rejected: Floor {room.floor} is for {room.allowed_gender()} only.",
                None,
            )

        # Check if room is full
        if room.is_full():
            return (
                False,
                f"Rejected: Room {room.room_number} is full (maximum 2 occupants).",
                None,
            )

        # Check if genders match
        if room.has_occupant() and room.existing_occupant_gender() != student.gender:
            return (
                False,
                f"Rejected: Room {room.room_number} already has a {room.existing_occupant_gender()} occupant. {student.name} is {student.gender}.",
                None,
            )

        # After all checks pass (calculate charges and append student to room)
        charges = self.calculate_charges(student, room)

        # Update the state of the student
        student.current_room = room
        student.previous_room = room
        student.assigned_before = True

        return (
            True,
            f"Success: {student.name} assigned to Room {room.room_number}.",
            charges,
        )

    # Online booking by student
    def book_room(self, student, room):
        print(f"\n | ONLINE BOOKING | {student.name}: Room {room.room_number}")
        success, message, charges = self.assign_room(student, room)
        print(message)
        if success and charges:
            self.print_charges(charges)
        return success

    # Manual allocation by warden
    def allocate_room(self, student, room):
        print(f"\n | WARDEN ASSIGNMENT | {student.name}: Room {room.room_number}")
        success, message, charges = self.assign_room(student, room)
        print(message)
        if success and charges:
            self.print_charges(charges)
        return success

    def vacate_room(self, student):
        # Remove a student from the current room
        if student.current_room is None:
            print(f"\n{student.name} is not currently assigned to any room.")
            return False

        room = student.current_room

        # Remove student from room
        room.occupants.remove(student)
        student.current_room = None

        print(f"\n | VACATE | {student.name} has vacated Room {room.room_number}.")

        # Recalculate rent after one student leaves
        if len(room.occupants) == 1:
            remaining = room.occupants[0]
            remaining.total_billed += 5000
            print(
                f"{student.name} is the only occupant of Room {room.room_number} hence rent is recalculated to KES 10,000."
            )

        print(f"Room {room.room_number} is now: {room.status().upper()}")
        return True

    # Payments

    def record_payment(self, student, amount):
        student.total_paid += amount
        print(
            f"| PAYMENT | KES {amount:,} recorded for {student.name}. Outstanding balance is KES {student.outstanding_balance():,.0f}"
        )

    # Decommissioning

    def decommission_room(self, room):
        print(f"Decommission Room {room.room_number}")

        displaced = list(room.occupants)
        for student in displaced:
            room.occupants.remove(student)
            student.current_room = None
            print(f"{student.name} is now displaced, kindly reaallocate a room.")

        room.is_decommissioned = True
        print(f"Room {room.room_number} is now decommissioned.")

    def print_charges(self, charges):
        print("==| CHARGES |==")
        for item, amount in charges.items():
            print(f"{item:} KES {amount:,}")
            print(f"{'Total':} KES {sum(charges.values()):,}")
