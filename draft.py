import pymysql
import matplotlib.pyplot as plt

def work(name):
    # Use a breakpoint in the code line below the debug your script.
    username = input("Enter username: ")
    pword = input("Enter password: ")
    d_id = input("Doctor ID: ")
    dfname = input("Doctor First Name: ")
    dlname = input("Doctor Last Name: ")

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
    authenticated = False

    # Display the main menu options
    print("Welcome to the main menu")

    choice = "no"  # Initialize the choice variable

    # Prompt user for additional options
    while True:
        print("\nPlease select an option:")
        print("1. Create new medical device entry")
        print("2. View your information")
        print("3. View devices")
        print("4. Perform administrative tasks")
        print("5. View your patients")
        print("0. Exit")
        option = input("Enter your choice (0-5): ")

        # if choice.lower() == "yes":
        #     option = "3"  # Set the option to 3 (View devices) if the user chooses to search for new devices
        #     choice = "no"  # Reset the choice to "no" to avoid re-entering the prompt for searching new devices
        #     continue  # Skip the input prompt in the main menu and directly enter the elif statement for option 3
        # else:
        #     option = input("Enter your choice (0-4): ")

        if option == "1":
            # Option 1: Create new medical device entry
            print("Creating new medical device entry...")
            # Add your code for creating a new medical device entry here

        elif option == "2":
            # Option 2: View user information
            print("Viewing your information...")
            # Add your code for viewing user information here

            while True:
                try:
                    print("Doctor Information")
                    c4 = connection.cursor()
                    c4.callproc('doctorInfo', (d_id, dfname, dlname))
                    all_device = c4.fetchall()
                    for row in all_device:
                        print(row)
                    c4.close()
                    break  # Break out of the loop if the query succeeds

                except pymysql.Error as e:
                    code, msg = e.args
                    print("Error retrieving data from the database:", code, msg)

                    # Prompt user to re-enter the name
                    print("Please re-enter your name.")
                    d_id = input("Doctor ID: ")
                    dfname = input("Doctor First Name: ")
                    dlname = input("Doctor Last Name: ")


            print("Your devices in use")
            try:
                print("Your Device(s)")
                c6 = connection.cursor()  # shouldn't reuse cursors
                # calling procedure by its string
                c6.callproc(
                    'filterDoctor', [d_id])  # second part department, is the list of parameters to the specific proceudre get_department
                for row in c6.fetchall():
                    print(row)

            except pymysql.Error as e:
                code, msg = e.args
                print("Error retrieving data from the database:", code, msg)

            # print("Your Patient(s)")
            # try:
            #     c7 = connection.cursor()  # shouldn't reuse cursors
            #     # calling procedure by its string
            #     c7.callproc(
            #         'filterPatient', [d_id] )  # second part department, is the list of parameters to the specific proceudre get_department
            #     for row in c7.fetchall():
            #         print(row)
            #
            # except pymysql.Error as e:
            #     code, msg = e.args
            #     print("Error retrieving data from the database:", code, msg)

        # Ask the user if they want to search for new devices
            choice = input("Do you want to request a device? (yes/no): ")
            if choice.lower() == "yes":
                option = "3"
            elif choice.lower() == "no":
                while True:
                    admin_option = input("\nEnter 'menu' to go back to the main menu or 'exit' to exit the code: ")
                    if admin_option == "menu":
                        break
                    elif admin_option == "exit":
                        print("Exiting the code...")
                        exit()
                    else:
                        print("Invalid option. Please choose again.")

        if option == "3":
            # if option == "3":
            #     view_devices = True
            # if view_devices:
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
                    print("1. Filter devices by device type")
                    print("2. Filter devices by hospital")
                    print("3. Filter which room contains specified device")
                    print("0. Return to the main menu")
                    filter_option = input("Enter your choice (0-4): ")

                    if filter_option == "1":
                        # Add code to filter devices by category
                        while True:
                            try:
                                print("Filter by Device Type")
                                device_type = input("Enter Device Type: ")
                                c1 = connection.cursor()
                                c1.callproc('filterType', (device_type,))
                                for row in c1.fetchall():
                                    print(row)
                                c1.close()
                                break  # Break out of the loop if no error occurs

                            except pymysql.Error as e:
                                code, msg = e.args
                                print("Error retrieving data from the database:", code, msg)
                                print("Please try again.\n")

                    elif filter_option == "2":
                        # Add code to filter devices by category
                        while True:
                            try:
                                print("Filter by Hospital")
                                hosp = input("Enter Hospital: ")
                                c2 = connection.cursor()
                                c2.callproc('filterHospital', (hosp,))
                                for row in c2.fetchall():
                                    print(row)
                                c2.close()
                                break  # Break out of the loop if no error occurs

                            except pymysql.Error as e:
                                code, msg = e.args
                                print("Error retrieving data from the database:", code, msg)
                                print("Please try again.\n")

                    elif filter_option == "3":
                        # Add code to filter devices by category
                        while True:
                            try:
                                print("Where specified device is located")
                                device = input("What device are you locating: ")
                                c3 = connection.cursor()
                                c3.callproc('filterRoom', (device,))
                                for row in c3.fetchall():
                                    print(row)
                                c3.close()
                                break  # Break out of the loop if no error occurs

                            except pymysql.Error as e:
                                code, msg = e.args
                                print("Error retrieving data from the database:", code, msg)
                                print("Please try again.\n")


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

        elif option == "4":
            if not authenticated:
                # Option 4: Perform administrative tasks
                # Initialize variables to store user input
                incorrect_attempts = 0
                ausername = ""
                apassword = ""


                # Loop until valid credentials are provided or maximum attempts are reached
                while ausername != admin_username or apassword != admin_password:
                    # Prompt user for username and password
                    ausername = input("Enter your username: ")
                    apassword = input("Enter your password: ")

                    # Check if username and password are correct
                    if ausername == admin_username and apassword == admin_password:
                        # Perform administrative tasks
                        authenticated = True
                        print("Authentication successful. You can now perform administrative tasks.")
                        break
                    else:
                        # Invalid username or password
                        incorrect_attempts += 1
                        print("Access denied. Invalid username or password. Please try again.")
                        if incorrect_attempts == 3:
                            print("Maximum incorrect attempts reached. Returning to the main menu.")
                            break
            if authenticated:
                # User is already authenticated, perform administrative tasks
                print("Performing administrative tasks...")
                # Add your code for the administrative tasks here
                # Add your code for the administrative tasks here
                print("\nPlease select an option:")
                print("1. Add Room")
                print("2. Remove Room")
                print("3. Add Hospital")
                print("4. Remove Hospital")
                print("0. Exit")
                option_choice = input("Enter your choice (0-4): ")

                if option_choice == "1":
                    try:
                        con = connection.cursor()

                        room_num = input("Please enter the room number you want to add: ")
                        hosp_id = input("Please enter the corresponding hospital id: ")

                        con.callproc("addRoom", (room_num, hosp_id))

                        con.close()
                    except:
                        print('Error: %d: %s' % (e.args[0], e.args[1]))

                elif option_choice == "2":
                    try:
                        con2 = connection.cursor()

                        room_num = input("Please enter the room number you want to add: ")
                        hosp_id = input("Please enter the corresponding hospital id: ")

                        con.callproc("removeRoom", (room_num, hosp_id))

                        con2.close()
                    except:
                        print('Error: %d: %s' % (e.args[0], e.args[1]))

                elif option_choice == "3":
                    try:
                        con4 = connection.cursor()

                        hosp_id = input("Please enter the new hospital's id: ")
                        hosp_name = input("Please enter the new hospital's name: ")
                        hosp_streetnum = input("Please enter the new hospital's street number: ")
                        hosp_streetname = input("Please enter the new hospital's street name: ")
                        hosp_town = input("Please enter the new hospital's town: ")
                        hosp_state = input("Please enter the new hospital's state: ")
                        hosp_zipcode = input("Please enter the new hospital's zipcode: ")

                        con4.callproc("addHosp", (
                        hosp_id, hosp_name.hosp_streetnum, hosp_streetname, hosp_town, hosp_state, hosp_zipcode))

                        con4.close()
                    except:
                        print('Error: %d: %s' % (e.args[0], e.args[1]))

                elif option_choice == "4":
                    try:
                        con3 = connection.cursor()

                        hosp_id = input("Please enter the hospital id that you wish to delete: ")

                        con.callproc("removeHospital", (hosp_id))

                        con3.close()
                    except:
                        print('Error: %d: %s' % (e.args[0], e.args[1]))

                # After performing administrative tasks, give the option to go back to the main menu or exit
                while True:
                    admin_option = input("\nEnter 'menu' to go back to the main menu or 'exit' to exit the code: ")
                    if admin_option == "menu":
                        break
                    elif admin_option == "exit":
                        print("Exiting the code...")
                        exit()
                    else:
                        print("Invalid option. Please choose again.")
        elif option == "5":
            print("Your Patient(s)")
            try:
                c7 = connection.cursor()  # shouldn't reuse cursors
                # calling procedure by its string
                c7.callproc(
                    'filterPatient', [
                        d_id])  # second part department, is the list of parameters to the specific proceudre get_department
                for row in c7.fetchall():
                    print(row)

            except pymysql.Error as e:
                code, msg = e.args
                print("Error retrieving data from the database:", code, msg)


        elif option == "0":
            # Option 0: Exit the program
            print("Exiting the program. Goodbye!")
            break

        else:
            # Invalid option
            print("Invalid option. Please choose again.")




if __name__ == '__main__':
    work('medical_device')