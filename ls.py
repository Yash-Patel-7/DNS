import socket
import sys
import select

def main():
	# create socket server
	ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# bind socket server to socket.gethostname() and port argv[1]
	lsListenPort = int(sys.argv[1])
	ls.bind((socket.gethostname(), lsListenPort))

	# listen for connections up to 1 max
	ls.listen(1)

	# forever do:
	while True:
		# accept connection
		csockid, addr = ls.accept()

		# receive data which is a domain from client
		domain = csockid.recv(1024).decode("utf-8")

		# parse command line arguments for TS1 and TS2
		ts1Hostname = sys.argv[2]
		ts1ListenPort = int(sys.argv[3])
		ts2Hostname = sys.argv[4]
		ts2ListenPort = int(sys.argv[5])

		# create client sockets for ls to connect to TS1 and TS2
		ls_to_ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ls_to_ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# connect to TS1 and TS2
		ls_to_ts1.connect((ts1Hostname, ts1ListenPort))
		ls_to_ts2.connect((ts2Hostname, ts2ListenPort))

		# make client sockets non-blocking
		ls_to_ts1.setblocking(0)
		ls_to_ts2.setblocking(0)
		
		# send domain to both TS1 and TS2
		ls_to_ts1.sendall(domain.encode("utf-8"))
		ls_to_ts2.sendall(domain.encode("utf-8"))

		# check if either TS1 or TS2 has a response using select
		read, write, exception = select.select([ls_to_ts1, ls_to_ts2], [], [], 5)

		# if either TS1 or TS2 has a response, send it to client, otherwise send error message
		if len(read) == 1:
			for ls_client in read:
				data = ls_client.recv(1024).decode("utf-8")
				csockid.sendall(data.encode("utf-8"))
		else:
			csockid.sendall((domain + " - TIMED OUT").encode("utf-8"))
		
		# shut down and close ls client connection to TS1 and TS2
		ls_to_ts1.shutdown(socket.SHUT_RDWR)
		ls_to_ts1.close()
		ls_to_ts2.shutdown(socket.SHUT_RDWR)
		ls_to_ts2.close()

if __name__ == "__main__":
	main()
