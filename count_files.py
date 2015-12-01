import os

files = os.listdir("preprocessed_text")
print len(files)

for i in range(0,5):
	print files[i]