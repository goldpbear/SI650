import os, shutil

congresses = [103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113]

#iterate through bill text and metadata files for hr or s in all congresses:
for congress in congresses:
	files = os.listdir("bill_text/%s/s" %congress)
	for i in files:
		check = 0
		try:
			#copy metadata files to new location:
			metadata_source = "bill_text/%s/s/" %congress + i + "/data.json" 
			metadata_destination = "preprocessed_text/" + str(congress) + "_s_" + str(i[1:]) + ".json"
			shutil.copy(metadata_source, metadata_destination)

			#open source and destination text files:
			input_filename = "bill_text/%s/s/" %congress + i + "/text-versions/is/document.txt" 
			output_filename = "preprocessed_text/" + str(congress) + "_s_" + str(i[1:]) + ".txt"
			input_file = open(input_filename, "rU")
			output_file = open(output_filename, "w")

			#strip out header:
			for line in input_file:
				if line.replace(" ", "") == "ABILL\n":
					check = 1
					continue
				if check == 1:
					#write file to new destination:
					output_file.write(line)
			output_file.close()

		except:
			continue