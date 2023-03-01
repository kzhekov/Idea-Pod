import re
import ssl
from string import punctuation

import nltk
import spacy
from nltk import TreebankWordTokenizer
from nltk.corpus import stopwords
from pytrends.request import TrendReq


class KeywordsGenerator:
    def __init__(self):
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        nltk.download('punkt')
        nltk.download('stopwords')

    def generate_tags(self, text, top_words=30):
        clean_text = self._remove_noise(text)
        top_words = self._get_top_words(clean_text, top_words)
        suggestions = []
        for top_word in top_words:
            suggestions.extend(self.get_suggestions(top_word))
        suggestions.extend(top_words)
        tags = self._clean_tokens(suggestions)
        return ",".join(list(set(tags)))

    def _remove_noise(self, text):
        # 1. Convert Text To Lowercase and remove numbers
        lower_case_text = str.lower(text)
        just_text = re.sub(r'\d+', '', lower_case_text)
        tokenizer = TreebankWordTokenizer()
        tokens = tokenizer.tokenize(just_text)
        # 3. Clean text
        clean = self._clean_tokens(tokens)
        return clean

    @staticmethod
    def _clean_tokens(tokens):
        clean_words = [w for w in tokens if w not in punctuation]
        stopwords_to_remove = stopwords.words('english')
        clean = [w for w in clean_words if w not in stopwords_to_remove and not w.isnumeric()]
        return clean

    @staticmethod
    def _get_top_words(words, top):
        counts = dict()

        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        count_list = list({k: v for k, v in sorted(counts.items(), key=lambda item: item[1])}.keys())[:top]
        print(count_list)
        return count_list


if __name__ == "__main__":
    to_process = """
        Python is already one of the most popular programming languages, and it’s only getting more popular. In fact, experts predict that Python will soon dominate the market, with demand for developers and services increasing exponentially. This article will take a look at all the major factors that make it one of the most sought-after skills for cutting-edge development.

        Python is easy to learn, powerful, and versatile. It’s used by top companies like Google, Meta, Instagram, and Dropbox, and it has a thriving community of developers that improve both its core functionality and additional requirements with open-source libraries. It can cover pretty much any use case you can imagine, ranging from APIs and web frameworks, to data analysis and machine learning, and it can do it in the most efficient way possible.
        
        If you’re not using Python yet, now is the time to start learning. But if you’re still not convinced, read on! Trust me — your career will thank you for it.
        
        Python is an incredibly powerful and versatile language, made even more potent by its community and open source standard library. With its popular backing always growing, Python users can tackle any challenge that comes their way, with abundant documentation and helpful resources covering the different use cases that might arise.
        
        There are countless great libraries that are available for use with the execution of a single “pip install” command. From payment processing, to data analysis and business intelligence, to GUI programming, to APIs, Python’s abundant landscape of tools offers every project a chance to shine in a fraction of the cost it would need if the functionality had to be implemented from scratch.
        
        The community also goes towards maintaining Python’s core, providing fixes for older versions as well as helping to create newer versions of Python itself, ensuring that users have the latest tools available at their disposal. Whether you’re a novice programmer or a seasoned software engineer, knowing that you are not betting on a dying language, but one that is constantly evolving, is quite reassuring.
        
        In the end, all of this translates into one of the most important factors when deciding for a tech stack — productivity. An abundance of high-quality resources that cut your development time by a lot is a great way of reducing not only the initial cost of development, but also the cost of code maintenance and fixing code debt, architecture and module handover, and developer onboarding.
    """
    from keybert import KeyBERT

    tags = KeyBERT().extract_keywords(to_process, top_n=16)
    print(tags)
    result = []
    pytrends = TrendReq(hl='en-GB', tz=360)
    payloads = []
    print(len(tags))
    for i in range(0, len(tags), 4):
        print(i, [tag[0] for tag in tags[i:i+4]])
        payloads.append([tag[0] for tag in tags[i:i+4]])
    for payload in payloads:
        print(payload)
        pytrends.build_payload(payload, timeframe='today 6-m')
        data = pytrends.related_queries()[payload]['top']
        if len(data):
            result.extend([x[0] for x in data.values.tolist()][:2])
    print(result)
