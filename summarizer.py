from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def generate_summary(text):

    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    summarizer = LsaSummarizer()

    summary = summarizer(parser.document, 5)

    final_summary = ""

    for sentence in summary:
        final_summary += str(sentence) + " "

    return final_summary