import whoosh.index as index
from whoosh.fields import *
from whoosh.qparser import MultifieldParser
from whoosh import scoring

w = scoring.BM25F(B=0.75, content_B=1.0, K1=1.5)
fieldnames = ["bill_text", "bill_title", "year", "sponsor_name", "subject"]
boosts = {"bill_text": 1, "bill_title": 2.5, "year": 0, "sponsor_name": 0, "subject": 2.0}

#load index:
ix = index.open_dir("final_index")
writer = ix.writer()

#search:
def results(q):
	hits = []
	with ix.searcher(weighting=w) as searcher:
		query = MultifieldParser(fieldnames, ix.schema, fieldboosts=boosts).parse(q)
		results = searcher.search_page(query, 1, pagelen=10)
		print "\n" + str(len(results)) + " results found!"
		print "Displaying top ten results:"
		for result in results:
			if result["house_or_senate"] == "h":
				hs = "hr"
				billnum = "hr" + str(result["bill_number"])
				isih = "ih"
			elif result["house_or_senate"] == "s":
				hs = "s"
				billnum = "s" + str(result["bill_number"])
				isih = "is"
			
			url = "https://www.govtrack.us/data/congress/" + str(result["congress_number"]) + "/bills/" + hs + "/" + hs + str(result["bill_number"]) + "/text-versions/" + isih + "/document.txt" 
			hits.append({"bill_title":result["bill_title"], "year":result["year"], "url":url, "sponsor_name":result["sponsor_name"]})
	return hits

query = raw_input("\nSearch for a term in bill text: ")
query = query.lstrip()

print results(query)