import pandas as pd
data = {}
columns = ['A', 'B', 'C', 'X', 'D', 'E', 'F']
storage_space = ['D78', 'E78', 'F78', 'D79', 'E79', 'F79']

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
df.loc[1, 'A'] = 'B'
print(df.transpose())
print(df['D'][78])


def choice1():
    answer = input("Enter a seat number to check availability (e.g. A9): ")
    check = check_seat(answer)
    if check == "S" or check == "B":
        print(f"Sorry the seat {answer} is not available")
        print("1. Check another seat\n"
              "2. Go back to main menu")
        input_choice = int(input("Select an option: "))
        if input_choice == 1:
            return choice1()
        elif input_choice == 2:
            return
        else:
            print("Invalid input")
    elif check == "F":
        print(f"The seat {answer} is available")
        print("1. Check another seat\n"
              "2. Book the seat\n"
              "3. Go back to main menu")
        input_choice = int(input("Select an option: "))
        if input_choice == 1:
            return choice1()
        elif input_choice == 2:
            return choice2()
        elif input_choice == 3:
            return
        else:
            print("Invalid input")
    else:
        print(check)


def check_seat(seat_num):
    seat = list(seat_num)
    if len(seat) == 2:
        first = seat[0].upper()
        second = int(seat[1])
        return df[first][second]
    else:
        return "Invalid input for seat number"


def choice2():
    answer = input("Enter a seat number to book (e.g. A9): ")
    check = check_seat(answer)
    if check == "S" or check == "B":
        print(f"Sorry the seat {answer} is not available")
        print("1. Book another seat\n"
              "2. Go back to main menu")
        input_choice = int(input("Select an option: "))
        if input_choice == 1:
            return choice2()
        elif input_choice == 2:
            return
        else:
            print("Invalid input")
    elif check == "F":
        print(book_seat(answer))
        print("1. Book another seat\n"
              "2. Go back to main menu")
        input_choice = int(input("Select an option: "))
        if input_choice == 1:
            return choice2()
        elif input_choice == 2:
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
            number = int(seat[0])
            letter = seat[1].upper()
        df.loc[number, letter] = 'B'
        return f"The seat {seat_num} is successfully booked"
    else:
        return "Invalid input for seat number"


while True:
    print("1. Check availability of seat \n"
          "2. Book a seat\n"
          "3. Free a seat\n"
          "4. Show booking state\n"
          "5. Exit program\n")
    input_choice = int(input("Select an option: "))
    if input_choice == 1:
        choice1()
    elif input_choice == 2:
        choice2()
    elif input_choice == 3:
        answer = input("Enter a seat number to cancel: ")
    elif input_choice == 4:
        print("There are {available} available seats out of {all}")
    elif input_choice == 5:
        print("Thank you for choosing Apache airlines✈️")
        break
    else:
        print("Invalid choice!")


