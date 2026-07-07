SECRETS = {}

with open("secrets.txt") as f:
	for line in f:
		s = line.strip().split(' : ')
		if len(s) >= 2:
			SECRETS[s[0]] = s[1]

print("> Secrets established")
