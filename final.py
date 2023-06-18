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
        pass



    """
    print("Several Filter Functionalities")
    try:
        print("Filter by Device Type")
        type = input("Enter Device Type: ")
        c1 = connection.cursor()  # shouldn't reuse cursors
        # calling procedure by its string
        c1.callproc('filterType', (type,))  # second part department, is the list of parameters to the specific proceudre get_department
        for row in c1.fetchall():
            print(row)

    except pymysql.Error as e:
        code, msg = e.args
        print("Error retrieving data from the db", code, msg)


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

    try:
        print("Filter by Doctor First Name, Last Name ")
        first = input("Enter doctor first name: ")
        last = input("Enter doctor last name: ")

        c3 = connection.cursor() #shouldn't reuse cursors
        # calling procedure by its string
        c3.callproc('filterDoctor', [first, last]) #second part department, is the list of parameters to the specific proceudre get_department
        for row in c3.fetchall():
            print(row)
        c3.close()
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



    print("ordering the device by quantity")
    try:
        print("Order Device ")
        c5 = connection.cursor()  # shouldn't reuse cursors
        # calling procedure by its string
        c5.callproc('mostQuantity2', )  # second part department, is the list of parameters to the specific proceudre get_department
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