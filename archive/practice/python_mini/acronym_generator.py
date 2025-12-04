# Acronym Generator

text = str(input("Enter a String\n"))
text = text.split()
acronym = ""
for i in text:
    acronym = acronym+str(i[0]).upper()
print(acronym)