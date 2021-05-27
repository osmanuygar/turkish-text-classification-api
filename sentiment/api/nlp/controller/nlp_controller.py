from sentiment.api.nlp.controller.jvm import init_jvm
from sentiment.api.nlp.controller.normalizer import normalizer_main, get_lang,check_lang, lemma_main
from sentiment.api.nlp.controller.tokenizer import tokenizer_main,stop_words

def understandable_text(input_data):
    init_jvm()
    result = {}
    if not input_data.strip():
        result['result'] = 'NoContent'
        return result
    normalized = normalizer_main(input_data)
    if check_lang(normalized)!=True and len(normalized.split()) > 8:
        result['result'] = 'NoTurkishContent'
        return result
    result['result'] = normalized
    return result


def clean_text(input_data):
    init_jvm()
    result = {}
    if not input_data.strip():
        result['result'] = 'NoContent'
        return result
    tokenized = tokenizer_main(input_data)
    # return if context null
    if not tokenized.strip():
        result['result'] = 'NoContent'
        return result
    tokenized_normalized = normalizer_main(tokenized)
    stop_tokenized_normalized = stop_words(tokenized_normalized)
    # return if context is not turkish
    if check_lang(stop_tokenized_normalized) != True and len(stop_tokenized_normalized.split()) > 5:
        result['result'] = 'NoTurkishContent'
        return result
    result['result'] = stop_tokenized_normalized
    return result


def lemma_text(input_data):
    init_jvm()
    result = {}
    if not input_data.strip():
        result['result'] = 'NoContent'
        return result
    tokenized = tokenizer_main(input_data)
    # return if context null
    if not tokenized.strip():
        result['result'] = 'NoContent'
        return result
    tokenized_normalized = normalizer_main(tokenized)
    # return if context is not turkish
    if check_lang(tokenized_normalized) != True and len(tokenized_normalized.split()) > 5:
        result['result'] = 'NoTurkishContent'
        return result
    lemma_sentence = lemma_main(tokenized_normalized)
    result['result'] = lemma_sentence
    return result
