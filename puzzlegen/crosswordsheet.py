import os
import csv
from lib import *
import datetime;


class document(object):
    """
    Small class for managing the documents and compiling them
    """
    def __init__(self, fname, title="", savetex=True):
        self.savetex = savetex
        #self.start,self.middle, self.end = doc_generator(title)
        self.main = []
        self.fname = fname


        #with open('starwars.csv', mode='r') as csvfile:


    def add(self, code):
        """
        Adds new sections to the document
        """
        self.main.append(code)

    def write_compile(self, remove_aux=True):
        """
        Writes and compiles into a pdf
        """
        print "I think fname is >>>"+self.fname+"<<<<\n"
        f = open("tmp/%s.tex" % self.fname, "wb")
        f.write('\n'.join(self.main))
        f.close()
        os.system("pdflatex --output-directory tmp tmp/%s.tex" % self.fname)
        now=datetime.datetime.now().isoformat()
        os.system("cp tmp/{}.pdf log/{}_{}.pdf".format(self.fname,self.fname,now))

        os.remove("tmp/%s.log" % self.fname)
        if remove_aux:
            os.remove("tmp/%s.aux" % self.fname)
        if not self.savetex:
            os.remove("tmp/%s.tex" % self.fname)

class crossword1d(object):

    def __init__(self, fname, title="",clue="gimme", savetex=False):
        print " I just got {}".format(fname)
        with open('static/'+fname, mode='r') as csvfile:
            reader = csv.reader(csvfile,quotechar='"')
            self.s = {rows[0]:rows[1] for rows in reader}

        self.fname=fname.replace(" ","").lower().replace(".csv","")
        self.clue=clue.upper()

        self.crossword_puzzle=document(self.fname)
        self.title=title
        self.puzzle_lines=[]
        self.hint_lines=[]
        self.puzzle_list=list()
        self.pos={}
        self.hints=[]
        self.width_of_puzzle=0



    def add_section(self, *args, **kwargs):
        start,middle,end=docparts.crossword_parts(title=self.title)
        self.choose_words()
        self.make_puzzle_lines()
        self.make_hint_lines()
        print self.pos

        self.crossword_puzzle.add(start)
        self.crossword_puzzle.add("\\begin{Puzzle}{"+str(self.width_of_puzzle)+"}{"+str(len(self.puzzle_list))+"}")
        self.crossword_puzzle.add('\n'.join(self.puzzle_lines))
        self.crossword_puzzle.add(middle)
        self.crossword_puzzle.add('\n'.join(self.hint_lines))
        self.crossword_puzzle.add(end)


    def layout_line(self,line,clue_num,clue_column):
        #given '---CAT-----',11
        #output |{}|{}|{}|[1]C|A|T|{}|{}|{}|{}|{}|.
        output_line="|"
        numbered = False
        print "just received:"+line
        print "with length:"+str(len(line))
        print "and clue column:"+str(clue_column)
        for i in range(len(line)):
            col_str=""
            ch = line[i]
            if ch=='-':
                col_str='{}'
            else:
                if not numbered:
                    col_str="["+str(clue_num)+"]"
                    numbered = True
                else:
                    col_str+="[]"
                if i == clue_column:
                    col_str += "[O]"
                col_str += ch
            output_line = output_line +col_str +"|" 
        return output_line+"."

    def choose_words(self, *args, **kwargs):
        glossary=self.s.keys()
        cnt=0
        max_to_right=0
        max_to_left=0
        for ch in self.clue.replace(" ",""):
            while True and cnt<40:
                one_word=random.choice(glossary)
                print ",".join(self.puzzle_list)
                print "looking for {}".format(ch)
                print "and {} doesn't cut it with {}".format(one_word,one_word in self.puzzle_list)
                if ch in one_word.upper() and one_word not in self.puzzle_list:
                    self.puzzle_list.append(one_word)
                    chars_to_left=one_word.upper().index(ch)-1
                    chars_to_right=len(one_word)-chars_to_left-1
                    max_to_left=chars_to_left if chars_to_left>max_to_left else max_to_left
                    max_to_right=chars_to_right if chars_to_right>max_to_right else max_to_right
                    self.pos[one_word]=(chars_to_left,chars_to_right)
                    
                    break
                else:
                    cnt=+1
            cnt=0

        self.width_of_puzzle=max_to_left+max_to_right+1
        self.max_to_left=max_to_left
        self.max_to_right=max_to_right

    def make_puzzle_lines(self,*args, **kwargs):

        for i in range(len(self.puzzle_list)):
            word = self.puzzle_list[i]
            print "Question "+str(i+1)+":"+word.replace(" ","")
            tex_formatted_line=self.layout_line('-'*(self.max_to_left-self.pos[word][0])+word.replace(" ","")+'-'*(self.max_to_right-self.pos[word][1]),i+1,self.max_to_left+1)
            self.puzzle_lines.append(tex_formatted_line)
            self.hints.append("\\Clue{"+str(i+1)+"}{"+word.upper()+"}{"+self.s[word]+"}")   

    def make_hint_lines(self,*args,**kwargs):
        second_half_flag = False
        for i in range(len(self.hints)):
            line=self.hints[i]
            if i > len(self.puzzle_list)/2 and not second_half_flag:
                self.hint_lines.append('\\end{PuzzleClues}')
                self.hint_lines.append('\\begin{PuzzleClues}{\\textbf{ }}\\\\')
                second_half_flag = True
            self.hint_lines.append(line+"\\"+"\\"+"\\")

    def write(self):
        self.crossword_puzzle.write_compile()

if __name__ == "__main__":
        mycrossword = crossword1d("European_History.csv",clue="i love you", savetex=True)
        mycrossword.add_section()
        mycrossword.write()
