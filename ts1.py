import socket
import sys

def main():
	# create socket server
	ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# bind socket server to socket.gethostname() and port argv[1]
	ts1ListenPort = int(sys.argv[1])
	ts1.bind((socket.gethostname(), ts1ListenPort))

	# listen for connections up to 1 max
	ts1.listen(1)

	# forever do:
	while True:
		# accept connection
		csockid, addr = ts1.accept()

		# receive data which is a domain from LS
		domain = csockid.recv(1024).decode("utf-8")

		# check if domain is in file, with case insensitive, called PROJ2-DNSTS1.txt, in which each line is in the format "domain ip flag"
		with open("PROJ2-DNSTS1.txt", "r") as dns:
			for line in dns:
				# if domain is in file, send the entire line + " IN" to LS
				if domain.lower() == line.split(" ")[0].lower():
					# remove trailing whitespace from line
					line = line.rstrip()
					csockid.sendall((line + " IN").encode("utf-8"))
					break

if __name__ == "__main__":
	main()
