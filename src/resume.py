import slate3k as slate
import re
from nltk.corpus import stopwords
import logging
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
from operator import itemgetter


class JobDescription:

    def __init__(self, path):

        self.path = path

        self.summary = None

        self.corpus = list()

        self.parse()

    def parse(self):

        with open(self.path, 'r') as file:
            text = file.read()

        self.summary = TextPreprocessor().text_cleaning(text, 'Summary(.*?)Education')

#       self.details = TextPreprocessor().text_cleaning(text, 'Experience(.*?)Education')

        self.corpus.append(self.summary)


class Resume:

    def __init__(self, path):

        self.path = path

        self.summary = None

        self.corpus = list()

        self.education_details = None

        self.experience = None

        self.value = None

        self.parse()

    def compare_with(self, obj):
        """
        it takes the jobDescription object as input and returns the score as output.
        :param obj:
        :return:
        """

        self.corpus.append(' '.join(obj.corpus))

        self.value = self.score(self.corpus)

        return self.value

    def id(self):
        """
        appends id to the score of every individual's resume.
        :return:
        """

        path = str(self.path).replace('.pdf', '')

        return [path, self.value]

    def parse(self):
        """
        This method is used to parse through the PDF file. It also calls the text_cleaning method and then appends the
        cleaned_text to corpus.
        :return:
        """
        logging.propagate = False

        logging.getLogger().setLevel(logging.ERROR)

        with open(self.path, 'rb') as file:
            text = slate.PDF(file)

        text = ' '.join(text)

        text = '\n'.join([line for line in text.splitlines() if line])

        self.experience = text

        self.summary = TextPreprocessor().text_cleaning(text, 'Summary(.*?)Education')

        self.corpus.append(self.summary)

#        self.education_details = TextPreprocessor().text_cleaning(text, 'Education(.*?)gmail')

    def score(self, corpus):

        """
        Takes list of texts as input and returns float value. The float value represents the similarity of the texts
        present in the corpus by creating bag_of_words.
        :param corpus:
        :return:
        """

        cv = CountVectorizer(max_features=150)

        bag_of_words = cv.fit_transform(corpus).toarray()

        value = cosine_similarity(bag_of_words)

        years = re.findall('([0-9]{1,2}) years?', self.experience)

        months = re.findall('([0-9]{1,2}) months?', self.experience)

        self.experience = sum(list(map(int, years))) + (sum(list(map(int, months))) / 12)

        value[0][1] = value[0][1] + self.experience / 100

        return value[0][1]


class SortId:

    def sort(self, id_list=list(), min_score=0.0, max_rank=0):

        length_list = len(id_list)

        id_list.sort(key=itemgetter(1), reverse=True)

        if max_rank != 0:

            if max_rank > 0:

                return [id_list[l] for l in range(0, max_rank)]
            else:

                max_rank = abs(max_rank)

                return [id_list[length_list - l] for l in range(1, max_rank+1)]

        else:

           id_list = [l for l in id_list if l[1] >= min_score]

        return id_list


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

        self.experience = raw_text

        raw_text = re.sub('[^a-zA-Z]', " ", raw_text).split()

        raw_text = ' '.join([word for word in raw_text if word not in set(stopwords.words('english'))])


        special_words = ['machine', 'learning', 'artificial', 'intelligence', 'deep', 'learning']

        abbrev = {'ml': 'machinelearning', 'ai': 'artificialintelligence', 'dl': 'deeplearning'}

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

        #print(raw_text)

        return clean_text


jobDescription = JobDescription('/Users/swaroop/Desktop/swaroop/jds/se1.txt')

pathlist = Path('/Users/swaroop/Desktop/swaroop/resumes').glob('*.pdf')

id_list = list()

for path in pathlist:
    resume = Resume(path)
    print(resume.compare_with(jobDescription))
    id_list.append(resume.id())

# print(resume.path)

# print(resume.experience)

# print(resume.value)

sort_id = SortId()

print(sort_id.sort(id_list))

# 62-LI_Profile_Export_Applicants_20190521 (3).pdf best case
# 66-LI_Profile_Export_Applicants_20190521 (2).pdf worst case
