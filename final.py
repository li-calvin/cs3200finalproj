import pymysql

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






    connection.close()


if __name__ == '__main__':
    work('medical_device')