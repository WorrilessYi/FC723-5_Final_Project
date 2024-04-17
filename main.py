import pandas as pd
data = {}
columns = ['A', 'B', 'C', 'X', 'D', 'E', 'F']
storage_space = ['D77', 'E77', 'F77', 'D78', 'E78', 'F78']
all = 6 * 80 - len(storage_space)
for col in columns:
    temp = []
    for x in range(1, 81):
        if col == 'X':
            temp.append('X')
        elif col+str(x) in storage_space:
            temp.append('S')
        else:
            temp.append('F')
    data[col] = temp


# Create the pandas DataFrame
df = pd.DataFrame(data)
df.index = df.index + 1
checked, booked, cancelled = [], [], []


def choice1():
    answer = input("Enter a seat number to check availability (e.g. A9) or (quit): ")
    if answer.lower() == 'quit' or answer.lower() == 'q':
        return
    check = check_seat(answer)
    checked.append(answer)
    if check == "S" or check == "B":
        print(f"Sorry the seat {answer} is not available")
        return choice1()
    elif check == "F":
        print(f"The seat {answer} is available")
        print("1. Check another seat\n"
              "2. Book the seat\n"
              "3. Go back to main menu")
        input_choice = input("Select an option: ")
        if input_choice == "1":
            return choice1()
        elif input_choice == "2":
            return book_seat(answer)
        elif input_choice == "3":
            return
        else:
            print("Invalid input")
    else:
        print(check)


def check_seat(seat_num):
    seat = list(seat_num)
    if len(seat) == 2:
        if seat[0].isalpha() and seat[1].isdigit():
            first = seat[0].upper()
            second = int(seat[1])
            if first in df.columns and 1 <= second <= 80:
                return df[first][second]
    elif len(seat) == 3:
        if seat[0].isalpha() and seat[1].isdigit() and seat[2].isdigit():
            first = seat[0].upper()
            second = int(seat[1]+seat[2])
            if first in df.columns and 1 <= second <= 80:
                return df[first][second]
    return "Invalid input for seat number. Please enter a valid seat number (e.g., A1)."


def choice2():
    answer = input("Enter a seat number to book (e.g. A9) or (quit): ")
    if answer.lower() == 'quit' or answer.lower() == 'q':
        return
    check = check_seat(answer)
    if check == "S" or check == "B":
        print(f"Sorry the seat {answer} is not available")
        return choice2()
    elif check == "F":
        print(book_seat(answer))
        booked.append(answer)
        print("1. Cancel the seat\n"
              "2. Book another seat\n"
              "3. Go back to main menu")
        input_choice = input("Select an option: ")
        if input_choice == "1":
            return free_seat(answer)
        elif input_choice == "2":
            return choice2()
        elif input_choice == "3":
            return
        else:
            print("Invalid input")
    else:
        print(check)


def book_seat(seat_num):
    seat = list(seat_num)
    if len(seat) == 2:
        try:
            number = int(seat[1])
            letter = seat[0].upper()
        except ValueError:
            print("Invalid input for seat number. Please enter a valid seat number (e.g., A1).")
        else:
            df.loc[number, letter] = 'B'
        return f"The seat {seat_num} is successfully booked"
    elif len(seat) == 3:
        if seat[0].isalpha() and seat[1].isdigit() and seat[2].isdigit():
            letter = seat[0].upper()
            number = int(seat[1] + seat[2])
            if letter in df.columns and 1 <= number <= 80:
                df.loc[number, letter] = 'B'
                return f"The seat {seat_num} is successfully booked"
    return "Invalid input for seat number. Please enter a valid seat number (e.g., A1)."


def choice3():
    answer = input("Enter a seat number to cancel (e.g. A9) or (quit): ")
    if answer.lower() == 'quit' or answer.lower() == 'q':
        return
    check = check_seat(answer)
    if check == "F" or check == "S":
        print(f"Sorry the seat {answer} is not booked and can't be cancelled")
        return choice3()
    elif check == "B":
        print(free_seat(answer))
        cancelled.append(answer)
    else:
        print(check)


def free_seat(seat_num):
    seat = list(seat_num)
    if len(seat) == 2:
        try:
            number = int(seat[1])
            letter = seat[0].upper()
        except ValueError:
            number = int(seat[0])
            letter = seat[1].upper()
        df.loc[number, letter] = 'F'
        return f"The seat {seat_num} is successfully cancelled"
    elif len(seat) == 3:
        if seat[0].isalpha() and seat[1].isdigit() and seat[2].isdigit():
            letter = seat[0].upper()
            number = int(seat[1] + seat[2])
            if letter in df.columns and 1 <= number <= 80:
                df.loc[number, letter] = 'F'
                return f"The seat {seat_num} is successfully cancelled"
        return "Invalid input for seat number. Please enter a valid seat number (e.g., A1)."


def show_state():
    pd.set_option('display.max_columns', None)
    print(df.transpose())
    print(f"The seats booked: {str(booked)}")
    print(f"The seats cancelled: {str(cancelled)}")
    print(f"{all-len(booked)+len(cancelled)} available out of {all} seats")


print(df.transpose())
while True:
    print("\n1. Check availability of seat \n"
          "2. Book a seat\n"
          "3. Free a seat\n"
          "4. Show booking state\n"
          "5. Exit program\n")
    input_choice = input("Select an option: ")
    if input_choice == "1":
        choice1()
    elif input_choice == "2":
        choice2()
    elif input_choice == "3":
        choice3()
    elif input_choice == "4":
        show_state()
    elif input_choice == "5":
        print("Thank you for choosing Apache airlines✈️")
        break
    else:
        print("Invalid choice!")
