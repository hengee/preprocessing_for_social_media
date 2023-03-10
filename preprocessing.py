import re

EMOJI_PATTERN = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+", flags=re.UNICODE)
AT_HASH_PATTERN = re.compile(r'\s([@#])(?!\w+\b)')
RETWEET_PATTERN = re.compile(r'\b(retweet)\b')

def extract_emoji(text):
    """
    Extract all emoji characters from text.

    Args:
        text: A string containing text to extract emoji from.

    Returns:
        A string containing all extracted emoji characters separated by spaces.
    """
    return ' '.join(emoji_pattern.findall(text))

# for reddit or stackoverflow
def remove_markdown(text):
    """
    Remove markdown formatting and symbols from text.

    Args:
        text: A string containing text to remove markdown from.

    Returns:
        A string containing text with markdown and symbols removed.
    """
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
    """
    Remove Twitter-specific symbols from text.

    Args:
        text: A string containing text to remove Twitter-specific symbols from.

    Returns:
        A string containing text with Twitter-specific symbols removed.
    """
    # replace usernames with [user]
    text = re.sub(r'@\S+', '@user', text) # replace usernames with @user, @ and user exist in the vocab of sentence transformer
    text = re.sub(AT_HASH_PATTERN,'',text) # remove @ and # symbols
    text = re.sub(RETWEET_PATTERN,'rt',text) # replace the word 'retweet' with 'rt', rt exist in the vocab of sentence transformer but not retweet

    # since it has previously removed the emoji, we don't need to remove it again, but to play safe, we can encode it to utf-8
    text = text.encode('utf-8', errors='ignore') # usually there's error involve with emoji, so we need to encode it to utf-8

    return text

def preprocess(text, is_twitter=True):
    """
    Preprocess social media text using remove_markdown and remove_twitter. Also returns the emojis in the text.

    Args:
        text (str): The social media text to preprocess.

    Returns:
        tuple: A tuple containing two items:
            - str: A string containing all extracted emoji characters separated by spaces.
            - str: The preprocessed text.
    """
    # extract emoji first
    emojis = extract_emoji(text)
    # remove markdown
    text = remove_markdown(text)
    # remove twitter specific symbols
	
    if is_twitter:
    	text = remove_twitter(text)
    
    # print emojis first and then text in the same line
    return emojis, text
    
if __name__ == '__main__':
    text = 'RT @user: This is a test tweet with a link https://t.co/123456 and an emoji 😂'
    emojis, preprocessed_text = preprocess(text)
    print(emojis, preprocessed_text)
