from Tkinter import *;
from sklearn.externals import joblib
from sklearn.feature_extraction.text import HashingVectorizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import string;

def stem(sentence):
   sentence = sentence.lower().translate(replace_punctuation)
   sentence = ' '.join([word for word in sentence.split() if word not in (stop)]);
   singles = []
   lmtzr = WordNetLemmatizer() 
   for plural in sentence.split():
       singles.append(lmtzr.lemmatize(plural))
   sentence = ' '.join(singles)  
   return sentence;       


def getScore(que):
   stemmed_que = stem(que).split(" ");
   question = last_question.split(" ");

   score = 0;
   for x in question:
      for y in stemmed_que:
         if x==y:
            score = score+1;
            print("hello")
            print(x)

   for x in question:
      synonyms = []
      for ss in wn.synsets(x):
         for sy in ss.lemma_names():
            synonyms.append(sy)  

      synonyms = list(set(synonyms))
      for y in stemmed_que:
         for syn in synonyms:       
            if syn==y:
               score = score+1;
               print("hi")
               print(x)

   return score;




def getBest(ans):
   size = len(my_dict[ans]);

   first_best = float("-inf");
   second_best = float("-inf");
   third_best = float("-inf");
   first_index = 0;
   second_index = 0;
   third_index = 0;

   for x in xrange(0,size):
      score = getScore(my_dict[ans][x]);
      if score>first_best:
         first_index = x;
         first_best = score;
      elif score>second_best:
         second_index = x;
         second_best = score;
      elif score>third_best:
         third_index=x;
         third_best = score;

   return [first_index,second_index,third_index]


def onClick(i):
   global last_question;

   if i==0:
      text = entry.get()
      last_question = stem(text);
      x_test = vectorizer.transform([last_question]);
      #prob = clf.decision_function(x_test);
      #print(prob[0])

      last_answer = clf.predict(x_test)[0];
      print(last_answer);

      rank = getBest(last_answer);

      b1["text"] = my_dict[last_answer][rank[0]];
      b2["text"] = my_dict[last_answer][rank[1]];
      b3["text"] = my_dict[last_answer][rank[2]];

      clf.partial_fit(vectorizer.transform([last_question]),[last_answer]);
   elif i==1:
      res.configure(text = b1["text"]);
   elif i==2:
      res.configure(text = b2["text"]);
   elif i==3:
      res.configure(text = b3["text"]);
   return


def quit():
   joblib.dump(clf, 'clf.pkl')
   joblib.dump(vectorizer, 'vectorizer.pkl') 
   root.destroy()
   print("bot closed") 


if __name__ == '__main__':
   punc = string.punctuation.translate(None, "'");
   replace_punctuation = string.maketrans(punc, ' '*len(punc));
   operators = set(["why","what","how","when","where","who","which","whose","whom","whether","whatsoever","whither","whence"])
   stop = set(stopwords.words('english'))-operators;

   clf = joblib.load('clf.pkl') 
   vectorizer = joblib.load('vectorizer.pkl')
   my_dict = joblib.load('my_dict.pkl')

   last_answer = "";
   last_question = "";

   root = Tk()
   root.configure(background='lightblue')
   root.title("Mahdihusain Momin")
   Label(root, text="ASK ME", bg="lightblue").pack()
   entry = Entry(root, width=75)
   entry.pack()
   b0 = Button(root, text='Get Answer', height=2, width=25, command=lambda i=0: onClick(0), bg="gold")
   b0.pack()
   b1 = Button(root,text='Suggestion 1', height=2, width=75,command=lambda i=1: onClick(1), bg="lightgreen")
   b1.pack()
   b2 = Button(root,text='Suggestion 2', height=2, width=75, command=lambda i=2: onClick(2), bg="lightgreen")
   b2.pack()
   b3 = Button(root,text='Suggestion 3', height=2, width=75, command=lambda i=3: onClick(3), bg="lightgreen")
   b3.pack()
   res = Label(root, bg="lightblue")
   res.pack()
   root.protocol('WM_DELETE_WINDOW', quit)
   root.mainloop()