import pandas as pd
from booking_reference import generate_booking_reference


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

    def create_seating_arrangement(self):
        for col in self.columns:
            temp = []
            for x in range(1, 81):
                if col == 'X':
                    temp.append('X')
                elif col + str(x) in self.storage_space:
                    temp.append('S')
                else:
                    temp.append('F')
            self.data[col] = temp

    def choice1(self):
        answer = input("Enter a seat number to check availability (e.g. A9): ")
        check = self.check_seat(answer)
        if answer not in self.checked:
            self.checked.append(answer)
        if check == "F":
            print(f"The seat {answer} is available")
        elif check == "invalid":
            print("Invalid input for seat number. Please enter a valid seat number (e.g., A1).")
        else:
            print(f"Sorry, the seat {answer} is not available")

    def check_seat(self, seat_num):
        if self.display_seat(seat_num):
            first, second = self.display_seat(seat_num)
            return self.data[first][second-1]
        return "invalid"

    def display_seat(self, seat_num):
        seat = list(seat_num)
        letter, number = None, 0
        if len(seat) == 2:
            if seat[0].isalpha() and seat[1].isdigit():
                letter = seat[0].upper()
                number = int(seat[1])
        elif len(seat) == 3:
            if seat[0].isalpha() and seat[1].isdigit() and seat[2].isdigit():
                letter = seat[0].upper()
                number = int(seat[1] + seat[2])
        if letter in self.data.keys() and 1 <= number <= 80:
            return letter, number

    def choice2(self):
        answer = input("Enter a seat number to book (e.g. A9): ")
        check = self.check_seat(answer)
        if check == "F":
            print(self.book_seat(answer))
        elif check == "invalid":
            print("Invalid input for seat number. Please enter a valid seat number (e.g., A1).")
        else:
            print(f"Sorry, the seat {answer} is not available")

    def book_seat(self, seat_num):
        if seat_num in self.booked:
            return "Seat already booked"
        letter, number = self.display_seat(seat_num)
        if self.data[letter][number-1] == 'F':
            booking_reference = generate_booking_reference(self.booked)
            self.data[letter][number-1] = booking_reference
            # Store booking reference and customer data
            self.booked[seat_num] = {
                "reference": booking_reference,
                "passport_number": input("Enter passenger's passport number: "),
                "first_name": input("Enter passenger's first name: "),
                "last_name": input("Enter passenger's last name: "),
                "row": number,
                "column": letter
            }
            return f"Seat {seat_num} booked successfully. Reference: {booking_reference}"
        else:
            return f"Seat {seat_num} is not available for booking"

    def choice3(self):
        answer = input("Enter a seat number to cancel (e.g. A9): ")
        check = self.check_seat(answer)
        if check == "F" or check == "S" or check == "X":
            print(f"Sorry the seat {answer} is not booked and can't be cancelled")
        elif check == "invalid":
            print("Invalid input for seat number. Please enter a valid seat number (e.g., A1).")
        else:
            print(self.free_seat(answer))
            self.cancelled.append(answer)

    def free_seat(self, seat_num):
        if seat_num in self.booked:
            del self.booked[seat_num]  # Remove booking details
        letter, number = self.display_seat(seat_num)
        self.data[letter][number-1] = 'F'
        return f"Seat {seat_num} cancelled successfully"

    def show_booking_state(self):
        df = pd.DataFrame(self.data)  # Dataframing it so
        df.index = df.index + 1
        print(df.transpose())
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
                self.choice1()
            elif choice == '2':
                self.choice2()
            elif choice == '3':
                self.choice3()
            elif choice == '4':
                self.show_booking_state()
            elif choice == '5':
                print("Thank you for choosing Apache airlines...✈️")
                break
            else:
                print("Invalid choice. Please select from 1 to 5.")


if __name__ == "__main__":
    seat_booking_system = SeatBookingSystem()
    seat_booking_system.menu()
