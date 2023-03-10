# Preprocessing Social Media Text
This Python script provides functions to preprocess social media text, specifically Reddit and StackOverflow posts, as well as Twitter text.

## Installation
This script requires Python 3 and the re module. There are no additional dependencies.

## Usage
To use this script, first import it in your Python code:

```python
from preprocessing import preprocess
```

Then, call the `preprocess()` function with the text you want to preprocess as the argument. By default, the function assumes the text is Twitter text, but you can set the is_twitter argument to False if you are preprocessing Reddit or StackOverflow posts:

```python
text = 'RT @user: This is a test tweet with a link https://t.co/123456 and an emoji 😂'
emojis, preprocessed_text = preprocess(text)
```

The function returns a tuple containing two items:

1. A string containing all extracted emoji characters separated by spaces.
2. The preprocessed text.

## Functionality
### `extract_emoji()`
Extracts all emoji characters from the text.

```python
emojis = extract_emoji(text)
```

### `remove_markdown()`
Removes markdown formatting and symbols from the text.

```python
preprocessed_text = remove_markdown(text)
```

### `remove_twitter()`
Removes Twitter-specific symbols from the text.

```python
preprocessed_text = remove_twitter(text)
```

### `preprocess()`
Preprocesses social media text by first extracting all emoji characters, then removing markdown formatting and symbols, and finally removing Twitter-specific symbols (if is_twitter is set to True).

```python
emojis, preprocessed_text = preprocess(text, is_twitter=True)
```

```bib
@misc{preprocess,
  title = {Preprocessing Social Media Text},
  author = {Heng Ee Tay},
  year = {2023},
  howpublished = {GitHub repository},
  url = {https://github.com/hengee/preprocessing_for_social_media}
}
```
