import pymysql
import matplotlib.pyplot as plt
from datetime import datetime

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
        try:
            c9 = connection.cursor()
            c9.callproc('isDoctor', (d_id, dfname, dlname))
            all_device = c9.fetchall()
            for row in all_device:
                print(row)
            c9.close()
            break  # Break out of the loop if the query succeeds

        except pymysql.Error as e:
            code, msg = e.args
            print("Error retrieving data from the database:", code, msg)
            print("Please re-enter your name.")
            d_id = input("Doctor ID: ")
            dfname = input("Doctor First Name: ")
            dlname = input("Doctor Last Name: ")

    main_menu = True
    while main_menu:
        print("\nPlease select an option:")
        print("1. View your information")
        print("2. View devices")
        print("3. Perform administrative tasks")
        print("4. View your patients")
        print("0. Exit")
        option = input("Enter your choice (0-4): ")


            #
            # # Perform validation checks
            # if not d_id.isdigit():
            #     print("Doctor ID must be a numeric value.")
            #     continue
            #
            # if not dfname.isalpha() or not dlname.isalpha():
            #     print("Doctor first name and last name must contain only alphabetic characters.")
            #     continue
            #
            # # Validation checks passed, break out of the loop
            # break

        # if choice.lower() == "yes":
        #     option = "3"  # Set the option to 3 (View devices) if the user chooses to search for new devices
        #     choice = "no"  # Reset the choice to "no" to avoid re-entering the prompt for searching new devices
        #     continue  # Skip the input prompt in the main menu and directly enter the elif statement for option 3
        # else:
        #     option = input("Enter your choice (0-4): ")


        if option == "1":
            # Option 2: View user information
            print("Viewing your information...")
            # Add your code for viewing user information here

            try:
                print("Doctor Information")
                c4 = connection.cursor()
                c4.callproc('doctorInfo', (d_id, dfname, dlname))
                all_device = c4.fetchall()
                for row in all_device:
                    print(row)
                c4.close()

            except pymysql.Error as e:
                code, msg = e.args
                print("Error retrieving data from the database:", code, msg)

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


        # Ask the user if they want to search for new devices
            choice = input("Do you want to request a device or ? (yes/no): ")
            if choice.lower() == "yes":
                option = "2"
            elif choice.lower() == "no":
                while True:
                    admin_option = input(
                        "\nEnter 'menu' to go back to the main menu or 'exit' to exit the code: ").lower().strip()
                    if admin_option == "menu":
                        print("Entering main menu")
                        break
                    elif admin_option == "exit":
                        print("Exiting the code...")
                        exit()
                    elif admin_option != "menu" or admin_option != "exit":
                        print("Invalid option. Please choose again.")

        if option == "2":
            view_device = True
            if view_device:
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

                filter_menu = True
                while filter_menu:
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
                        filter_menu = False
                        view_device = False
                        break

                    else:
                        # Invalid option
                        print("Invalid option. Please choose again.")

                    reprompt1 = ""
                    while reprompt1 not in ["yes", "no"]:
                        reprompt1 = input(
                            "\nDo you want to continue filtering? (yes/no): ")
                        break

                    if reprompt1.lower() == "yes":
                        continue
                    elif reprompt1.lower() == "no":
                        filter_menu = False
                        break


        elif option == "3":
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
        elif option == "4":
            print("Your Patient(s)")
            try:
                c7 = connection.cursor()  # shouldn't reuse cursors
                # calling procedure by its string
                c7.callproc(
                    'filterPatient', [
                        d_id])  # second part department, is the list of parameters to the specific proceudre get_department
                all_patients = c7.fetchall()
                for row in all_patients:
                    print(row)

            except pymysql.Error as e:
                code, msg = e.args
                print("Error retrieving data from the database:", code, msg)

            if not all_patients:
                print("No patients found.")

            patient_menu = True
            while patient_menu:
                print("\nSelect an option:")
                print("1. Add a patient")
                print("2. Delete a patient")
                print("3. Select a specific patient for further operations")
                print("0. Go Back to Main Menu")

                sub_option = input("Enter your choice (1, 2, or 3): ")

                if sub_option == "1":
                # Add a patient
                # Code to add a patient to the database
                    while True:
                        try:
                            c10 = connection.cursor()  # shouldn't reuse cursors
                            # calling procedure by its string
                            c10.callproc(
                                'availableRooms', [d_id])  # second part department, is the list of parameters to the specific proceudre get_department
                            available_rooms = c10.fetchall()
                            print("These are the available rooms in the current doctor hospital you can assign patient to")
                            print(available_rooms)
                        except pymysql.Error as e:
                            code, msg = e.args
                            print("Error retrieving data from the database:", code, msg)

                        values = input("Enter patient first name, last name, check in, and room number separated by commas : (e.g Ace, Ventura, 2023-06-20 14:30:00, 101")
                        value_list = values.split(",")

                        if len(value_list) != 4:
                            print("Invalid number of values. Please enter 4 values.")
                            continue

                        pt_fname, pt_lname, pt_in, room_n = [value.strip() for value in value_list]
                        print(pt_fname, pt_lname, pt_in, room_n)

                        if not pt_fname.isalpha() or not pt_fname:
                            print("Invalid value: pt_fname must be a non-empty string.")
                            continue

                        if not pt_lname.isalpha() or not pt_lname:
                            print("Invalid value: pt_lname must be a non-empty string.")
                            continue

                        try:
                            datetime.strptime(pt_in, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            print("Invalid value: pt_in must be a valid datetime in the format 'YYYY-MM-DD HH:MM:SS'.")
                            continue


                        # print(all_patients)
                        for row in available_rooms:
                            # print(type(row['pt_id']))
                            if room_n.isdigit() and int(room_n) == row['room_num']:
                                continue

                        break

                    try:
                        c9 = connection.cursor()  # shouldn't reuse cursors
                        # calling procedure by its string
                        c9.callproc(
                            'createPatient', [pt_fname, pt_lname, pt_in, room_n, d_id])  # second part department, is the list of parameters to the specific proceudre get_department

                    except pymysql.Error as e:
                        code, msg = e.args
                        print("Error retrieving data from the database:", code, msg)

                elif sub_option == "2":
                    if not all_patients:
                        print("No patients to delete")
                        continue

                # Delete a patient
                # Code to delete a patient from the database
                    b = True
                    while b == True:
                        pt_id = input("Enter patient id you want to delete from list above: ")

                        match_found = False

                       # print(all_patients)
                        for row in all_patients:
                            #print(type(row['pt_id']))
                            if pt_id.isdigit() and int(pt_id) == row['pt_id']:
                                match_found = True
                                print("found")
                                break

                        if match_found:
                            print("Code ran successfully")
                            c8 = connection.cursor()  # shouldn't reuse cursors
                            # calling procedure by its string
                            c8.callproc(
                                'removePatient',
                                [pt_id, ])  # second part department, is the list of parameters to the specific proceudre get_department
                            for row in c8.fetchall():
                                print("The following record has been deleted")
                                print(row)
                            c8.close()
                            b = False
                            break
                        else:
                            print("Error: Patient doesn't match your list")


                elif sub_option == "3":
                    # Select a specific patient for further operations
                    # Code to perform operations on a specific patient
                    while True:
                        pt_id = input("Enter patient id you want to examine from list above: ")

                        match_found = False

                        # print(all_patients)
                        for row in all_patients:
                            # print(type(row['pt_id']))
                            if pt_id.isdigit() and int(pt_id) == row['pt_id']:
                                match_found = True
                                break

                        if match_found:
                            print("You have selected a patient")
                            patient_options = True
                            while patient_options:
                                # Display additional options for the selected patient
                                print("\nAdditional Options for Patient:")
                                print("1. Option 1")
                                print("2. Option 2")
                                print("3. Option 3")

                                patient_option = ""
                                while patient_option not in ["1", "2", "3"]:
                                    patient_option = input("Please enter a valid choice (0-3): ")

                                if patient_option == "1":
                                    # Code for Option 1
                                    pass

                                elif patient_option == "2":
                                    # Code for Option 2
                                    pass

                                elif patient_option == "3":
                                    # Code for Option 3
                                    pass


                                reprompt = ""
                                while reprompt not in ["option", "select", "main"]:
                                    reprompt = input(
                                        "\nDo you want to go back to select a different option for the specified patient, \n select a new patient, or go back to the main menu? (option/select/main): ")


                                if reprompt.lower() == "option":
                                    continue
                                elif reprompt.lower() == "select":
                                    break
                                elif reprompt.lower() == "main":
                                    patient_menu = False
                                    break
                            #
                            if reprompt.lower() == "select":
                                continue
                            elif reprompt.lower() == "main":
                                patient_menu = False
                                break

                        else:
                            print("Error: Patient doesn't match your list")

                elif sub_option == "0":
                    # Go back to the suboptions menu
                    patient_menu = False

                else:
                    print("Invalid choice. Please select a valid option.")

                # while True:
                #     reprompt = input("\nDo you want to go back to the sub-options or main menu? (sub/main): ")
                #     if reprompt.lower() == "sub":
                #         break
                #     elif reprompt.lower() == "main":
                #         break
                #     else:
                #         print("Invalid input. Please enter 'sub' or 'main'.")
                #
                # if reprompt.lower() == "main":
                #     break

        elif option == "0":
            # Option 0: Exit the program
            print("Exiting the program. Goodbye!")
            main_menu = False

        else:
            # Invalid option
            print("Invalid option. Please choose again.")




if __name__ == '__main__':
    work('medical_device')