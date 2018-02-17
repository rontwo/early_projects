####Rudimentary program that parses a text file and tallies up the wordcount for each word

#filepath stored in variable 'file'
file = '<<filename>>'

#open file, store each string as separate elements in a list called 'words'
with open(file, 'r') as read_file:
	text = read_file.read()
	words = text.split()

#delete all header data (if any)
target_word = '<<index0_word>>'
try:
	target_index = words.index(target_word)
except ValueError:
	target_index = None

del words[:target_index]

#initialize dictionary, where key = word and value = count of word
counts = {}

for word in words:
	counts[word] = counts.get(word,0) + 1

#print out all words and their respective counts
print('All words in text and their counts are listed below')
print(counts)

print(counts.get('car'))

#find most common word and total count 
bigcount = None
bigword = None

for word,count in counts.items():
	if bigcount is None or count > bigcount:
		bigword = word
		bigcount = count

#print most common word and total count
print('The most common word is: "' + bigword + '" with a frequency of: ' + str(bigcount) + ' occurences.')
