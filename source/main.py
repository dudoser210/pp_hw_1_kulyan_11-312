file = open('task1.py', 'r',encoding='utf-8')
line_var = []
for line in file:
	if 'open' in line:
		line_spl = line.split('open')
		line_spll = line_spl[1].split("'")
		print(line_spll[1])
		