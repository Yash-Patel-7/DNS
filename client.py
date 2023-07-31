import socket 
import sys

def main(): 
	# parse command line arguments for LS hostname and port
	lsHostname = sys.argv[1]
	lsListenPort = int(sys.argv[2])

	# open input file and output file
	with open("PROJ2-HNS.txt", "r") as input:
		with open("RESOLVED.txt", "a") as output:
			# read each line of input file
			for domain in input:

				# remove trailing whitespace from domain
				domain = domain.rstrip()

				# create client socket and connect to LS
				client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				client.connect((lsHostname, lsListenPort))

				# send domain name to LS and receive information
				client.sendall(domain.encode("utf-8"))
				msg = client.recv(1024).decode("utf-8")

				# shut down and close client connection
				client.shutdown(socket.SHUT_RDWR)
				client.close()

				# write received information to output file
				output.write(msg + "\n")

if __name__ == "__main__" :
	main()
