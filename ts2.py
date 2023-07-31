import socket
import sys

def main():
	# create socket server
	ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# bind socket server to socket.gethostname() and port argv[1]
	ts2ListenPort = int(sys.argv[1])
	ts2.bind((socket.gethostname(), ts2ListenPort))

	# listen for connections up to 1 max
	ts2.listen(1)

	# forever do:
	while True:
		# accept connection
		csockid, addr = ts2.accept()

		# receive data which is a domain from LS
		domain = csockid.recv(1024).decode("utf-8")

		# check if domain is in file, with case insensitive, called PROJ2-DNSTS2.txt, in which each line is in the format "domain ip flag"
		with open("PROJ2-DNSTS2.txt", "r") as dns:
			for line in dns:
				# if domain is in file, send the entire line + " IN" to LS
				if domain.lower() == line.split(" ")[0].lower():
					# remove trailing whitespace from line
					line = line.rstrip()
					csockid.sendall((line + " IN").encode("utf-8"))
					break

if __name__ == "__main__":
	main()
