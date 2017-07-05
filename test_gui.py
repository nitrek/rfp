from Tkinter import *;
from sklearn.externals import joblib
from sklearn.feature_extraction.text import HashingVectorizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
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


def getTop(lst):
   first_index=0;
   second_index=0;
   third_index=0;
   first_value=float("-inf");
   second_value=float("-inf");
   third_value=float("-inf");

   for x in xrange(0,len(lst)):
      if lst[x]>first_value:
         first_value=lst[x];
         first_index=x;
      elif lst[x]>second_value:
         second_value=lst[x];
         second_index=x;
      elif lst[x]>third_value:
         third_value=lst[x];
         third_index=x;

   return [(first_index,first_value), (second_index,second_value), (third_index,third_value)];
      


def onClick(i):
   global last_question, first_value, second_value, third_value;

   if i==0:
      text = entry.get()
      last_question = stem(text);
      x_test = vectorizer.transform([last_question]);
      prob = clf.decision_function(x_test);
      print(prob[0])

      last_answer = clf.predict(x_test)[0];
      print(last_answer);

      topthree = getTop(prob[0]);
      first_index,first_value = topthree[0];
      second_index,second_value = topthree[1];
      third_index,third_value = topthree[2];

      b1["text"] = clf.classes_[first_index];
      b2["text"] = clf.classes_[second_index];
      b3["text"] = clf.classes_[third_index];
   elif i==1:
      res.configure(text = b1["text"]);
      if first_value>-1:
         print("reinforced")
         clf.partial_fit(vectorizer.transform([last_question]),[b1["text"]]);
   elif i==2:
      res.configure(text = b2["text"]);
      if second_value>-1:
         print("reinforced")
         clf.partial_fit(vectorizer.transform([last_question]),[b2["text"]]);
   elif i==3:
      res.configure(text = b3["text"]);
      if third_value>-1:
         print("reinforced")
         clf.partial_fit(vectorizer.transform([last_question]),[b3["text"]]);

   return


def quit():
   #joblib.dump(clf, 'clf.pkl')
   #joblib.dump(vectorizer, 'vectorizer.pkl') 
   root.destroy()
   print("bot closed") 


if __name__ == '__main__':
   punc = string.punctuation.translate(None, "'");
   replace_punctuation = string.maketrans(punc, ' '*len(punc));
   operators = set(["why","what","how","when","where","who","which","whose","whom","whether","whatsoever","whither","whence"])
   stop = set(stopwords.words('english'))-operators;

   clf = joblib.load('clf.pkl') 
   vectorizer = joblib.load('vectorizer.pkl')

   last_answer = "";
   last_question = "";
   first_value=float("-inf");
   second_value=float("-inf");
   third_value=float("-inf");

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