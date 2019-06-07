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

        self.experience = None

        self.education_details = None

        self.corpus = list()

        self.parse()

    def parse(self):
        """
        extracts all the text of different regex and assigns the values to respective variables
        :return:
        """

        with open(self.path, 'r') as file:
            text = file.read()

        self.summary = TextPreprocessor().text_cleaning(text, 'Summary(.*)')

        self.experience = TextPreprocessor().text_cleaning(text, 'Experience(.*?)Education')

        self.education_details = TextPreprocessor().text_cleaning(text, 'Education(.*)')

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

        self.value = self.score(self.corpus, obj)

        return self.value

    def id(self):
        """
        appends id to the score of every individual's resume and returns a list of id and score.
        :return:
        """

        path = str(self.path).replace('.pdf', '')

        return [path, self.value]

    def modify(self, text):
        """
        Removes all the blank lines and returns a string.
        :param text:
        :return:
        """

        text = ' '.join(text)

        text = '\n'.join([line for line in text.splitlines() if line])

        return text

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

        text = self.modify(text)

        self.summary = TextPreprocessor().text_cleaning(text, 'Summary(.*)')

        self.corpus.append(self.summary)

        self.experience = TextPreprocessor().text_cleaning(text, 'Experience(.*?)Education')

        self.education_details = TextPreprocessor().text_cleaning(text, 'Education(.*?)gmail')

    def score(self, corpus, obj):
        """
        Takes list of texts as input and returns float value. The float value represents the similarity of the texts
        present in the corpus by creating bag_of_words.
        :param corpus:
        :param obj:
        :return:
        """

        cv = CountVectorizer(max_features=None)

        bag_of_words = cv.fit_transform(corpus).toarray()

        value = cosine_similarity(bag_of_words)

        value[0][1] = value[0][1] + self.experience / (obj.experience * 10)

        return value[0][1]


class SortId:

    def sortScores(self, id_list, score=0.0, rank=0):
        """
        sorts the list of scores in descending order. It contains default parameters score and rank which can be
        used to retrieve required resumes.
        :param id_list:
        :param score:
        :param rank:
        :return:
        """

        length_list = len(id_list)

        id_list.sort(key=itemgetter(1), reverse=True)

        if rank != 0:

            if rank > 0:

                return [id_list[l] for l in range(0, rank)]
            else:

                rank = length_list - abs(rank)

                return [id_list[l] for l in range(rank, length_list)]

        else:

           id_list = [l for l in id_list if l[1] >= score]

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

        if regex == 'Experience(.*?)Education':

            raw_text = re.sub('[^a-zA-Z0-9]', ' ', raw_text)

            raw_text = re.findall(regex, raw_text)

            raw_text = ' '.join(raw_text)

            years = re.findall('([0-9]{1,2}).? years?', raw_text)

            months = re.findall('([0-9]{1,2}) months?', raw_text)

            return sum(list(map(int, years))) + (sum(list(map(int, months))) / 12)

        elif regex == 'Education(.*?)gmail':
            pass

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

        return clean_text


if __name__ == '__main__':

    jobDescription = JobDescription('/Users/swaroop/Desktop/swaroop/jds/sse1.txt')

    pathlist = Path('/Users/swaroop/Desktop/swaroop/resumes').glob('*.pdf')

    id_list = list()

    for file in pathlist:
        resume = Resume(file)
        print(resume.compare_with(jobDescription))
        id_list.append(resume.id())

    sort_id = SortId()

    print(sort_id.sortScores(id_list))


