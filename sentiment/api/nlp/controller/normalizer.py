import jpype as jp

TurkishMorphology = jp.JClass('zemberek.morphology.TurkishMorphology')
TurkishSentenceNormalizer = jp.JClass('zemberek.normalization.TurkishSentenceNormalizer')
Paths = jp.JClass('java.nio.file.Paths')
lookupRoot = Paths.get('lib/normalization')
lmPath = Paths.get('lib/lm/lm.2gram.slm')
morphology = TurkishMorphology.createWithDefaults()
normalizer = TurkishSentenceNormalizer(morphology, lookupRoot, lmPath)

LanguageIdentifier = jp.JClass('zemberek.langid.LanguageIdentifier')
#lid = LanguageIdentifier.fromInternalModels()
lid = LanguageIdentifier.fromInternalModelGroup("tr_group");


def normalizer_main(input_text):
    output_text = normalizer.normalize(input_text)
    return output_text


def get_lang(input_text):
    lang = lid.identify(input_text)
    return lang


def check_lang(input_text):
    valid = lid.containsLanguage(input_text,"tr",100)
    return valid


def lemma_main(input_text):
    sentence = ""
    for myword in input_text.split():
        results = morphology.analyze(myword).analysisResults
        if len(results) == 0:
            sentence += myword
            sentence += " "
            continue
        result=results[0]
        root = result.getLemmas()
        if len(root) == 0:
            continue
        sentence += root[0]
        sentence += " "
    return sentence
