earth_alhpabet = 'abcdefghijklmnopqrstuvwxyz{}_ '

zoom_alphabet = 'zoumna'

keys = # censored # 

a, b, c = keys[0], keys[1], keys[2]

translated_zoom_alphabet = [ (zoom_alphabet[(len(earth_alhpabet) - i) % a] + zoom_alphabet[(len(earth_alhpabet) - i) % b] + zoom_alphabet[(len(earth_alhpabet) - i) % c])
																																		 for i in range(len(earth_alhpabet)) ]
dict = { earth_alhpabet[i]:translated_zoom_alphabet[i] for i in range(30) }

text = input()

encrypted =  ''

for i in text:
		encrypted+=dict[i]

print(encrypted)