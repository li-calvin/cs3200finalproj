import pymysql
import matplotlib.pyplot as plt

def work(name):
    # Use a breakpoint in the code line below the debug your script.
    username = input("Enter username: ")
    pword = input("Enter password: ")

    try:
        connection = pymysql.connect(
            host = "localhost",
            user = username, #root
            password= pword, #specify regular password
            database = name,
            cursorclass=pymysql.cursors.DictCursor, #many other cursors to use
                autocommit = True) #ensures that whenever you connect to db it automatically modifies
    except pymysql.Error as e: #to deal with procesing errors
        code, msg = e.args
        print("Cannot connect to the database", code, msg)

    # Define the correct admin username and password
    admin_username = "admin"
    admin_password = "password"

    # Prompt user if they want to perform administrative tasks
    choice = input("Do you want to perform administrative tasks? (yes/no): ")

    # Check user's choice
    if choice.lower() == "yes":
        # Initialize variables to store user input
        ausername = ""
        apassword = ""

        # Loop until valid credentials are provided
        while ausername != admin_username or apassword != admin_password:
            # Prompt user for username and password
            ausername = input("Enter your username: ")
            apassword = input("Enter your password: ")

            # Check if username and password are correct
            if ausername == admin_username and apassword == admin_password:
                # Perform administrative tasks
                pass

            else:
                # Invalid username or password
                print("Access denied. Invalid username or password. Please try again.")
    else:
        # User doesn't want to perform administrative tasks
        print("Welcome to the main menu")

        # Prompt user for additional options
        while True:
            print("\nPlease select an option:")
            print("1. Create new medical device entry")
            print("2. View your information")
            print("3. View devices")
            print("0. Exit")
            option = input("Enter your choice (0-3): ")

            if option == "1":
                # Option 1: Create new medical device entry
                print("Creating new medical device entry...")
                # Add your code for creating a new medical device entry here

            elif option == "2":
                while True:
                    # Option 2: View user information
                    print("Viewing your devices used ...")

                    try:
                        print("Filter by Doctor First Name, Last Name ")
                        first = input("Enter doctor first name: ")
                        last = input("Enter doctor last name: ")

                        c3 = connection.cursor()  # shouldn't reuse cursors
                        # calling procedure by its string
                        c3.callproc('filterDoctor', [first, last])  # second part department, is the list of parameters to the specific proceudre get_department
                        for row in c3.fetchall():
                            print(row)
                        c3.close()
                    except pymysql.Error as e:
                        code, msg = e.args
                        print("Error retrieving data from the db", code, msg)

                    # Ask the user if they want to return to the main menu
                    return_to_menu = input("Do you want to return to the main menu? (yes/no): ")
                    if return_to_menu.lower() == "yes":
                        break
                    else:
                        continue

            elif option == "3":
                while True:
                    # Option 3: View devices
                    print("Viewing devices...")
                    # Add your code for viewing devices here
                    print("ordering the device by quantity")
                    try:
                        print("Order Device ")
                        c5 = connection.cursor()  # shouldn't reuse cursors
                        # calling procedure by its string
                        c5.callproc(
                            'mostQuantity2', )  # second part department, is the list of parameters to the specific proceudre get_department
                        all_device = c5.fetchall()
                        for row in all_device:
                            print(row)

                        quantities = [row['quantity'] for row in all_device]
                        devices = [row['device_id'] for row in all_device]
                        plt.bar(devices, quantities)
                        plt.xlabel('Device')
                        plt.ylabel('Quantity')
                        plt.title('Device Quantity')
                        plt.show()
                        c5.close()


                    except pymysql.Error as e:
                        code, msg = e.args
                        print("Error retrieving data from the db", code, msg)

                    while True:
                        print("\nPlease select a filtering option:")
                        print("1. Filter devices by category")
                        print("2. Filter devices by price range")
                        print("3. Filter devices by availability")
                        print("0. Return to the main menu")
                        filter_option = input("Enter your choice (0-3): ")

                        if filter_option == "1":
                            # Add code to filter devices by category
                            try:
                                print("Filter by Device Type")
                                type = input("Enter Device Type: ")
                                c1 = connection.cursor()  # shouldn't reuse cursors
                                # calling procedure by its string
                                c1.callproc('filterType', (
                                type,))  # second part department, is the list of parameters to the specific proceudre get_department
                                for row in c1.fetchall():
                                    print(row)

                            except pymysql.Error as e:
                                code, msg = e.args
                                print("Error retrieving data from the db", code, msg)

                        elif filter_option == "0":
                            # Return to the main menu
                            break

                        else:
                            # Invalid option
                            print("Invalid option. Please choose again.")

                    # Ask the user if they want to return to the main menu
                    return_to_menu = input("Do you want to return to the main menu? (yes/no): ")
                    if return_to_menu.lower() == "yes":
                        break
                    else:
                        continue

            elif option == "0":
                # Option 0: Exit the program
                print("Exiting the program. Goodbye!")
                break

            else:
                # Invalid option
                print("Invalid option. Please choose again.")



    """
    try:
        print("Filter by Room")
        room = input("Enter Room: ")
        c2 = connection.cursor() #shouldn't reuse cursors
        # calling procedure by its string
        c2.callproc('filter_byRoom', (room,)) #second part department, is the list of parameters to the specific proceudre get_department
        for row in c2.fetchall():
            print(row)
            print("The following devices are used in room " + room + ": " + row['devices'])
        c2.close()
    except pymysql.Error as e:
        code, msg = e.args
        print("Error retrieving data from the db", code, msg)

    

    print("There are other functionailities that exist such as moving the medial device to the appropriate room that the device is needed in ")
    try:
        print("Move Medical Device")
        device = input("Enter the device that needs to be moved: ")
        old_room = input("Enter the old room that the device currently exists in : ")
        new_room = input("Enter the new room you want to relocate the device")

        c4 = connection.cursor() #shouldn't reuse cursors
        # calling procedure by its string
        c4.callproc('filterDoctor', [device, old_room, new_room]) #second part department, is the list of parameters to the specific proceudre get_department
        c4.close()
    except pymysql.Error as e:
        code, msg = e.args
        print("Error retrieving data from the db", code, msg)



    
    
    print("List of all Examinations of a specific patient")
    try:
        first = input("Enter patient first name: ")
        last = input("Enter patient last name: ")

        c6 = connection.cursor()  # shouldn't reuse cursors
        # calling procedure by its string
        c6.callproc(
            'allExam', [first, last] )  # second part department, is the list of parameters to the specific proceudre get_department
        for row in c6.fetchall():
            print(row)
        c6.close()
    except pymysql.Error as e:
        code, msg = e.args
        print("Error retrieving data from the db", code, msg)
    """


    connection.close()




if __name__ == '__main__':
    work('medical_device')
