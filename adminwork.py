print("2. Remove Room")
print("3. Add Hospital")
print("4. Remove Hospital")
print("5. Add Patient Entry")
print("6. Remove Patient")
print("5. Add Medical Device Entry")
print("6. Edit Medical Device Entry")
print("7. Remove Medical Device")
print("8. View All Rooms")
print("9. View All Hospitals")
print("10. View All Medical Devices")
print("0. Exit")
option_choice = input("Enter your choice (0-4): ")
option_choice = input("Enter your choice (0-10): ")

# Option to add a room
if option_choice == "1":
    try:
        con = connection.cursor()


@ @-167

, 11 + 172, 14 @ @


def work(name):
    hosp_id = input("Please enter the corresponding hospital id: ")

    con.callproc("addRoom", (room_num, hosp_id))

    print("Your room has been added")

    con.close()

except:
print('Error: %d: %s' % (e.args[0], e.args[1]))

# Option to delete a room
elif option_choice == "2":
try:
    con2 = connection.cursor()


@ @-180

, 11 + 188, 14 @ @


def work(name):
    hosp_id = input("Please enter the corresponding hospital id: ")

    con2.callproc("removeRoom", (room_num, hosp_id))

    print("Your room has been removed")

    con2.close()

except:
print('Error: %d: %s' % (e.args[0], e.args[1]))

# Option to add a hospital
elif option_choice == "3":
try:
    con3 = connection.cursor()


@ @-198

, 55 + 209, 128 @ @


def work(name):
    hosp_zipcode = input("Please enter the new hospital's zipcode: ")

    con3.callproc("addHosp", (hosp_id, hosp_name, hosp_streetnum, hosp_streetname, hosp_town, hosp_state, hosp_zipcode))

    print("Your hospital has been added")

    con3.close()

except:
print('Error: %d: %s' % (e.args[0], e.args[1]))

# Option to delete a hospital
elif option_choice == "4":
try:
    con4 = connection.cursor()

    hosp_id = input("Please enter the hospital id that you wish to delete: ")

    con4.callproc("removeHospital", (hosp_id))

    print("Your hospital has been removed")
    con4.close()
except:
    print('Error: %d: %s' % (e.args[0], e.args[1]))

    # Option to add a device
elif option_choice == "5":
try:
    con5 = connection.cursor()

    pid = input("Please enter the new patient's id: ")
    pfname = input("Please enter the patient's first name: ")
    plname = input("Please enter the patient's last name: ")
    cintime = input("Please enter patient's check-in time: ")
    couttime = input("Please enter patient's check-out time: ")
    hospid = input("Please enter the id of the hospital the patient is at: ")
    did = input("Please enter the new device id: ")
    dname = input("Please enter the new device name: ")
    l = input("Please enter the new length of the device: ")
    w = input("Please enter the new width of the device: ")
    h = input("Please enter the new height of the device: ")
    li = input("Please enter the life involvement of the new device: ")
    quant = input("Please enter the quantity of the device: ")
    hospid = input("Please enter the id of the hospital the device is at: ")

    con5.callproc("addPatient", (pid, pfname, plname, cintime, couttime, hospid))

    con5.callproc("createDevice", (did, dname, l, w, h, li, quant, hospid))

    print("Your device has been created")
    con5.close()
except:
    print('Error: %d: %s' % (e.args[0], e.args[1]))

# Option to update a device
elif option_choice == "6":
try:
    con6 = connection.cursor()

    pt_id = input("Please enter the patient id of which you want to delete: ")
    hosp_id = input("Please enter the hospital id of the patient: ")

    con6.callproc("removePatient", (pt_id, hosp_id))

    updated_did = input("Please enter the updated device id: ")
    updated_dname = input("Please enter the updated device name: ")
    updated_l = input("Please enter the updated length of the device: ")
    updated_w = input("Please enter the updated width of the device: ")
    updated_h = input("Please enter the updated height of the device: ")
    updated_li = input("Please enter the updated life involvement of the device: ")
    updated_quant = input("Please enter the updated quantity of the device: ")
    updated_hospid = input("Please enter the updated id of the hospital the device is at: ")

    con6.callproc("updateDevice", (
    updated_did, updated_dname, updated_l, updated_w, updated_h, updated_li, updated_quant, updated_hospid))

    print("Your device has been updated")
    con6.close()
except:
    print('Error: %d: %s' % (e.args[0], e.args[1]))

# Option to delete a device
elif option_choice == "7":
try:
    con7 = connection.cursor()

    device_id = input("Please enter the device id of which you want to delete: ")

    con7.callproc("deleteDevice", (device_id))

    print("Your device has been deleted")
    con7.close()
except:
    print('Error: %d: %s' % (e.args[0], e.args[1]))

# Option to view all rooms
elif option_choice == "8":
try:
    con8 = connection.cursor()

    query1 = "SELECT * FROM room"

    con8.execute(query1)

    for row in con8.fetchall():
        print(row)
    con8.close()
except:
    print('Error: %d: %s' % (e.args[0], e.args[1]))

# Option to view all hospitals
elif option_choice == "9":
try:
    con9 = connection.cursor()

    query2 = "SELECT * FROM hospital"

    con9.execute(query2)

    for row in con9.fetchall():
        print(row)
    con9.close()
except:
    print('Error: %d: %s' % (e.args[0], e.args[1]))

elif option_choice == "10":
try:
    con10 = connection.cursor()

    query3 = "SELECT * FROM med_device"

    con10.execute(query3)

    for row in con10.fetchall():
        print(row)
    con10.close()
except:
    print('Error: %d: %s' % (e.args[0], e.args[1]))

# Exit this menu
elif option_choice == "0":
break