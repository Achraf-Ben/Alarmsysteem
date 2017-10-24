from ipscanner import doListScan

x = True
y = 0
while y < 255:
    ip = "192.168.42." + str(y)
    doListScan(ip)
    y = y + 1
