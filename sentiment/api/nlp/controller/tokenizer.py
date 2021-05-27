import jpype as jp
import nltk

nltk.download('stopwords')
stop_word_list = nltk.corpus.stopwords.words('turkish')

file1 = open("lib/custom_stop_words.txt")
line = file1.read()
words = line.split()

for w in words:
    if w not in stop_word_list:
        stop_word_list.append(w)

TurkishTokenizer = jp.JClass('zemberek.tokenization.TurkishTokenizer')
TurkishLexer = jp.JClass('zemberek.tokenization.antlr.TurkishLexer')

tokenizer = TurkishTokenizer.builder().ignoreTypes(  # TurkishLexer.Abbreviation,
    TurkishLexer.SpaceTab,
    TurkishLexer.NewLine,
    TurkishLexer.Time,
    TurkishLexer.Date,
    TurkishLexer.PercentNumeral,
    # TurkishLexer.Number,
    TurkishLexer.URL,
    TurkishLexer.Email,
    # TurkishLexer.HashTag,
    # TurkishLexer.Mention,
    # TurkishLexer.MetaTag,
    # TurkishLexer.Emoticon,
    TurkishLexer.RomanNumeral,
    # TurkishLexer.AbbreviationWithDots,
    # TurkishLexer.Word,
    TurkishLexer.WordAlphanumerical,
    TurkishLexer.WordWithSymbol,
    TurkishLexer.Punctuation,
    TurkishLexer.UnknownWord,
    TurkishLexer.Unknown
).build()


def tokenizer_main(input_text):
    input_text = input_text.replace('~', ' ')
    input_text = input_text.replace('|', ' ')
    output_text = tokenizer.tokenizeToStrings(input_text)
    return ' '.join(map(str,output_text))


def stop_words(input_text):
    input_list = str(input_text).split()
    filtered_tokens = [token for token in input_list if token not in stop_word_list]
    return ' '.join(map(str,filtered_tokens))


