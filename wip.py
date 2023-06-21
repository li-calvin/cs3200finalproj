import pymysql
import matplotlib.pyplot as plt
from datetime import datetime

def work(name):
    # Use a breakpoint in the code line below the debug your script.
    print("\n-------- Login --------")
    username = input("Enter username (e.g root): ")
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

    choice = "no"  # Initialize the choice variable

    # Prompt user for doctor id, fname, lname if entered incorrectly at beginning
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
            print("\nError retrieving data from the database:", code, msg)
            print("Please re-enter your name.")
            d_id = input("Doctor ID: ")
            dfname = input("Doctor First Name: ")
            dlname = input("Doctor Last Name: ")

    main_menu = True
    while main_menu:
        # Display the main menu options
        print("\n-------- Main Menu --------")
        print("Please select an option:")
        print("1. View your information")
        print("2. View devices")
        print("3. Perform administrative tasks")
        print("4. View your patients")
        print("0. Exit")
        option = input("Enter your choice (0-4): ")

        # Option 1: View Your Doctor Information
        if option == "1":
            # Option 2: View user information
            print("\nViewing your information...")
            # Add your code for viewing user information here

            # View Doctor Information
            try:
                print("-- Doctor Information -- ")
                c4 = connection.cursor()
                c4.callproc('doctorInfo', (d_id, dfname, dlname))
                all_device = c4.fetchall()
                for row in all_device:
                    print(row)
                c4.close()
            except pymysql.Error as e:
                code, msg = e.args
                print("Error retrieving data from the database:", code, msg)

            # View Your Devices and corresponding examination it is used in
            try:
                print("\n-- Your Device(s) and Corresponding Test --")
                c6 = connection.cursor()
                c6.callproc(
                    'filterDoctor', [d_id])
                for row in c6.fetchall():
                    print(row)
            except pymysql.Error as e:
                code, msg = e.args
                print("Error retrieving data from the database:", code, msg)

            # Ask the user if they want to request a device or not
            choice = ""
            while choice not in ["yes", "no"]:
                print("\nDo you want to request a device?")
                choice = input("Please select a valid option (yes/no): ")

            if choice.lower() == "yes":
                option = "2" # sends the user directly to view all available devices in system
            elif choice.lower() == "no":
                while True:
                    # Provide option to either go to main menu or exit after entering no
                    print("\nDo you want to return to main menu or exit")
                    admin_option = input(
                        "Please select a valid option (menu/exit):  ").lower().strip()
                    if admin_option == "menu":
                        print("Entering main menu...")
                        break
                    elif admin_option == "exit":
                        print("Exiting Program...")
                        exit()
                    else:
                        print("Invalid option. Please choose again.")

        # Option 2: View devices
        if option == "2":
            view_device = True
            if view_device:
                print("\nViewing devices...")
                print("\n-- Devices --")
                try:
                    c5 = connection.cursor()
                    c5.callproc(
                        'mostQuantity2', )
                    all_device = c5.fetchall()
                    for row in all_device:
                        print(row)

                    # Visualization of all device
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

                # After Viewing Devices given filtering menu for devices
                filter_menu = True
                while filter_menu:
                    print("\n-------- Filter --------")
                    print("\nPlease select a filtering option:")
                    print("1. Filter devices by device type")
                    print("2. Filter devices by hospital")
                    print("3. Filter which room contains specified device")
                    print("0. Return to the main menu")
                    filter_option = input("Enter your choice (0-3): ")

                    # Filter Option 1: Filter devices by device type
                    if filter_option == "1":
                        while True:
                            try:
                                print("\nFilter by Device Type")
                                device_type = input("Enter Device Type: ")
                                print("-- Devices under category:", device_type, "--")
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

                    # Filter Option 2: Filter devices that exist in a specified hospital
                    elif filter_option == "2":
                        while True:
                            try:
                                print("\nFilter Devices by Hospital")
                                hosp = input("Enter Hospital: ")
                                print("-- Devices in Hospital:", hosp, "--")
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

                    # Filter Option 3: Determine Location of Specified Device
                    elif filter_option == "3":
                        while True:
                            try:
                                print("\nFilter Device Location")
                                device = input("What device are you locating: ")
                                print("-- Location of device:", device, "--")
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

                    # Option 0: Return to the main menu
                    elif filter_option == "0":
                        filter_menu = False
                        view_device = False
                        break

                    # Invalid option
                    else:
                        print("Invalid option. Please choose again.")

                    # Gives the option to either continue filtering or not
                    print("\nDo you want to continue filtering?")
                    reprompt1 = ""
                    while reprompt1 not in ["yes", "no"]:
                        reprompt1 = input(
                            "Please select a valid option (yes/no): ")

                    if reprompt1.lower() == "yes":
                        continue
                    elif reprompt1.lower() == "no":
                        # For prompting the user if they want to move a device
                        print("\nDo you want to move device?")
                        prompt = ""
                        while prompt not in ["yes", "no"]:
                            prompt = input(
                                "Please select a valid option (yes/no): ")

                        if prompt.lower() == "yes":
                            try:
                                print("All Rooms")
                                c12 = connection.cursor()
                                query = 'SELECT * from room'
                                c12.execute(query)
                                all_rooms = c12.fetchall()
                                print(all_rooms)
                            except pymysql.Error as e:
                                code, msg = e.args
                                msg = e.args[1]
                                code = e.args[0]
                                print("Error retrieving data from the db", code, msg)

                            while True:
                                try:
                                    print("\n-- Device Relocation -- ")
                                    device = input("What device are you relocating (id): ")
                                    old_room = input("What is the old room of this device: ")
                                    old_hosp = input("What is the old hospital of this device: ")
                                    new_room = input("What is the new room of this device: ")
                                    new_hosp = input("What is the new hospital of this device: ")

                                    c13 = connection.cursor()
                                    c13.callproc('moveDevice', [device,old_room, old_hosp, new_room, new_hosp])
                                    for row in c13.fetchall():
                                        print(row)
                                    c13.close()
                                    print("Successful Relocation")
                                    break  # Break out of the loop if no error occurs

                                except pymysql.Error as e:
                                    code, msg = e.args
                                    print("Error retrieving data from the database:", code, msg)
                                    print("Please try again.\n")


                        elif prompt.lower() == "no":
                            print("Returning to main menu...")
                            break

                        filter_menu = False
                        break

        # Option 3: Perform administrative tasks
        elif option == "3":
            if not authenticated:
                # Initialize variables to store user input
                incorrect_attempts = 0
                ausername = ""
                apassword = ""

                # Loop until valid credentials are provided or maximum attempts are reached
                while ausername != admin_username or apassword != admin_password:
                    # Prompt user for username and password
                    print("\n-------- Admin Login --------")
                    ausername = input("Enter admin username: ")
                    apassword = input("Enter admin password: ")

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
                print("\n-------- Administration Tasks --------")
                # Add your code for the administrative tasks here
                # Add your code for the administrative tasks here
                print("\nPlease select an option:")
                print("1. Add Room")
                print("2. Remove Room")
                print("3. Add Hospital")
                print("4. Remove Hospital")
                print("0. Exit")
                option_choice = input("Enter your choice (0-4): ")

                pass

                # After performing administrative tasks, give the option to go back to the main menu or exit
                while True:
                    print("\nDo you want to return to main menu or exit")
                    admin_option = input(
                        "Please select a valid option (menu/exit):  ").lower().strip()
                    if admin_option == "menu":
                        break
                    elif admin_option == "exit":
                        print("Exiting the code...")
                        exit()
                    else:
                        print("Invalid option. Please choose again.")

        # Option 4: View Your Patients and associated code
        elif option == "4":
            patient_menu = True
            while patient_menu:
                print("\n-- Your Patient(s) --")
                try:
                    c7 = connection.cursor()
                    c7.callproc(
                        'filterPatient', [
                            d_id])
                    all_patients = c7.fetchall()
                    for row in all_patients:
                        print(row)
                except pymysql.Error as e:
                    code, msg = e.args
                    print("Error retrieving data from the database:", code, msg)

                # If there are no patients print so
                if not all_patients:
                    print("No patients found.")

                print("\n-------- Patient Menu --------")
                print("Select an option:")
                print("1. Add a patient")
                print("2. Delete a patient")
                print("3. Select a specific patient for further operations ")
                print("4. Update patient check out time ")
                print("0. Go Back to Main Menu")
                sub_option = input("Enter your choice (0-4): ")

                # Patient Option 1: Add patient
                if sub_option == "1":
                    while True:
                        try:
                            print("\nAdd Patient")
                            c10 = connection.cursor()
                            c10.callproc(
                                'availableRooms', [d_id])
                            available_rooms = c10.fetchall()
                            print("These are the available rooms in the current doctor hospital you can assign patient to")
                            print(available_rooms)
                        except pymysql.Error as e:
                            code, msg = e.args
                            print("Error retrieving data from the database:", code, msg)

                        while True:
                            # input
                            values = input("Enter patient first name, last name, check in, and available room number separated by commas (e.g Ace, Ventura, 2023-06-20 14:30:00, 101): ")
                            value_list = values.split(",")
                            pt_fname, pt_lname, pt_in, room_n = [value.strip() for value in value_list]
                            # print(pt_fname, pt_lname, pt_in, room_n)

                            # Preliminary data validation
                            if len(value_list) != 4:
                                print("Invalid number of values. Please enter 4 values.")
                                continue

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

                            # Ensure they choose correct room from available rooms
                            for row in available_rooms:
                                # print(type(row['pt_id']))
                                if room_n.isdigit() and int(room_n) == row['room_num']:
                                    continue

                            break

                        break

                    try:
                        c11 = connection.cursor()  # shouldn't reuse cursors
                        # calling procedure by its string
                        c11.callproc(
                            'createPatient', [pt_fname, pt_lname, pt_in, room_n, d_id])  # second part department, is the list of parameters to the specific proceudre get_department
                        print("Patient Created")
                    except pymysql.Error as e:
                        code, msg = e.args
                        print("Error retrieving data from the database:", code, msg)

                # Patient Option 2: Delete a paitient that exists
                elif sub_option == "2":
                    b = True
                    if not all_patients:
                        print("No patients to delete")
                        b = False
                        continue

                    # Enter from all_patients that exist
                    while b == True:
                        print("\nDelete Patient")
                        pt_id = input("Enter patient id you want to delete from your patients: ")
                        match_found = False

                        # Conditional check
                        for row in all_patients:
                            if pt_id.isdigit() and int(pt_id) == row['pt_id']:
                                match_found = True
                                break

                        if match_found:
                            c8 = connection.cursor()
                            c8.callproc(
                                'removePatient',
                                [pt_id, ])
                            c8.close()
                            print("The following patient has been deleted:", pt_id)
                            b = False
                            break
                        else:
                            print("Error: Patient doesn't match your list. Please try again.")
                    break

                # Patient option 3: SELECT THE PATIENT YOU WANT TO SEE FOR FURTHER OPERATIONS
                elif sub_option == "3":
                    if not all_patients:
                        print("No patients found.")
                        print("Can't update check out time, add examination, or archive examinations.")
                        break

                    while True:
                        print("\nSelect Patient")
                        pt_id = input("Enter patient id you want to examine from list above: ")
                        match_found = False

                        # Data validation that it is one of your patients
                        for row in all_patients:
                            if pt_id.isdigit() and int(pt_id) == row['pt_id']:
                                match_found = True
                                break

                        if match_found:
                            print("You have selected patient:", pt_id)
                            try:
                                print("-- Patient Information -- ")
                                c18 = connection.cursor()
                                c18.callproc('patientInfo', [pt_id])
                                for row in c18.fetchall():
                                    print(row)
                                c18.close()
                            except pymysql.Error as e:
                                code, msg = e.args
                                print("Error retrieving data from the database:", code, msg)

                            try:
                                print("\n-- All Examinations for Patient ", pt_id,"--")
                                c19 = connection.cursor()
                                c19.callproc('allExam', [pt_id])
                                all_Exam1 = c19.fetchall()
                                for row in all_Exam1:
                                    print(row)
                            except pymysql.Error as e:
                                code, msg = e.args
                                print("Error retrieving data from the database:", code, msg)



                            patient_options = True
                            while patient_options:
                                # Display additional options for the selected patient
                                print("\n-------- Additional Patient Options --------")
                                print("1. View Number of Exams")
                                print("2. Add Examination ")
                                print("3. Archive Examinations")
                                print("0. Main Menu")

                                patient_option = ""
                                while patient_option not in ["0", "1", "2", "3"]:
                                    patient_option = input("Please enter a valid choice (0-3): ")

                                # Patient Option 1: Look at num Exam compared to other patients
                                if patient_option == "1":
                                    try:
                                        c21 = connection.cursor()
                                        c21.callproc('initialize_num_exam')
                                    except pymysql.Error as e:
                                        code, msg = e.args
                                        print("Error retrieving data from the database:", code, msg)

                                    try:
                                        c22 = connection.cursor()
                                        print("Number of Exams for all Patients")
                                        query = 'SELECT pt_id, numExams from patient';
                                        c22.execute(query)
                                        all_NumExam = c22.fetchall()
                                        # print(type(all_NumExam))
                                        for row in all_NumExam:
                                            # print(type(row))
                                            print(row)

                                        pt_ids = [row['pt_id'] for row in all_NumExam]
                                        num_exams = [row['numExams'] for row in all_NumExam]
                                        # Create the pie chart
                                        plt.pie(num_exams, labels=pt_ids, autopct='%1.1f%%')
                                        plt.title('Number of Exams per pt_id')

                                        # Show the pie chart
                                        plt.show()
                                    except pymysql.Error as e:
                                        code, msg = e.args  # this gives the message e.args[0] gives the state
                                        msg = e.args[1]
                                        code = e.args[0]
                                        print("Error retrieving data from the db", code, msg)








                                # Patient Option 2: Add New Examination for Your Patient
                                elif patient_option == "2":
                                    while True:
                                        print("\nAdd Examination")
                                        values = input(
                                            "Enter patient symptom, medical device, examDate (e.g smpytom, 1007, 2023-06-20 14:30:00): ")
                                        value_list = values.split(",")

                                        if len(value_list) != 3:
                                            print("Invalid number of values. Please enter 4 values.")
                                            continue

                                        symp, m_device, examDate = [value.strip() for value in value_list]
                                        print(symp, m_device, examDate)

                                        if not symp.isalpha() or not symp:
                                            print("Invalid value: symptom must be a non-empty string.")
                                            continue

                                        if not m_device.isdigit() or not m_device:
                                            print("Invalid value: pt_lname must be a non-empty string.")
                                            continue

                                        try:
                                            datetime.strptime(examDate, "%Y-%m-%d %H:%M:%S")
                                        except ValueError:
                                            print(
                                                "Invalid value: pt_in must be a valid datetime in the format 'YYYY-MM-DD HH:MM:SS'.")
                                            continue


                                        try:
                                            c15 = connection.cursor()
                                            c15.callproc(
                                                'addExam', [symp, pt_id, m_device, examDate
                                                    ])
                                            all_patients = c15.fetchall()
                                            for row in all_patients:
                                                print(row)
                                            print("Successful Exam Entry")
                                            break

                                        except pymysql.Error as e:
                                            code, msg = e.args
                                            print("Error retrieving data from the database:", code, msg)

                                    # Update the list of patients after adding the examination
                                    try:
                                        c7 = connection.cursor()
                                        c7.callproc('filterPatient', [d_id])
                                        all_patients = c7.fetchall()
                                        for row in all_patients:
                                            print(row)
                                    except pymysql.Error as e:
                                        code, msg = e.args
                                        print("Error retrieving data from the database:", code, msg)

                                # Code for Option 3: Archive option
                                elif patient_option == "3":
                                    try:
                                        print("-- All Examinations for Patient", pt_id, "--")
                                        c16 = connection.cursor()
                                        c16.callproc('allExam', [pt_id])
                                        all_Exam = c16.fetchall()
                                        for row in all_Exam:
                                            print(row)
                                    except pymysql.Error as e:
                                        code, msg = e.args
                                        print("Error retrieving data from the database:", code, msg)
                                        reprompt = "main"
                                        break

                                    while True:
                                       try:
                                           print("\nArchive examination")
                                           date = input("Choose a date where all examination that precede are archived (e.g. 2023-07-20 00:00:00): ")
                                           c17 = connection.cursor()
                                           c17.callproc('ArchiveOldExaminations', [pt_id, date])
                                           print("Successful Archive")
                                           break
                                       except pymysql.Error as e:
                                           code, msg = e.args
                                           print("Error retrieving data from the database:", code, msg)

                                elif patient_option == "0":
                                    reprompt = "main"
                                    break

                                reprompt = ""
                                while reprompt not in ["option", "select", "main"]:
                                    reprompt = input(
                                        "\nDo you want to go back to select a different option for the specified patient,\n select a new patient, or go back to the main menu? (option/select/main): ")


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

                # Option 4: Where we're able to change the check out time for any patient
                elif sub_option == "4":

                    while True:
                        print("\nUpdate Check Out")
                        patient = input("Select your patient id that you want to insert check out time for: ")
                        match_found3 = False

                        for row in all_patients:
                            if patient.isdigit() and int(patient) == row['pt_id']:
                                match_found3 = True
                                break
                            else:
                                print("Invalid option. Not your patient")

                        if match_found3:
                            try:
                                check_out = input("Select Check Out Time (e.g. 2023-06-20 14:30:00): ")
                                c14 = connection.cursor()
                                c14.callproc(
                                    'enterCheckout', [
                                        patient, check_out])
                                print("Update CheckOut Time Successful")
                                break
                            except pymysql.Error as e:
                                code, msg = e.args
                                print("Error retrieving data from the database:", code, msg)
                                break

                # Go back to the suboptions menu
                elif sub_option == "0":

                    patient_menu = False

                else:
                    print("Invalid choice. Please select a valid option.")

        elif option == "0":
            # Option 0: Exit the program
            print("Exiting the program. Goodbye!")
            main_menu = False

        else:
            # Invalid option
            print("Invalid option. Please choose again.")

if __name__ == '__main__':
    work('medical_device')