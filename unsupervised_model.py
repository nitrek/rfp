from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.externals import joblib
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import string;
import numpy as np;
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import PassiveAggressiveClassifier
from time import time


clf = joblib.load('clf.pkl') 
vectorizer = joblib.load('vectorizer.pkl')
my_dict = joblib.load('my_dict.pkl')
sol_dict = joblib.load('sol_dict.pkl')

t0 = time()

punc = string.punctuation.translate(None, ",");

replace_punctuation = string.maketrans(punc, ' '*len(punc));
operators = set(["why","what","how","when","where","who","which","whose","whom","whether","whatsoever","whither","whence"])
stop = set(stopwords.words('english'))-operators;

with open('unsupervised_questions', 'r') as qfile:
    questions = qfile.readlines();

qfile.close();

questions = [x.strip()for x in questions];

for x in xrange(0,len(questions)):
	que = questions[x].split(",");

	questions[x] = " ".join(que[:len(que)-1]);
	sol_dict[questions[x].strip()] = que[-1];

backup_questions = list(questions);

joblib.dump(sol_dict,'sol_dict.pkl')

questions = [x.lower().translate(replace_punctuation) for x in questions];

for line in xrange(0,len(questions)):
    questions[line] = ' '.join([word for word in questions[line].split() if word not in (stop)]);


for line in xrange(0,len(questions)):
    singles = []
    lmtzr = WordNetLemmatizer() 
    for plural in questions[line].split():
        singles.append(lmtzr.lemmatize(plural))
    questions[line] = ' '.join(singles)

answers = clf.predict(vectorizer.transform(questions)).tolist();

for x in xrange(0,len(questions)):

	if my_dict.has_key(answers[x]):
		my_dict[answers[x]].append(backup_questions[x]);
	else:
		my_dict[answers[x]] = [];
		my_dict[answers[x]].append(backup_questions[x]);

joblib.dump(my_dict, 'my_dict.pkl')

nltk_questions = [];
nltk_answers = [];

for sentence in xrange(0,len(questions)):

	list_x = questions[sentence].split(" ");

	list_of_list = [];
	for x_word in xrange(0,len(list_x)):
		synonyms = []
		for ss in wn.synsets(list_x[x_word]):
			for sy in ss.lemma_names():
				synonyms.append(sy)	

		synonyms = list(set(synonyms))
		list_of_list.append(synonyms);

	for i in xrange(0,len(max(list_of_list, key=len))):
	    new_que = "";
	    for lst in xrange(0,len(list_of_list)):
	    	if len(list_of_list[lst])>i:
	    		new_que += list_of_list[lst][i];
	    	else:
	    		new_que += list_x[lst];
	    	new_que += " ";	
	    nltk_questions.append(new_que);
	    nltk_answers.append(answers[sentence])		

			
nltk_questions = [x.strip().lower().replace("_", " ")for x in nltk_questions];


answers.extend(nltk_answers);
y_train = answers;

questions.extend(nltk_questions);

print(len(questions))

X_train = vectorizer.transform(questions);

clf.partial_fit(X_train, y_train);

joblib.dump(clf, 'clf.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl') 
total_time = time()-t0;
print(total_time);