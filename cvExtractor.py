import glob, nltk, os, code, sys, re
from pprint import pprint
from pathlib import Path
import json


# from json import dumps, loads, JSONEncoder, JSONDecoder
# import pickle
#
# class PythonObjectEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
#             return JSONEncoder.default(self, obj)
#         return {'_python_object': pickle.dumps(obj)}
#
# def as_python_object(dct):
#     if '_python_object' in dct:
#         return pickle.loads(str(dct['_python_object']))
#     return dct


class exportToJSON:
    def __init__(self, fileName='results.txt', resetFile=False):
        headers = ['FILE NAME',
                   'NAME',
                   'META',
                   'LOCATION',
                   'INFO',
                   'PROJECTS',
                   'INDUSTRY',
                   'EDUCATION',
                   'SKILLS',
                   'LANGUAGES',
                   'EXPERIENCE',
                   'CONTACT',
                   #'PHONE',
                   ]
        if not os.path.isfile(fileName) or resetFile:
            # Will create/reset the file as per the evaluation of above condition
            fOut = open(fileName, 'w')
            fOut.close()
        fIn = open(fileName)  #Open file if file already present
        inputString = fIn.read() #inString or inputString..help
        fIn.close()
        if len(inputString) <= 0:  #If File already exsists but is empty, it adds the header
            fOut = open(fileName, 'w')
            fOut.write(','.join(headers) + '\n')
            fOut.close()


class FiletoParse:

    def __init__(self, filename, debug=False):
        print("Hello User! Welcome to CV Extractor")
        fields = ["name", "meta", "location", "info", "projects", "industry", "education", "skills", "languages",
                  "experience", "contact"]
        self.file = Path(filename)
        self.extension = self.file.suffix
        #print(self.extension)
        self.debug = debug
        self.information = []
        self.readFile()
        self.infoDict = {x: None for x in fields}
        self.tokens = []
        self.lines = []
        self.sentences = []

    def write(self):
        # Individual elements are dictionaries
        #writeString = ''
        #with open('totalResultsCSV.csv', 'a') as fOut:
            #writeString += str(self.infoDict['fileName']) + ','
            #writeString += str(self.infoDict['name']) + ','
            #writeString += str(self.infoDict['role']) + ','
            #fOut.write(writeString)
        with open('results_' + self.file.stem + '.json', 'w') as fOut:
            #writeString += str(infoDict['fileName']) + ','
            #writeString += str(infoDict['name']) + ','
            #writeString += str(infoDict['role']) + ','
            fOut.write(json.dumps(self.infoDict, indent=4, sort_keys=True))

    def readFile(self):
        #self.extension = self.file.suffix
        if self.extension == ".txt":
            f = open(self.file, 'r')
            self.inputString = f.read()
            f.close()
        else:
            print("I'm sorry, this is an unsupported file format")
            self.inputString = None

    def processFile(self,):
        #self.inputString, info['extension'] = self.readFile(f)
        #info['fileName'] = f

        #info is information that goes inside the infoDict from that particular function.
        self.tokens, self.lines, self.sentences = FiletoParse.preprocess(self.inputString)
        self.matchName()
        self.matchMeta()
        #self.matchRole()
        self.matchLocation()
        self.matchInfo()
        self.matchProjects()
        self.matchIndustry()
        self.matchEducation()
        self.matchSkills()
        self.matchLanguages()
        self.matchExperience()
        self.matchContact()
        self.matchMeta()
        #self.matchPhone()

        # csv = exportToJSON()
        # csv.write(info)
        # self.information.append(info)
        # print(info)

    @staticmethod
    def preprocess(document):
        try:

            try:
                document = document.decode('ascii', 'ignore')
            except:
                document = document.encode('ascii', 'ignore')

            lines = [el.strip() for el in document.split("\n") if len(el) > 0]
            lines = [nltk.word_tokenize(el) for el in lines]
            lines = [nltk.pos_tag(el) for el in lines]
            sentences = nltk.sent_tokenize(document)
            sentences = [nltk.word_tokenize(sent) for sent in sentences]
            tokens = sentences
            sentences = [nltk.pos_tag(sent) for sent in sentences]
            dummy = []
            for el in tokens:
                dummy += el
            tokens = dummy
            return tokens, lines, sentences

        except Exception as e:
            print("Your error is here")
            print(e)
            return None, None, None

    def tokenize(self, inputString):
        try:
            self.tokens, self.lines, self.sentences = self.preprocess(inputString)
            return self.tokens, self.lines, self.sentences
        except Exception as e:
            print(e)

#meta
    def matchMeta(self):
        self.infoDict['meta'] = {"format": "FRESH@1.0.0"}

#below code finds name from CV
    def matchName(self):
        name = ()
            # open and read both files for comparison
        words1 = set(open("names.txt").read().split())
        words2 = set(self.inputString.split())
        # find intersection between both texts (i.e detect name)
        matches = words1.intersection(words2)
        name = ' '.join(matches)

        self.infoDict['name'] = str(name)


