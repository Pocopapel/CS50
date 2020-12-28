from cs50 import get_string
text = get_string("Type your text here: ")
lettercount = 0
wordcount = 1
sentencecount = 0
for i in range(len(text)):
    if (text[i].isalpha() == True):
        lettercount += 1
    if (text[i] == " "):
        wordcount += 1
    if (text[i] == "!" or text[i] == "?" or text[i] == "."):
        sentencecount += 1
print("letters:", lettercount)
print("words:", wordcount)
print("sentences:", sentencecount)

CLindex = 0.0588 * (lettercount * 100 / wordcount) - 0.296 * (100 * sentencecount / wordcount) - 15.8

if (CLindex < 1):
    print("Before Grade 1")
elif (CLindex > 15):
    print("Grade 16+")
else:
    print("Grade:", round(CLindex))

