import whoosh.index as index
from whoosh.fields import *
from whoosh.qparser import MultifieldParser
from whoosh import scoring

w = scoring.BM25F(B=0.75, content_B=1.0, K1=1.5)
fieldnames = ["bill_text", "bill_title", "year", "sponsor_name"]
boosts = {"bill_text": 1, "bill_title": 2.5, "year": 0, "sponsor_name": 2}

#load index:
ix = index.open_dir("final_index")
writer = ix.writer()
print ix

user_input = raw_input("\nSearch for a term in bill text: ")

#search:
with ix.searcher(weighting=w) as searcher:
	query = MultifieldParser(fieldnames, ix.schema, fieldboosts=boosts).parse(user_input)
	results = searcher.search(query)
	print "\n" + str(len(results)) + " results found!"
	print "Displaying top ten results:"
	for i in range(0,10):
		if results[i]["house_or_senate"] == "h":
			hs = "hr"
			billnum = "hr" + str(results[i]["bill_number"])
			isih = "ih"
		elif results[i]["house_or_senate"] == "s":
			hs = "s"
			billnum = "s" + str(results[i]["bill_number"])
			isih = "is"
		try:
			url = "https://www.govtrack.us/data/congress/" + str(results[i]["congress_number"]) + "/bills/" + hs + "/" + hs + str(results[i]["bill_number"]) + "/text-versions/" + isih + "/document.txt" 
			print "     " + results[i]["bill_title"]
			print "     " + url
		except:
			continue
	print "\n"