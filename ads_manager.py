#Doc at https://ads.readthedocs.io/en/latest/
import ads
ads.config.token = 'secret token'
import csv

def show_input_file(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} citation corresponds to ADS code {row[1]}.')
                line_count += 1
    print(f'Found {line_count} lines.')

def check_duplicates(filename):
    references = set()
    bibcodes = set()
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                reference, bibcode = row[0], row[1]
                if reference in references:
                    print ("reference", reference, " is already present!")
                else:
                    references.add(reference)
                if bibcode in bibcodes:
                    print ("bibcode", bibcode, " is already present!")
                else:
                    bibcodes.add(bibcode)
            line_count += 1
    print(f'Found {line_count} lines.')

def read_papers(filename):
    papers = {}
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                reference = row[0]
                if reference[0] != "#":
                    bibcode = row[1]
                papers[reference] = bibcode
            line_count += 1
    return dict(sorted(papers.items(), key=lambda x: x[0].lower()))

filename = "2021-handbook.csv"
#filename = "2020-positron-pwne.csv"
#filename = "2021-stochastic-sources.csv"

#show_input_file(filename)

check_duplicates(filename)

papers = read_papers(filename)

bibcodes = list(papers.values())

bibtex = ads.ExportQuery(bibcodes=bibcodes, format='bibtex').execute()

for reference in papers.keys():
    bibcode = papers[reference]
    bibtex = bibtex.replace(bibcode, reference, 1)

bibname = filename.replace(".csv", ".bib")

f = open(bibname, "w")
f.write(bibtex)
f.close()
