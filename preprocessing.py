# e removed self-reported posts from the datasets and kept the most recent 1000 posts. We then performed lowercasing to standardise the text. URLs, HTML tags, “rt” notation, mentions of other users, and hashtag symbols were removed. However, the content of the hashtags was kept.


# 1. Extract emoji from text
# 2. Remove markdown (e.g. # Heading, **Bold**, *Italic*, > Quote, 1. Item, - Item, `Code`, ---, [Link text](URL), ![Alt text](URL))
# 3. Remove newline and tab characters
# 4. Remove URLs, HTML tags, “rt” notation, mentions of other users, and hashtag symbols
# 5. Remove emoji
# 6. Encode to utf-8
# 7. Keep punctuation
# 8. Remove punctuation

# including RT or not
# 
import re

emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+", flags=re.UNICODE)

at_hash_pattern = re.compile(r'\s([@#])(?!\w+\b)')
retweet_pattern = re.compile(r'\b(retweet)\b')

def extract_emoji(text):
    return ' '.join(emoji_pattern.findall(text))

# for reddit or stackoverflow
def remove_markdown(text):
    
    text = re.sub(r'^#{1,6}\s+', '', text) # Remove headings (e.g. ## Heading)
    text = re.sub(emoji_pattern, '', text) # Remove emoji
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text) # Remove bold (e.g. **Bold**)
    text = re.sub(r'\*(.*?)\*', r'\1', text) # Remove italic (e.g. *Italic*)
    text = re.sub(r'^\>\s+', '', text, flags=re.MULTILINE) # Remove blockquote (e.g. > Quote)
    text = re.sub(r'^\d\.\s+', '', text, flags=re.MULTILINE) # Remove ordered list (e.g. 1. Item)
    text = re.sub(r'^\-\s+', '', text, flags=re.MULTILINE) # Remove unordered list (e.g. - Item)
    text = re.sub(r'`(.+?)`', r'\1', text) # Remove code (e.g. `Code`)
    text = re.sub(r'^\s*---\s*$', '', text, flags=re.MULTILINE) # Remove horizontal rule (e.g. ---)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', text) # Remove link (e.g. [Link text](URL))
    text = re.sub(r'\!\[(.*?)\]\((.*?)\)', r'', text) # Remove image (e.g. ![Alt text](URL))
    text = re.sub(r'#(\S+)', r'\1', text) # Remove hashtag symbol (e.g. #hashtag)
    text = re.sub(r'\n', ' ', text) # Remove newline characters
    text = re.sub(r'\t', ' ', text) # Remove tab characters
    # Remove URLs, HTML tags
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\S+', '', text)
    text = re.sub(r'bit.ly\S+', '', text)
    text = re.sub(r'bitly\S+', '', text)
    text = re.sub(r'pic.twitter\S+', '', text)
    text = re.sub(r'youtube.\S+', '', text)
    text = re.sub(r'<.*?>', '', text) # remove html tags
    text = text.strip() # Remove leading and trailing whitespace

    return text


def remove_twitter(text):

    # replace usernames with [user]
    text = re.sub(r'@\S+', '@user', text) # replace usernames with @user, @ and user exist in the vocab of sentence transformer
    text = re.sub(at_hash_pattern,'',text) # remove @ and # symbols
    text = re.sub(retweet_pattern,'rt',text) # replace the word 'retweet' with 'rt', rt exist in the vocab of sentence transformer but not retweet

    # since it has previously removed the emoji, we don't need to remove it again, but to play safe, we can encode it to utf-8
    text = text.encode('utf-8', errors='ignore') # usually there's error involve with emoji, so we need to encode it to utf-8

    return text


if __name__ == '__main__':
    text = 'RT @user: This is a test tweet with a link https://t.co/123456 and an emoji 😂'

    # extract emoji first
    emojis = extract_emoji(text)
    # remove markdown
    text = remove_markdown(text)
    # remove twitter specific symbols
    text = remove_twitter(text)
    
    # print emojis first and then text in the same line
    print(emojis, text)