#below code finds role in CV
    #def matchRole(self):
        #role = ()
        #words1 = set(open("roles.txt").read().split())
        #words2 = set(self.inputString.split())
        # print(self.inputString)

        #matches = words1.intersection(words2)
        #role = matches

        #self.infoDict['info'] = {"brief": '', "label": str(role)}

#below code finds area in CV
    def matchLocation(self):
        area = ()
        words1 = set(open("locations.txt").read().split())
        words2 = set(self.inputString.split())
        # print(self.inputString)

        matches = words1.intersection(words2)
        area = ' '.join(matches)
        self.infoDict['location'] = {"region": str(area)}
        #print(self.infoDict)

#below code finds background in CV
    def matchInfo(self):
        #matching brief (aka background)
        copy = False
        background = ''
        for line in self.inputString.splitlines():
            if line.strip() == "Profile/Background":
                copy = True
                continue
            elif line.strip() == "Key project experience":
                copy = False
                continue
            elif line.strip() == "Industry expertise":
                copy = False
                continue
            if copy:
                background = background + str(line)

        #matching role aka label
        role = ()
        words1 = set(open("roles.txt").read().split())
        words2 = set(self.inputString.split())
        # print(self.inputString)

        matches = words1.intersection(words2)
        role = ' '.join(matches)

        self.infoDict['info'] = {"label": (str(role)), "brief": background}

#bwloe code finds keyprojects in CV
    def matchProjects(self):
        keyProject = ''
        copy = False
        for line in self.inputString.splitlines():
            if line.strip() == "Key project experience":
                copy = True
                continue
            elif line.strip() == "Industry expertise":
                copy = False
                continue
            if copy:
                keyProject = keyProject + str(line)
        self.infoDict['projects'] = keyProject
                # if self.debug:
                #     print("\n", pprint(self.infoDict), "\n")
                #     code.interact(local=locals())
                #     return background

#below code finds industry experience in CV
    def matchIndustry(self):
        industry = ''
        copy = False
        for line in self.inputString.splitlines():
            if line.strip() == "Industry expertise":
                copy = True
                continue
            elif line.strip() == "Education":
                copy = False
                continue
            if copy:
                industry = industry + str(line)
        array = industry.split('* ')
        del array[0]
        self.infoDict['industry'] = array

#below codes finds education from CV
    def matchEducation(self):
        education = ''
        copy = False
        for line in self.inputString.splitlines():
            if line.strip() == "Education":
                copy = True
                continue
            elif line.strip() == "Areas of specialization":
                copy = False
                continue
            if copy:
                education = education + str(line)
            array = education.split('* ')
            del array[0]
        #for institution array[-1] and for title array[0] but may not always be case
        self.infoDict['education'] = {"summary": array, "degree": ' '.join(array[0:1]), "history": [{"institution": array[1::2], "title": array[::2]}]}


#below code matches skills in CV
    def matchSkills(self):
        skills = ''
        copy = False
        for line in self.inputString.splitlines():
            if line.strip() == "Areas of specialization":
                copy = True
                continue
            elif line.strip() == "Languages":
                copy = False
                continue
            if copy:
                skills = skills + str(line)
        array = skills.split('* ')
        del array[0]
        self.infoDict['skills'] = array

#below code matches Languages
    def matchLanguages(self):
        languages = ()
        words1 = set(open("languages.txt").read().split())
        words2 = set(self.inputString.split())
        # print(self.inputString)

        matches = words1.intersection(words2)
        languages = matches

        self.infoDict['languages'] = str(languages)
        print(self.infoDict)

#below code matche experience
    #needs fixing because it displays more than just experience
    def matchExperience(self):
        experience = ''
        copy = False
        for line in self.inputString.splitlines():
            if line.strip() == "Prior professional experience":
                copy = True
                continue
            elif line.strip() == self.infoDict['name']: #i believe this line is at fault- how to call output from another function?l
                copy = False
                continue
            if copy:
                experience = experience + str(line)
        array = experience.split('* ')
        del array[0]
        self.infoDict['experience'] = array

#below code finds email
    def matchContact(self):
        email = ''
        for line in self.inputString.splitlines():
            if re.findall(r'[\w\.-]+@[\w\.-]+', line):
                email = email + str(line.replace('* ', ''))
        self.infoDict['contact'] = {"email": email}

#below code finds phone
    def matchPhone(self):
        phone = ''
        for line in self.inputString.splitlines():
            if re.findall(r'(/^((\+|00)32\s?|0)4(60|[789]\d)(\s?\d{2}){3}$/)', line):
                phone = phone + str(line)
                print(phone)
        self.infoDict['phone'] = phone

if __name__ == "__main__":
    verbose = False
    if "-v" in str(sys.argv):
        verbose = True
        pathy = '/Users/samareaa/PycharmProjects/CVproject/CVs/*.txt'
        text_files = glob.glob(pathy)

        files = set(text_files)
        files = list(files)
        print("%d files identified" % len(files))

        # info is a dictionary that stores all the data obtained from parsing!
        for f in files:
            print("Reading File...Please wait %s" % f)
            p = FiletoParse(f, verbose)
            p.processFile()
            p.write()







