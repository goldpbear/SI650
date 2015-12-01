import sqlite3 as sqlite
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

#create index schema:
schema = Schema(bill_title=TEXT(stored=True), bill_text=TEXT(stored=False), year=NUMERIC(stored=True), month=NUMERIC(stored=True), sponsor_title=TEXT(stored=True), sponsor_state=TEXT(stored=True), sponsor_name=TEXT(stored=True), sponsor_district=NUMERIC(stored=True), congress_number=NUMERIC(stored=True), house_or_senate=TEXT(stored=True), subejct=TEXT(stored=True), day=NUMERIC(stored=True), bill_number=NUMERIC(stored=True))
ix = create_in("final_index", schema)
writer = ix.writer()

count = 1

#open db:
with sqlite.connect(r"billsComplete.db") as con:
	cur = con.cursor()
	cur.execute("SELECT bills.BillTitle, bills.BillText, bills.Year, bills.Month, bills.SponsorTitle, bills.SponsorState, bills.SponsorName, bills.SponsorDistrict, bills.Congressnumber, bills.Houseorsenate, bills.Subject, bills.Day, bills.Billnumber FROM bills")
	rows = cur.fetchall()

	#index:
	for row in rows:
		writer.add_document(bill_title=row[0], bill_text=row[1], year=row[2], month=row[3], sponsor_title=row[4], sponsor_state=row[5], sponsor_name=row[6], sponsor_district=row[7], congress_number=row[8], house_or_senate=row[9], subejct=row[10], day=row[11], bill_number=row[12])
		print count
		count +=1
	writer.commit()

con.close()

user_input = raw_input("\nSearch for a term in bill text: ")

#search:
with ix.searcher() as searcher:
	query = QueryParser("bill_text", ix.schema).parse(user_input)
	results = searcher.search(query)
	print "\n" + str(len(results)) + " results found!"
	print "Displaying top ten results:"
	for i in range(0,10):
		try:
			print "     " + results[i]["bill_title"]
		except:
			continue
	print "\n"