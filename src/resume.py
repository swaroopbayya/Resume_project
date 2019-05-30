import slate3k as slate
import re
from nltk.corpus import stopwords
import logging
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class JobDescription:

    def __init__(self, path):
        self.path = path
        self.summary = None
        self.education_details = None
        self.corpus = list()
        self.parse()

    def parse(self):

        logging.propagate = False

        logging.getLogger().setLevel(logging.ERROR)

        with open(self.path, 'rb') as file:
            text = slate.PDF(file)

        self.summary = TextPreprocessor().text_cleaning(text, 'Summary(.*?)Education')

        self.corpus.append(self.summary)


class TextPreprocessor:

    def text_cleaning(self, raw_text, regex):

        """
        Takes string as input. This method cleans the text by removing words called as stopwords
        and it returns a string.
       :param raw_text:
       :param regex:
       :return:
       """
        clean_text = None

        raw_text = ' '.join(raw_text)

        raw_text = '\n'.join([line for line in raw_text.splitlines() if line])

        raw_text = re.sub('[^a-zA-Z]', " ", raw_text).split()

        raw_text = ' '.join([word for word in raw_text if word not in set(stopwords.words('english'))])

        if regex == 'Summary(.*?)Education':

            special_words = ['machine', 'learning', 'artificial', 'intelligence', 'deep', 'learning', 'natural',
                             'language', 'processing']

            abbrev = {'ml': 'machinelearning', 'ai': 'artificialintelligence', 'nlp': 'naturallanguageprocessing',
                      'dl': 'deeplearning'}

            summary = re.findall(regex, raw_text)

            len_of_text = len(summary)

            for i in range(len_of_text):
                if summary[i].lower() in abbrev:
                    summary[i] = abbrev[summary[i]]

            lis_length = len(special_words)

            for i in range(lis_length - 1):
                if special_words[i] + special_words[i + 1] in summary:
                    summary.remove(special_words[i] + special_words[i + 1])
                    summary.append(special_words[i])
                    summary.append(special_words[i + 1])

            clean_text = ' '.join(summary).lower()

        elif regex == 'Education(.*?)gmail':
            pass

        return clean_text


class Resume:

    def __init__(self, path):
        self.path = path
        self.summary = None
        self.corpus = list()
        self.education_details = None
        self.value = None
        self.parse()

    def compare_with(self, obj):

        self.corpus.append(' '.join(obj.corpus))

        return self.score(self.corpus)

    def id(self):

        path = self.path

        number = path.replace('.pdf', '')

        vector = list()

        vector.append([number, self.score])

    def parse(self):

        logging.propagate = False

        logging.getLogger().setLevel(logging.ERROR)

        with open(self.path, 'rb') as file:
            text = slate.PDF(file)

        self.summary = TextPreprocessor().text_cleaning(text, 'Summary(.*?)Education')

        self.corpus.append(self.summary)


#        self.education_details = TextPreprocessor().text_cleaning(text, 'Education(.*?)gmail')

    def score(self, corpus):

        cv = CountVectorizer()

        bag_of_words = cv.fit_transform(corpus).toarray()

        value = cosine_similarity(bag_of_words)

        return value[0][1]


resume = Resume('/Users/swaroop/Desktop/swaroop/resume_sample/LI_Profile_Export_Applicants_20190521 (4).pdf')
jobDescription = JobDescription('/Users/swaroop/Desktop/swaroop/resume_sample/LI_Profile_Export_Applicants_20190521 (1).pdf')
print(resume.compare_with(jobDescription))
# print(resume.corpus)
# print(jobDescription.corpus)

