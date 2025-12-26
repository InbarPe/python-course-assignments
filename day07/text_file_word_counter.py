from collections import defaultdict
import string
import os

def count_words(filename):
    word_counts = defaultdict(int)

    # chars to remove (punctuation)
    translator = str.maketrans("", "", string.punctuation)

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            # remove punctuation and lowercase
            line = line.translate(translator).lower()

            words = line.split()

            for word in words:
                word_counts[word] += 1

    return word_counts

# get the file path
base = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base, "text_file.txt")

# --- run the function ---
counts = count_words(path)

# Print results sorted by frequency:
for word, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{word}: {count}")
