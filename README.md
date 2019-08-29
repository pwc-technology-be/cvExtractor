# cvExtractor
![meme](https://user-images.githubusercontent.com/49131000/63941659-5b62ef80-ca6c-11e9-8e8a-d894a0ec2753.png)

## What is this sorcery?
Long gone will be the days where the manual "copy/paste" actions will be needed to transfer your
information to a new CV Template thanks to the cvExtractor. 
This python script will identify the various components from the TalentLink CV (important, as it only
works with talentLink profiles for now) and transform them into a JSON file under the FRESH schema
which can then be ran through hackmyresume to apply the data to a different template.
Stay tuned for updates on completion of Europass template...

## Like the idea? Let's see how it works!
cvExtractor is designed to be simple and easy to use. Below is a step by step guide that will help
with the installation and running of the program. 

### Step 1: Download
Download the contents of the git repository to desired location on your computer.
(The shorter the path, the easier)

Also download your CV from talentlink as a .txt file, and save it in a folder called CVs inside 
the same folder containing the newly downloaded cvExtractor repository.

<img width="528" alt="Capture" src="https://user-images.githubusercontent.com/49131000/63938231-9b25d900-ca64-11e9-98c5-49cb88fed8fa.PNG">

### Step 2: Running the script
Once you've set up the previous step, the script should be able to run and generate an output JSON
file inside the folder under the name results_filename.json where filename is the name of the .txt
file containing your talentlink CV

### Step 3: Applying extracted data to new templates
In order to manage this final stage, a few preparations need to be taken:

>1.Download and install the latest version of [Node.js](https://nodejs.org/en/)

>2.Now in terminal, you can install hackmyresume with the following command:
```shell
npm install hackmyresume -g
```
>once everything is correctly installed, you can proceed to the next step.

When you are ready to generate your resume, you will need to reference the location of the folder as you installed it:
```shell
hackmyresume build results_filename.json TO out/resume.all -t positive
```
and you should see a terminal that looks somewhat like this:

<img width="272" alt="snapshot1" src="https://user-images.githubusercontent.com/49131000/63937885-ce1b9d00-ca63-11e9-937e-1ee7f11d4b36.PNG">


If the above image looks familiar then congratulations! You have successfully generated a new resume
in various formats (html, doc, json, yml) and will find these in your folder under a folder called 'out'.
