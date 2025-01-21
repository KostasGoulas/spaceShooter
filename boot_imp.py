
def is_server_open():
    server_file = open("Server", "r+")
    an = server_file.read()
    server_file.close()
    if an == 'o' :
        return True
    return False

def server_open():
    server_file = open("Server", "w+")
    server_file.write("o")
    server_file.close()

def server_close():
    server_file = open("Server", "w+")
    server_file.write("c")
    server_file.close()

def set_connection_to_zero():
    confile = open("Connections", "w+")
    confile.write("0")
    confile.close()

def add_connection():
    confile = open("Connections", "r+")
    if confile.read() == "1":
        confile.close()
        confile = open("Connections", "w+")
        confile.write("2")
    else :
        confile.close()
        confile = open("Connections", "w+")
        confile.write("1")
    confile.close()

def connections_count():
    confile = open("Connections", "r+")
    an = confile.read()
    confile.close()
    if an == "1":
        return 1
    elif an == "2":
        return 2
    else :
        return 0
    
def boot() :
    set_connection_to_zero()
    server_close()