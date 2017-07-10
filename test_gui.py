from __future__ import division
from Tkinter import *;
from sklearn.externals import joblib
from sklearn.feature_extraction.text import HashingVectorizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import string;
import math


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

   return (score*len(question)/len(stemmed_que));


def getHigh(lst):
   first_best = float("-inf");
   second_best = float("-inf");
   third_best = float("-inf");
   first_index = 0;
   second_index = 0;
   third_index = 0;

   for x in xrange(0,len(lst)):
      score = lst[x];
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
      newQuery()
      text = entry.get()
      last_question = stem(text);
      #print(last_question)
      x_test = vectorizer.transform([last_question]);
      prob = clf.decision_function(x_test);
      prob = sigmoid(prob[0]);

      category_rank = getHigh(prob);

      if prob[category_rank[0]]<(100/len(clf.classes_))+1:
         print(prob[category_rank[0]])
         print((100/len(clf.classes_)))
         b11["text"] = clf.classes_[category_rank[0]] + "     " + str(prob[category_rank[0]]);
         b12["text"] = clf.classes_[category_rank[1]] + "     " + str(prob[category_rank[1]]);
         b13["text"] = clf.classes_[category_rank[2]] + "     " + str(prob[category_rank[2]]);

      b11["text"] = clf.classes_[category_rank[0]] + "     " + str(prob[category_rank[0]]);
      b12["text"] = clf.classes_[category_rank[1]] + "     " + str(prob[category_rank[1]]);
      b13["text"] = clf.classes_[category_rank[2]] + "     " + str(prob[category_rank[2]]);


      #clf.partial_fit(vectorizer.transform([last_question]),[last_answer]);
   elif i==1:
      print_ans(b1["text"]);
   elif i==2:
      print_ans(b2["text"]);
   elif i==3:
      print_ans(b3["text"]);
   elif i==11:
      rank = getBest((b11["text"].split("    "))[0]);

      b1["text"] = my_dict[(b11["text"].split("    "))[0]][rank[0]];
      b2["text"] = my_dict[(b11["text"].split("    "))[0]][rank[1]];
      b3["text"] = my_dict[(b11["text"].split("    "))[0]][rank[2]];

      res2.configure(text = b11["text"])

      #clf.partial_fit(vectorizer.transform([last_question]),[b11["text"]]);

   elif i==12:
      rank = getBest((b12["text"].split("    "))[0]);

      b1["text"] = my_dict[(b12["text"].split("    "))[0]][rank[0]];
      b2["text"] = my_dict[(b12["text"].split("    "))[0]][rank[1]];
      b3["text"] = my_dict[(b12["text"].split("    "))[0]][rank[2]];

      res2.configure(text = b12["text"])

      #clf.partial_fit(vectorizer.transform([last_question]),[b12["text"]]);
   elif i==13:
      rank = getBest((b13["text"].split("    "))[0]);

      b1["text"] = my_dict[(b13["text"].split("    "))[0]][rank[0]];
      b2["text"] = my_dict[(b13["text"].split("    "))[0]][rank[1]];
      b3["text"] = my_dict[(b13["text"].split("    "))[0]][rank[2]];   

      res2.configure(text = b13["text"])

      #clf.partial_fit(vectorizer.transform([last_question]),[b13["text"]]);
   return


def quit():
   joblib.dump(clf, 'clf.pkl')
   joblib.dump(vectorizer, 'vectorizer.pkl') 
   root.destroy()
   print("bot closed") 


def print_ans(ans):
   res_ans.configure(text = ans[:60]);
   res_ans1.configure(text = ans[60:120]);
   res_ans2.configure(text = ans[120:180]);
   res_ans3.configure(text = ans[180:240]);
   res_ans4.configure(text = ans[240:300]);

def sigmoid(lst):
   sum = 0;
   for x in xrange(0,len(lst)):
      lst[x] = 1 / (1 + math.exp(-lst[x]))
      sum += lst[x];

   for x in xrange(0,len(lst)):
      lst[x] = (lst[x]/sum)*100;

   return lst;


def newQuery():
   res2.configure(text = "")
   res_ans.configure(text = "")
   res_ans1.configure(text = "")
   res_ans2.configure(text = "")
   res_ans3.configure(text = "")
   res_ans4.configure(text = "")
   b1["text"] = "Suggestion 1";
   b2["text"] = "Suggestion 2";
   b3["text"] = "Suggestion 3";

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
   entry = Entry(root, width=200)
   entry.pack()
   gap = Label(root, bg="lightblue")
   gap.pack()
   #categories
   b10 = Button(root, text='Get Answer', height=2, width=25, command=lambda i=0: onClick(0), bg="gold")
   b10.pack()
   gap1 = Label(root, bg="lightblue")
   gap1.pack()
   b11 = Button(root,text='Category 1', height=2, width=200,command=lambda i=11: onClick(11), bg="lightgreen")
   b11.pack()
   b12 = Button(root,text='Category 2', height=2, width=200, command=lambda i=12: onClick(12), bg="lightgreen")
   b12.pack()
   b13 = Button(root,text='Category 3', height=2, width=200, command=lambda i=13: onClick(13), bg="lightgreen")
   b13.pack()
   res1 = Label(root, bg="lightblue")
   res1.pack()
   res2 = Label(root, bg="lightblue")
   res2.pack()
   res3 = Label(root, bg="lightblue")
   res3.pack()
   #insidecategories
   b1 = Button(root,text='Suggestion 1', height=2, width=200,command=lambda i=1: onClick(1), bg="lightsalmon")
   b1.pack()
   b2 = Button(root,text='Suggestion 2', height=2, width=200, command=lambda i=2: onClick(2), bg="lightsalmon")
   b2.pack()
   b3 = Button(root,text='Suggestion 3', height=2, width=200, command=lambda i=3: onClick(3), bg="lightsalmon")
   b3.pack()
   res = Label(root, bg="lightblue")
   res.pack()
   res_ans = Label(root, bg="lightblue")
   res_ans.pack()
   res_ans1 = Label(root, bg="lightblue")
   res_ans1.pack()
   res_ans2 = Label(root, bg="lightblue")
   res_ans2.pack()
   res_ans3 = Label(root, bg="lightblue")
   res_ans3.pack()
   res_ans4 = Label(root, bg="lightblue")
   res_ans4.pack()
   res_ans5 = Label(root, bg="lightblue")
   res_ans5.pack()
   root.protocol('WM_DELETE_WINDOW', quit)
   root.mainloop()