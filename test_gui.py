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
   #print(que);
   stemmed_que = stem(que).split(" ");
   question = last_question.split(" ");

   score = 0;
   for x in question:
      for y in stemmed_que:
         if x==y:
            score = score+1;
            print((x,y))

   for x in question:
      synonyms = []
      for ss in wn.synsets(x):
         for sy in ss.lemma_names():
            synonyms.append(sy)  

      synonyms = list(set(synonyms))
      for y in stemmed_que:
         for syn in synonyms:       
            if syn==y and x!=y:
               score = score+1;
               print((x,y))

   return (score*len(question))/len(stemmed_que);


def onClick(i):
   global last_question;

   if i==0:
      newQuery()
      text = entry.get()
      last_question = stem(text);
      print(last_question)
      x_test = vectorizer.transform([last_question]);
      prob = clf.decision_function(x_test);
      prob = sigmoid(prob[0]);

      OPTIONS = list(clf.classes_);      

      fOPTIONS = list();    
      fprob = []; 
      sum = 0.001;

      for x in xrange(0,len(OPTIONS)):
         temp = list(my_dict[OPTIONS[x]]); 
         fOPTIONS.extend(temp);   
         
         for y in xrange(0,len(temp)):
            score = (getScore(temp[y])+0.001)*(prob[x]+0.001);
            fprob.append(score)
            sum = sum + score;

      for x in xrange(0,len(fOPTIONS)):
         fprob[x] = fprob[x]*100/sum;
         fOPTIONS[x] = fOPTIONS[x] + "     " + str(fprob[x]);

      fOPTIONS = [x for (y,x) in sorted(zip(fprob,fOPTIONS), reverse=True)]  
      freset_option_menu(fOPTIONS[:5], 0)         

      for x in xrange(0,len(prob)):
         OPTIONS[x] = OPTIONS[x] + "     " + str(prob[x]);

      OPTIONS = [x for (y,x) in sorted(zip(prob,OPTIONS), reverse=True)]
      reset_option_menu(OPTIONS, 0)


   elif i==1:
      #clf.partial_fit(vectorizer.transform([last_question]),[variable.get().split("     ")[0]]);
      fque = fvariable.get().split("     ")[0];
      clf.partial_fit(vectorizer.transform([last_question]), [lazy_search(fque)])


def lazy_search(ques):
	for key in my_dict:
		for x in my_dict[key]:
			if x==ques:
				return key;

	return "key not found"


def quit():
   joblib.dump(clf, 'clf.pkl')
   joblib.dump(vectorizer, 'vectorizer.pkl') 
   root.destroy()
   print("bot closed") 


def print_ans(ans):
   margin = 100;
   res_ans.configure(text = ans[:margin]);
   res_ans1.configure(text = ans[margin:margin+100]);
   res_ans2.configure(text = ans[margin+100:margin+200]);
   res_ans3.configure(text = ans[margin+200:margin+300]);
   res_ans4.configure(text = ans[margin+300:margin+400]);
   res.configure(text = qvariable.get().split("     ")[0]);

def sigmoid(lst):
   sum = 0;
   for x in xrange(0,len(lst)):
      lst[x] = 1 / (1 + math.exp(-lst[x]))
      sum += lst[x];

   for x in xrange(0,len(lst)):
      lst[x] = (lst[x]/sum)*100;

   return lst;


def newQuery():
   res.configure(text = "")
   res_ans.configure(text = "")
   res_ans1.configure(text = "")
   res_ans2.configure(text = "")
   res_ans3.configure(text = "")
   res_ans4.configure(text = "")

# on change dropdown value
def change_dropdown(*args):
   qOPTIONS = list(my_dict[((variable.get()).split("    "))[0]]);   
   prob = []; 
   sum = 0.001;
   for x in xrange(0,len(qOPTIONS)):
      score = getScore(qOPTIONS[x]);
      prob.append(score)
      sum = sum + score;

   for x in xrange(0,len(qOPTIONS)):
      prob[x] = prob[x]*100/sum;
      qOPTIONS[x] = qOPTIONS[x] + "     " + str(prob[x]);

   qOPTIONS = [x for (y,x) in sorted(zip(prob,qOPTIONS), reverse=True)]  
   qreset_option_menu(qOPTIONS, 0)


# on change dropdown value
def qchange_dropdown(*args):
   if qvariable.get().split("     ")[0]=="que":
      print_ans("");
      return;
   print_ans(sol_dict[qvariable.get().split("     ")[0]]);

def fchange_dropdown(*args):
   if fvariable.get().split("     ")[0]=="que":
      print_ans("");
      return;
   print_ans(sol_dict[fvariable.get().split("     ")[0]]);


def reset_option_menu(options, index=None):
   menu = w["menu"]
   menu.delete(0, "end")
   for string in options:
      menu.add_command(label=string, 
                       command=lambda value=string:
                            variable.set(value))
   if index is not None:
      variable.set(options[index])

def qreset_option_menu(options, index=None):
   menu = qw["menu"]
   menu.delete(0, "end")
   for string in options:
      menu.add_command(label=string, 
                       command=lambda value=string:
                            qvariable.set(value))
   if index is not None:
      qvariable.set(options[index])

def freset_option_menu(options, index=None):
   menu = fw["menu"]
   menu.delete(0, "end")
   for string in options:
      menu.add_command(label=string, 
                       command=lambda value=string:
                            fvariable.set(value))
   if index is not None:
      fvariable.set(options[index])

if __name__ == '__main__':

   punc = string.punctuation.translate(None, "'");
   replace_punctuation = string.maketrans(punc, ' '*len(punc));
   operators = set(["why","what","how","when","where","who","which","whose","whom","whether","whatsoever","whither","whence"])
   stop = set(stopwords.words('english'))-operators;

   clf = joblib.load('clf.pkl') 
   vectorizer = joblib.load('vectorizer.pkl')
   my_dict = joblib.load('my_dict.pkl')
   sol_dict = joblib.load('sol_dict.pkl')

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

   OPTIONS = clf.classes_;

   variable = StringVar(root)
   variable.set(OPTIONS[0]) # default value

   w = apply(OptionMenu, (root, variable) + tuple(OPTIONS))

   variable.trace('w', change_dropdown)
   w.pack()

   qOPTIONS = ["que"];
   qvariable = StringVar(root)
   qvariable.set(qOPTIONS[0]) # default value

   qw = apply(OptionMenu, (root, qvariable) + tuple(qOPTIONS))

   qvariable.trace('w', qchange_dropdown)
   qw.pack()

   feed = Button(root, text='Positive Feedback', height=2, width=25, command=lambda i=1: onClick(1), bg="gold")
   feed.pack()

   fOPTIONS = ["que"];
   fvariable = StringVar(root)
   fvariable.set(fOPTIONS[0]) # default value

   fw = apply(OptionMenu, (root, fvariable) + tuple(fOPTIONS))

   fvariable.trace('w', fchange_dropdown)
   fw.pack()

   root.protocol('WM_DELETE_WINDOW', quit)
   root.mainloop()




