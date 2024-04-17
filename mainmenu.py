import pandas as pd
class SeatBookingSystem:
    def __init__(self):
        self.data = {}
        self.columns = ['A', 'B', 'C', 'X', 'D', 'E', 'F']
        self.storage_space = ['D77', 'E77', 'F77', 'D78', 'E78', 'F78']
        self.total_seats = 6 * 80 - len(self.storage_space)
        self.checked = []
        self.booked = {}  # Dictionary to store booking reference and customer data
        self.cancelled = []
        self.create_seating_arrangement()

    def book_seat(self, seat_num):
        if seat_num in self.booked:
            return "Seat already booked"
        seat = list(seat_num)
        if len(seat) == 2:
            if seat[0].isalpha() and seat[1].isdigit():
                first = seat[0].upper()
                second = int(seat[1])
                if first in self.data.keys() and 1 <= second <= 80:
                    if self.data[first][second] == 'F':
                        booking_reference = generate_booking_reference()
                        self.data[first][second] = booking_reference
                        # Store booking reference and customer data
                        self.booked[seat_num] = {
                            "reference": booking_reference,
                            "passport_number": input("Enter passenger's passport number: "),
                            "first_name": input("Enter passenger's first name: "),
                            "last_name": input("Enter passenger's last name: "),
                            "row": first,
                            "column": second
                        }
                        return f"Seat {seat_num} booked successfully. Reference: {booking_reference}"
                    else:
                        return f"Seat {seat_num} is not available for booking"
        return "Invalid input for seat number"

    def free_seat(self, seat_num):
        if seat_num in self.booked:
            del self.booked[seat_num]  # Remove booking details
        seat = list(seat_num)
        if len(seat) == 2:
            if seat[0].isalpha() and seat[1].isdigit():
                first = seat[0].upper()
                second = int(seat[1])
                if first in self.data.keys() and 1 <= second <= 80:
                    if self.data[first][second] != 'X':
                        self.data[first][second] = 'F'
                        return f"Seat {seat_num} freed successfully"
                    else:
                        return f"Seat {seat_num} cannot be freed as it is an aisle seat"
        return "Invalid input for seat number"

    def create_seating_arrangement(self):
        for col in self.columns:
            temp = []
            for x in range(1, 81):
                if col == 'X':
                    temp.append('X')
                elif col+str(x) in self.storage_space:
                    temp.append('S')
                else:
                    temp.append('F')
            self.data[col] = temp

    def display_seating_arrangement(self):
        df = pd.DataFrame(self.data)
        df.index = df.index + 1
        print(df.transpose())

    def check_seat_availability(self, seat_num):
        if seat_num in self.checked:
            return "Seat already checked"
        seat = list(seat_num)
        if len(seat) == 2:
            if seat[0].isalpha() and seat[1].isdigit():
                first = seat[0].upper()
                second = int(seat[1])
                if first in self.data.keys() and 1 <= second <= 80:
                    self.checked.append(seat_num)
                    return self.data[first][second]
        return "Invalid input for seat number"

    def show_booking_state(self):
        print(f"Total seats: {self.total_seats}")
        print(f"Booked seats: {len(self.booked)}")
        print(f"Cancelled seats: {len(self.cancelled)}")
        print(f"Available seats: {self.total_seats - len(self.booked)}")
        print(f"Checked seats: {len(self.checked)}")

    def menu(self):
        while True:
            print("\nMenu:")
            print("1. Check availability of seat")
            print("2. Book a seat")
            print("3. Free a seat")
            print("4. Show booking state")
            print("5. Exit program")

            choice = input("Select an option: ")

            if choice == '1':
                seat_num = input("Enter seat number to check availability: ")
                print(self.check_seat_availability(seat_num))
            elif choice == '2':
                seat_num = input("Enter seat number to book: ")
                print(self.book_seat(seat_num))
            elif choice == '3':
                seat_num = input("Enter seat number to free: ")
                print(self.free_seat(seat_num))
            elif choice == '4':
                self.show_booking_state()
            elif choice == '5':
                print("Exiting program...")
                break
            else:
                print("Invalid choice. Please select again.")

if __name__ == "__main__":
    seat_booking_system = SeatBookingSystem()
    seat_booking_system.menu()