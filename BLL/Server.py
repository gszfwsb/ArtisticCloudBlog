import BLL.ServerSocket


def main():
    host = "localhost"
    port = 9999
    address = (host, port)
    loginServer = BLL.ServerSocket.socketserver.ThreadingTCPServer(address, BLL.ServerSocket.ServerSocket)
    loginServer.serve_forever()


if __name__ == '__main__':
    main()
