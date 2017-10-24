disarm = 1
while disarm >= 1:
    disarmed = open("disarmed.txt", 'w')
    disarmed.write("Disarmed\n" + str(disarm))
    disarm += 1
    disarmed.close()
