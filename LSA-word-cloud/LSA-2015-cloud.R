# Generate a word cloud from csv of LSA title word frequencies.
library(wordcloud)

# Read in the data:
lsa <- read.csv("LSA-freq.csv")

# Plot a word cloud!
wordcloud(lsa$word, lsa$count, 			# tell it where words & frequencies are
		  scale=c(3, .5), 				# range of word sizes
		  min.freq=5, 					# only plot words with more than 5 tokens
		  random.color=TRUE, 			# color isn't mapped to frequency
		  random.order=FALSE,			# most frequent words in the middle
		  colors=brewer.pal(4, "BrBG"))	# use the brown & blue-green palette
		  
# Plotting is random, so if you generate enough plots there will be a few 
# nice-looking ones. Lowering the frequency minimum makes denser and larger plots;
# the data output from title_processor.py isn't 100% cleaned up though, so there
# is probably some weirdness at n=2 or less.

