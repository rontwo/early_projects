//Rudimentary program that parses a text file and tallies up the wordcount for each word

#filepath stored in variable 'file'
file = '/Users/ron_two/Documents/python_work/practice.rtf'

#open file, store each string as separate elements in a list called 'words'
read_file = open(file, 'r', encoding = "utf-8")
text = read_file.read()
words = text.split()
counts = dict()

#delete all header data (if any)
target_word = 'the'
try:
	target_index = words.index(target_word)
except ValueError:
	target_index = None

del words[:target_index]

#initialize dictionary, where key = word and value = count of word
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
print('The most common word is: "' + bigword + '" with a frequencey of: ' + str(bigcount) + ' occurences.')
