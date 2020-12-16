# ĐỒ ÁN MẠNG MÁY TÍNH
# ĐỒ ÁN SOCKET

# Sinh viên thực hiện: Bùi Quang Bảo
# MSSV: 19120454

# Ngôn ngữ: Python
# Quá trình chạy của chương trình được in ra console để dễ dàng theo dõi
# File báo cáo, ảnh chụp màn hình console và video demo đã đính kèm

# Lưu ý, nên cẩn thận với chức năng "Auto format" code của một số IDE ạ, 
# vì Python khá nhạy cảm với dấu cách và tab, một số IDE tự động format lại code, 
# vô tình thay đổi khiến cho chương trình bị lỗi, em đã bị trường hợp này.

import socket

# Hàm tạo socket server
def CreateSocketServer(host, port):
    # AF là viết tắt của Address Family
    # INET là INTERNET
    # AF_INET - IPv4
    # SOCK_STREAM - TCP
    Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # "Bind" 1 ip và 1 port
    # Trong đồ án, em sẽ bind localhost với port 8080
    Server.bind((host, port))
    # Server sẽ chuẩn bị 1 queue (hàng đợi) gồm 5 để tránh trường hợp quá tải do nhiều kết nối tới cùng 1 lúc
    Server.listen(5)
    return Server


# Hàm phụ trợ
def ReadRequest(Client):
    # print(">>>>>>>>> Error here <<<<<<<<<<")
    print("\t> Ham ReadRequest(Client):")
    request = ""
    timeOut = 5
    Client.settimeout(timeOut)  # Thông báo lỗi nếu hết thời gian chờ (giây)
    try:
        request = Client.recv(1024).decode()
        while (request):
            request = request + Client.recv(1024).decode()
    except socket.timeout:
        if not request:
            print("\t\t[Timeout] Sau", timeOut, "giay, da khong nhan duoc du lieu!")
    finally:
        print("\t\t[HTTP Request returned!]")
        # print(request)
        return request
# Kết nối client với server & đọc HTTP Request
def ReadHTTPRequest(Server):
    # print(">>>>>>>>> Error here <<<<<<<<<<")
    print("> Ham ReadHTTPRequest(Server):")
    request = ""
    while (request == ""):
        Client, address = Server.accept()
        print("\tClient da ket noi toi Server! Address:", address)
        request = ReadRequest(Client)
    return Client, request



# Bổ trợ 1 cho hàm MoveHomePage
def SendIndexCase1(Client): 
	print("\t> Ham SendIndexCase1(Client):")
	f = open ("index.html", "rb")
	L = f.read()
	header ="""HTTP/1.1 200 OK
Content-Length: %d

"""%len(L)
	print("\t\tSend header (+ html code): ")
	print(header)
	header += L.decode()
	Client.send(bytes(header, 'utf-8'))
# Bổ trợ 2 cho hàm MoveHomePage
def SendIndexCase2(Client):
	print("\t> Ham SendIndexCase2(Client):")
	header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/index.html

"""
	print("\t\tSend header (+ html code): ")
	print(header)
	Client.send(bytes(header,'utf-8'))
# Gửi HTTP Response & đóng server
def MoveHomePage(Server, Client, Request):
    # print(">>>>>>>>> Error here <<<<<<<<<<")
    print("\n> Ham MoveHomePage(Server, Client, Request):")
    print("\tCase 1: GET /index.html HTTP/1.1")
    SendIndexCase1(Client)
    print("\t\t[Sent to client. Done!]")
    Server.close()
    return True




# Hàm kiểm tra login
def CheckUsernamePassword(Request):
    print("\n> Ham CheckUsernamePassword(Request):")
    if "POST / HTTP/1.1" not in Request:
        print("\n\t[POST / HTTP/1.1 not in Request -> return False]")
        return False
    if "Username=admin&Password=admin" in Request:
        print("\t[Check username and password: True]")
        return True
    else:
        print("\t[Check username and password: False]")
        return False



# Bổ trợ cho hàm DirectTo404Page
def SendFile404(Client):
    # print(">>>>>>>>> Error here <<<<<<<<<<")
    print("\n> Ham SendFile404(Client):")
    f = open("404.html", "rb")
    L = f.read()
    header = """HTTP/1.1 404 Not Found
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

