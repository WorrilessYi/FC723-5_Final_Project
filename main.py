import pandas as pd
from booking_reference import generate_booking_reference


class SeatBookingSystem:
    def __init__(self):
        # Initialize data structures
        self.data = {}  # Dictionary to keep seat data
        self.columns = ['A', 'B', 'C', 'X', 'D', 'E', 'F']
        self.storage_space = ['D77', 'E77', 'F77', 'D78', 'E78', 'F78']  # List of storage space
        self.total_seats = 6 * 80 - len(self.storage_space)
        self.checked = []  # list to keep track of checked seats
        self.booked = {}  # Dictionary to store booking reference and customer data
        self.cancelled = []  # List of cancelled seats
        self.create_seating_arrangement()  # Create initial seating arrangement

    def create_seating_arrangement(self):
        """
        Creates initial seating arrangement in a dictionary by storing rows in column value
        """
        for col in self.columns:
            temp = []
            for x in range(1, 81):
                if col == 'X':
                    temp.append('X')  # aisle row
                elif col + str(x) in self.storage_space:
                    temp.append('S')  # Storage space
                else:
                    temp.append('F')  # free seats
            self.data[col] = temp  # add row by row

    def choice1(self):  #
        answer = input("Enter a seat number to check availability (e.g. A9): ")
        check = self.check_seat(answer)  # Check availability of the seat
        if answer not in self.checked:
            self.checked.append(answer)  # Add seat to checked list
        if check == "F":
            print(f"The seat {answer} is available")
        elif check == "invalid":
            print("Invalid input for seat number. Please enter a valid seat number (e.g., A1).")
        else:
            print(f"Sorry, the seat {answer} is not available")

    def check_seat(self, seat_num):
        """
        Checks if the seat is valid

        Returns:
        - Status of the seat (Free, Storage, Aisle, or Reference number)
        """
        if self.display_seat(seat_num):  # checking whether the input is legitimate
            letter, number = self.display_seat(seat_num)  # separating letter and number
            return self.data[letter][number-1]  # return the status
        else:
            return "invalid"  # input layout was wrong or out of range

    def display_seat(self, seat_num):
        """
        Separate the column letter and row number.

        Returns:
        - Column letter (string) and row number (int)
        """
        seat = list(seat_num)  # separating each characters
        letter, number = None, 0
        if len(seat) == 2:
            if seat[0].isalpha() and seat[1].isdigit():
                letter = seat[0].upper()  # Get row label
                number = int(seat[1])  # Get column number
        elif len(seat) == 3:
            if seat[0].isalpha() and seat[1].isdigit() and seat[2].isdigit():
                letter = seat[0].upper()
                number = int(seat[1] + seat[2])  # merging 2 digit number
        if letter in self.data.keys() and 1 <= number <= 80:  # making sure letter is in column and number in range
            return letter, number

    def choice2(self):
        answer = input("Enter a seat number to book (e.g. A9): ")
        if answer in self.booked:  # check if the seat is already booked
            return "Seat already booked"
        check = self.check_seat(answer)  # check the status of the given seat
        if check == "F":
            print(self.book_seat(answer))  # if the seat is free call booking function
        elif check == "invalid":
            print("Invalid input for seat number. Please enter a valid seat number (e.g., A1).")
        else:  # if not free or invalid seat, then it's booked, storage, or aisle seat.
            print(f"Sorry, the seat {answer} is not available")

    def book_seat(self, seat_num):
        """
        Book a seat.

        Returns:
        - Booking status message (string)
        """
        letter, number = self.display_seat(seat_num)
        if self.data[letter][number-1] == 'F':
            # Generate booking reference
            booking_reference = generate_booking_reference(list(self.booked.values()))
            self.data[letter][number-1] = booking_reference
            # Store booking reference and customer data
            self.booked[seat_num] = {
                "reference": booking_reference,
                "passport_number": input("Enter passport number: "),
                "first_name": input("Enter first name: "),
                "last_name": input("Enter last name: "),
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
        else:  # if not free, storage, aisle, or invalid must be booking reference
            print(self.free_seat(answer))
            self.cancelled.append(answer)

    def free_seat(self, seat_num):
        """
        Free a seat and deletes booking reference.

        Returns:
        - Cancelling status message (string)
        """
        if seat_num in self.booked:
            del self.booked[seat_num]  # Remove booking details
        letter, number = self.display_seat(seat_num)
        self.data[letter][number-1] = 'F'
        return f"Seat {seat_num} cancelled successfully"

    def show_booking_state(self):
        """
        Display the current booking state.

        This method prints the current seating arrangement along with the total number of seats,
        booked seats, cancelled seats, available seats, and checked seats.
        """
        # Create DataFrame to display the seating arrangement
        df = pd.DataFrame(self.data)
        df.index = df.index + 1
        pd.set_option('display.max_columns', None)
        print(df.transpose())  # Transpose DataFrame to display seats in columns
        # Print total seats, booked seats, cancelled seats, available seats, and checked seats
        print(f"\nTotal seats: {self.total_seats}")
        print(f"Booked seats: {len(self.booked)}")
        print(f"Cancelled seats: {len(self.cancelled)}")
        print(f"Available seats: {self.total_seats - len(self.booked)}")
        print(f"Checked seats: {len(self.checked)}")

    def menu(self):
        while True:
            # Display menu options
            print("\nMenu:")
            print("1. Check availability of seat")
            print("2. Book a seat")
            print("3. Free a seat")
            print("4. Show booking state")
            print("5. Exit program")

            choice = input("Select an option: ")  # Get user choice

            # Perform action based on user choice
            if choice == '1':
                self.choice1()
            elif choice == '2':
                self.choice2()
            elif choice == '3':
                self.choice3()
            elif choice == '4':
                self.show_booking_state()
            elif choice == '5':
                print("\nThank you for choosing Apache airlines...✈️")
                break
            else:
                print("Invalid choice. Please select from 1 to 5.")


if __name__ == "__main__":
    # Initialize seat booking system
    seat_booking_system = SeatBookingSystem()
    # Start main menu
    seat_booking_system.menu()
