# Resume_project
Sorting of resumes according to job description using natural language processing.

DESCRIPTION:
    Comparision of text is done between JobDescription(.txt) file and bunch of resumes(.pdf) using natural language processing. Two python files resume.py and flask_old.py(which uses flask) are used in this project. Flask is a python web framework which uses python decorators. They help in calling a function before the user's request is processed.
    
REQUIREMENTS:
    Python 3.7.3 is used in this project. In addition to python following libraries are required to run the code. For resume.py code slate3K, re, nltk,ssl(for MAC users), logging, sklearn, pathlib, operator are required. For flask_old.py flask, werkzeug, os, pathlib, re, resume(i.e., resume.py) are used. And also download stopwords from nltk package using nltk.download('stopwords') (Please check the note for more details regarding nltk.download()). 
    
WORKING:
    In order to use flask framework, it should be running in background. So first run the flask_old.py code. It displays a link http://127.0.0.1:5000/. Click the link. If the link is not displayed type the link in any browser to open. Then upload the resumes and jobDescription files which will be stored in local machine(please check the NOTE below) and click compare button. After clicking compare button the names and scores will be listed in tabular form. Clicking the names will redirect to file's path. This is the working of the code.
    
CREDITS:
    Author: Swaroop Bayya
    Contributors: Hemanth Yamijala
 
NOTE::
    Since the JobDescription and resumes after uploading will be stored in local machine, before running flask_old.py change the lines 12 and 14 which contains variables like app.config['UPLOAD_RESUME'] which holds resumes path after uploading and app.config['UPLOAD_JD'] which holds JobDescription path after uploading. Change the paths according to your desired path.
    
Regarding nltk.download() for MAC users because of some certificate issues some extra lines(221 - 228) are added at the end. After downloading is done, the lines can be removed to avoid re-downloading it.
    