""" % len(L)
    print("\tSend header (+ html code): ")
    print(header)
    header += L.decode()
    Client.send(bytes(header, 'utf-8'))

# Hàm này được gọi khi mà client gõ sai username và password
def DirectTo404Page(Server, Client):
    print("\n> Ham DirectTo404Page(Server, Client):")
    #
    header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/404.html

"""
    print("\tSend header (+ html code): ")
    print(header)
    Client.send(bytes(header, "utf-8"))
    Server.close()
    #
    Server = CreateSocketServer("localhost", 8080)
    Client, Request = ReadHTTPRequest(Server)
    if "GET /404.html HTTP/1.1" in Request:
        SendFile404(Client)
        print("\t\t[Sent to client. Done!]")
    Server.close()

# Bổ trợ cho hàm DirectToInfoPage
def SendFileInfo(Client):
    # print(">>>>>>>>> Error here <<<<<<<<<<")
    print("\n> Ham SendFileInfo(Client):")
    f = open("information.html", "rb")
    L = f.read()
    header = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

""" % len(L)
    print("\tSend header (+ html code): ")
    print(header)
    header += L.decode()
    Client.send(bytes(header, 'utf-8'))

# Hàm gửi file hình ảnh
# Bổ trợ cho hàm DirectToInfoPage
def SendFileImage(Client, imageFileName):
    print("\n> Ham SendFileImage(Client, imageFileName):")
    with open(imageFileName, 'rb') as f:
        L = f.read()
        header = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

""" % len(L)
        print("\tSend header (+ html code): ")
        print(header)
        header = bytes(header, 'utf-8') + L
        Client.send(header)

# Hàm này được gọi khi mà client nhập đúng username và password
def DirectToInfoPage(Server, Client):
    # print(">>>>>>>>> Error here <<<<<<<<<<")
    print("\n> Ham DirectToInfoPage(Server, Client):")
    #
    header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/information.html

"""
    print("\tSend header (+ html code): ")
    print(header)
    Client.send(bytes(header, "utf-8"))
    Server.close()
    #
    Server = CreateSocketServer("localhost", 8080)
    Client, Request = ReadHTTPRequest(Server)
    if "GET /information.html HTTP/1.1" in Request:
        SendFileInfo(Client)
        SendFileImage(Client, "image.jpg")
    Server.close()
    # Gọi hàm gửi file hình ảnh
    Server = CreateSocketServer("localhost", 8080)
    Client, Request = ReadHTTPRequest(Server)
    SendFileImage(Client, "image.jpg")
    print("\t\t[Sent to client. Done!]")
    Server.close()


# Hàm main
if __name__ == "__main__":
    # while True:
        print("\nSTART 1 ====================================================\n")
        print("1. Tra ve index.html khi truy cap server:")
        # Tạo 1 socket server
        Server = CreateSocketServer("localhost", 8080)
        # Kết nối client với server & đọc HTTP Request
        Client, Request = ReadHTTPRequest(Server)
        # Gửi HTTP Response, chuyển tới index.html & đóng server
        MoveHomePage(Server, Client, Request)
        print("END 1 ======================================================\n")

        print("\nSTART 2 ====================================================")
        # Tạo 1 socket server
        Server = CreateSocketServer("localhost", 8080)
        # Kết nối client với server & đọc HTTP Request
        Client, Request = ReadHTTPRequest(Server)
        # Kiểm tra login
        if CheckUsernamePassword(Request) == True:
            DirectToInfoPage(Server, Client)
        else:
            DirectTo404Page(Server, Client)
        print("END 2 ======================================================\n")