#!/bin/python3

import hashlib, asyncio, aiofiles, argparse
from time import time
from colorama import Fore

results = []

attemtps = 1

g = Fore.GREEN

r = Fore.RED

y = Fore.YELLOW

RE = Fore.RESET

parser = argparse.ArgumentParser(description='HASH CRACKER!')

parser.add_argument('-t', '--type', help='REQUIRED TYPE OF HASH!', metavar='', default='md5')

parser.add_argument('-w', '--wordlist', help='REQUIRED LIST OF PASSWORDS!', required=True, metavar='')

parser.add_argument('-l', '--list', help='REQUIRED LIST OF HASH!', required=True, metavar='')

args = parser.parse_args()

async def file_path(path):
	async with aiofiles.open(path, 'r') as lines:
		return [line.strip() for line in await lines.readlines()]


async def md5_check(passwords, hashes):
	global attemtps
	try:
		wordhash = hashlib.md5(passwords.encode()).hexdigest()
		if wordhash == hashes:
			print("{}Password Found: {}{}".format(g, RE, passwords))
			results.append(hashes + " : " + passwords)
		else:
			print("{}[-] Nothing Found! [{}{}{}]{}".format(y, RE, attemtps, y, RE))
	except Exception as e:
		print("{}[e] ERROR: {}{}".format(r, RE, e))

	attemtps += 1


async def sha256_check(passwords, hashes):
	global attemtps
	try:
		wordhash = hashlib.sha256(passwords.encode()).hexdigest()
		if wordhash == hashes:
			print("{}Password Found: {}{}".format(g, RE, passwords))
			results.append(hashes + " : " + passwords)
		else:
			print("{}[-] Nothing Found! [{}{}{}]{}".format(y, RE, attemtps, y, RE))
	except Exception as e:
		print("{}[e] ERROR: {}{}".format(r, RE, e))

	attemtps += 1


async def md5_cracker(wordlist, hashes):
	tasks = []
	async with aiofiles.open(wordlist, 'r') as file:
		lines = await file.readlines()
		for password in lines:
			for hashe in hashes:
				tasks.append(md5_check(password.strip(), hashe))
	await asyncio.gather(*tasks)


async def sha256_cracker(wordlist, hashes):
	tasks = []
	async with aiofiles.open(wordlist, 'r') as file:
		lines = await file.readlines()
		for password in lines:
			for hashe in hashes:
				tasks.append(sha256_check(password.strip(), hashe))
	await asyncio.gather(*tasks)


async def main():

	hashe_file = await file_path(args.list)

	if args.type == 'sha256':
		await sha256_cracker(args.wordlist, hashe_file)

	else:
		await md5_cracker(args.wordlist, hashe_file)

start = time()
asyncio.run(main())
end = time()
print(f"DONE IN {(end - start):.2f}s !")
if results:
	print("{}[*] {}FOUND MATCHES!".format(g, RE))
	for result in results:
		print("{}[+] {}{}".format(g, RE, result))
else:
	print("{}[-] NO MATCHES FOUND!{}".format(r, RE))
