# -*- coding: utf-8 -*-
"""
Created on Tuesday Jul 30 09:38:24 2019
Hello and welcome to my project.
Under the supervision of Christophe Cop, I aim to create a script that will do the following:

1. Read a cv file (in the formats: .txt)
2. Identify and extract particular information (Name, Role, Area, Background, Key Project, Industry, Education, Skills, languages, Experience, Email, and Phone)
3. Store extracted information in dictionaries and then export in JSON format to be reused with other templates

Enjoy!

@author: samareaa
"""

import nltk, json, glob, re, sys



class exportToJSON:

    def __init__(self, infoDict):
        with open('result.json', 'w') as fp:
            json.dump(infoDict, fp)

    def write(self, infoDict):
        fOut = open('infoExtracted.txt', 'a+')
        writeString = ''
        try:
            writeString += str(infoDict['fileName']) + ','
            writeString += str(infoDict['name']) + ','
            writeString += str(infoDict['role']) + ','
            writeString += str(infoDict['area']) + ','
            writeString += str(infoDict['background']) + ','
            writeString += str(infoDict['keyProjects']) + ','
            writeString += str(infoDict['industry']) + ','
            writeString += str(infoDict['education']) + ','
            writeString += str(infoDict['skills']) + ','
            writeString += str(infoDict['languages']) + ','
            writeString += str(infoDict['experience']) + ','
            writeString += str(infoDict['email']) + ','
            writeString += str(infoDict['phone']) + '\n'
            fOut.write(writeString)
        except:
            fOut.write('FAILED_TO_WRITE\n')
            fOut.close()



class Parse():
    information = []
    inputString = ''
    tokens = []
    lines = []
    sentences = []


    def __init__(self,verbose=False):
        print('Welcome')
        fields = ["name", "role", "area", "background", "keyProjects", "industry", "education", "skills", "languages", "experience", "email", "phone"]

        #glob module matches pattern
        text_files = glob.glob("1DOC44AC.txt")

        files = set(text_files)
        files = list(files)
        print("%d files identified" %len(files))

        for f in files:
            print("Reading File %s"%f)

            info = {}
            self.inputString, info['extension'] = self.readFile(f)
            info['fileName'] = f

            self.tokenize(self.inputString)
            self.matchName(self.inputString, info)
            self.matchRole(self.inputString, info)
            self.matchArea(self.inputString, info)
            self.matchBackground(self.inputString, info)
            self.matchKeyProjects(self.inputString, info)
            self.matchIndustry(self.inputString, info)
            self.matchEducation(self.inputString, info)
            self.matchSkills(self.inputString, info)
            self.matchLanguages(self.inputString, info)
            self.matchExperience(self.inputString, info)
            self.matchEmail(self.inputString, info)
            self.matchPhone(self.inputString, info)

            json = exportToJSON()
            json.write(info)
            self.information.append(info)
            print(info)

    def readFile(self, fileName):
        extension = fileName.split(".")[-1]
        if extension == 'txt':
            f = open(fileName, 'r')
            string = f.read()
            f.close()
            return string, extension
        else:
            print ('Unsupported format')
            return '', ''
        #insert elif here if I want to make more type of documents readable i.e: doc? docx?


    def ie_preprocess(self, document):
        # connect natural language toolkit default sentence segmeter
        lines = [lines.strip() for lines in document.split("\n") if len(lines) > 0]
        sentences = nltk.sent_tokenize(document)

        # connect nltk word tokenizer
        lines = [nltk.word_tokenize(line) for line in lines]
        sentences = [nltk.word_tokenize(sent) for sent in sentences]  # tokenized in lists of lists of strings
        tokens = sentences

        # connect nltk part-of-speech tagger
        lines = [nltk.pos_tag(lines) for lines in lines]
        sentences = [nltk.pos_tag(sent) for sent in sentences]  # tagged in lists of tuples being (<word>, <tag>)

        # converts tokens from list of list, to list (patching together)
        dummy = []
        for lines in tokens:
            dummy += lines
        tokens = dummy

        return tokens, lines, sentences


    def tokenize(self, inputString):
        try:
            self.tokens, self.lines, self.sentences = self.ie_preprocess(inputString)
            return self.tokens, self.lines, self.sentences
        except Exception as e:
            print(e)


    '''
    Following code will take a string as input and return matches
    for NAMES. 
    
    The code uses regex matches and requires:
    1. Input String
    2. Dictionary
    '''


    def matchName(self, inputString, infoDict):
        names = None

        try:
        # open and read both files for comparison
            words1 = set(open("names.txt").read().split())
            words2 = set(open("DOC44AC.txt").read().split())

        # find intersection between both txts (i.e detect name)
            names = words1.intersection(words2)
            print(names)

        except:
            pass

        infoDict['name'] = names


    '''
    Following code will take a string as input and return matches
    for ROLE. 
    
    The code uses regex matches and requires:
    1. Input String
    2. Dictionary
    '''


    def matchRole(self, inputString, infoDict):
        roles = None

        try:
            words1 = set(open("roles.txt").read().split())
            words2 = set(open(inputString).read().split())

            # find intersection between both txts (i.e detect name)
            roles = words1.intersection(words2)
        except:
            pass

        infoDict['role'] = roles


    '''
    Following code will take a string as input and return matches
    for AREA. 
    
    The code uses regex matches and requires:
    1. Input String
    2. Dictionary
    '''


    def matchArea(self, inputString, infoDict):
        areas = None

        try:
            words1 = set(open("locations.txt").read().split())
            words2 = set(open(inputString).read().split())

            areas = words1.intersection(words2)
        except:
            pass

        infoDict['area'] = areas


    '''
    Following code will take a string as input and return matches
    for BACKGROUND. 
    
    The code uses regex matches and requires:
    1. Input String
    2. Dictionary
    '''


    def matchBackground(self, inputString, infoDict):
        background = None
        copy = False
        for line in inputString:
            if line.strip() == "Profile/Background":
                copy = True
                continue
            elif line.strip() == "Key project experience":
                copy = False
                continue
            elif line.strip() == "Industry expertise":
                copy = False
                continue
            elif copy:
                infoDict['background'] = background


    '''
    Following code will take a string as input and return matches
    for KEY PROJECT EXPERIENCE. 
    
    The code uses regex matches and requires:
    1. Input String
    2. Dictionary
    '''


    # fix this
    def matchKeyProjects(self, inputString, infoDict):
        keyProject = None
        copy = False
        for line in inputString:
            if line.strip() == "Key project experience":
                copy = True
                continue
            elif line.strip() == "Industry expertise":
                copy = False
                continue
            elif copy:
                infoDict['keyProjects'] = keyProject


    '''
    Following code will take a string as input and return matches
    for INDUSTRY EXPERTISE. 
    
    The code uses regex matches and requires:
    1. Input String
    2. Dictionary
    '''


    def matchIndustry(self, inputString, infoDict):
        industry = None
        copy = False
        for line in inputString:
            if line.strip() == "Industry expertise":
                copy = True
                continue
            elif line.strip() == "Education":
                copy = False
                continue
            elif copy:
                infoDict['industry'] = industry


    '''
    Following code will take a string as input and return matches
    for EDUCATION. 
    
    The code uses regex matches and requires:
    1. Input String
    2. Dictionary
    '''


    def matchEducation(self, inputString, infoDict):
        # edit this to match the function, but method works!
        # also, this is not separated between the various elements yet so degree is not separate of school, its just a chunk
        # work on that after
        education = None
        copy = False
        for line in inputString:
            if line.strip() == "Education":
                copy = True
                continue
            elif line.strip() == "Areas of specialization":
                copy = False
                continue
            elif copy:
                infoDict['education'] = education


    '''
    Following code will take a string as input and return matches
    for AREAS OF SPECIALIZATION. 
    
    The code uses regex matches and requires:
    1. Input String
    2. Dictionary
    '''


    def matchSkills(self, inputString, infoDict):
        skills = None
        copy = False
        for line in inputString:
            if line.strip() == "Areas of specialization":
                copy = True
                continue
            elif line.strip() == "Languages":
                copy = False
                continue
            elif copy:
                infoDict['skills'] = skills



    '''
    Following code will take a string as input and return matches
    for LANGUAGES. 
    
    The code uses regex matches and requires:
    1. Input String
    2. Dictionary
    '''


    def matchLanguages(self, inputString, infoDict):
        # open and read both files for comparison
        words1 = set(open("Languages.txt").read().split())
        words2 = set(open(inputString).read().split())

        # find intersection between both txts (i.e detect language)
        languages = words1.intersection(words2)

        # uniques are now the words that are not matching
        # uniques = words1.difference(words2).union(words2.difference(words1))

        infoDict['languages'] = languages


    '''
    Following code will take a string as input and return matches
    for PRIOR PROFESSIONAL EXPERIENCE. 
    
    The code uses regex matches and requires:
    1. Input String
    2. Dictionary
    '''


    # doesn't work... but logic is the following:
    # take text between "prior professional experience" and the name identified earlier in
    # the matchNames() function....

    def matchExperience(self, inputString, infoDict, names):
        words1 = set(open("names.txt").read().split())
        words2 = inputString
        names = words1.intersection(words2)

        with open('DOC44AC.txt', 'r') as infile, open('results.txt', 'w') as outfile:
            copy = False
            for line in infile:
                if line.strip() == "Prior professional experience":
                    copy = True
                    continue
                elif line.strip() == words1.intersection(words2):
                    copy = False
                    continue
                elif copy:
                    outfile.write(line)


    '''
    Following code will take a string as an input, and return
    matches for EMAILS
    
    Using regular expression  and requires the following:
    1.Input string
    2. Dictionary where values are going to be stored
    '''


    def matchEmail(self, inputString, infoDict):
        email = None
        try:
            for line in inputString:
                for word in re.findall(r'\w+', line):
                    email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", line)
        except Exception as e:
            print(e)

        infoDict['email'] = email


    '''
    Following code will take a string as input, and return matches
    for PHONE numbers.
    
    Using regex and requires the following:
    1. Input string
    2. Dictionary
    '''


    def matchPhone(self, inputString, infoDict):
        phone = None
        try:
            pattern = re.compile(r'(/^((\+|00)32\s?|0)4(60|[789]\d)(\s?\d{2}){3}$/)')
            matches = pattern.findall(inputString)
            phone = matches
        except Exception as e:
            print(e)

        infoDict['phone'] = phone


if __name__ == "__main__":
    verbose = False
    if "-v" in str(sys.argv):
        verbose = True
    p = Parse(verbose)