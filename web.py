"""Web Search Engine

This module will show the page of the sites. A form will be displayed allows the user to input keywords and return a list of urls.
"""
from flask import Flask
from flask import request
from paging_rank_system import PagingRank
import copy

# noise word stored in a set for checking
noise = {"a", "an", "the", "and", "or", "of", "to", "be", "is", "in", "out", "by", "as", "at", "off"}
# dictionary to store alphabetical order
alpha_dict = {}
# fill the dictionary <character, order> a < A < b < B...z < Z
k = 1
for i in range (ord('a'), ord('z') + 1):
    k += 1
    ch = chr(i)
    alpha_dict[ch] = k
    temp = ord(ch) - 32
    temp_char = chr(temp)
    k += 1
    alpha_dict[temp_char] = k
    
    
# Initialize flask framework
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """Redirect to search page when users type in the address of website
       Parameters
       -----------
       None

       Returns
       -----------
       HTML
           Redirect to the search page
    """
    return signin_form()

@app.route('/signin', methods=['GET'])
def signin_form():
    """Search Page for inputting keywords
       Parameters
       -----------
       None

       Returns
       -----------
       HTML
           a web page for user's input
    """
    
    return '''<!DOCTYPE html>
              <html>
              <head>
                <title>Macrominer</title>
                <style>
                div {
                      height: 200px;
                      width: 400px;
                      position: fixed;
                      top: 50%;
                      left: 50%;
                      margin-top: -100px;
                      margin-left: -200px;
                }
              </style>
              </head>
              <body>
              <div><form action="/signin" method="post">
              <center><label for="story">Macrominer</label></center>
              <textarea id="inputContent" name="inputContent"
              rows="1" cols="50">
              </textarea>
              <center><button type="submit">Happy Search</button></center>
              </form>
              </div>
              </body>
              <html>'''


@app.route('/signin', methods=['POST'])
def signin():
    """Handle the user's post and feedback the information
       Parameters
       -----------
       None

       Returns
       -----------
       HTML
           The search results of the users
    """
    
    x = str(request.form['inputContent']).strip()
    if x != "":
        arr = filter_noise(x)
                    
        shifts = shift(arr)
        descriptors = alphabetizer(shifts)
        urls = '''<!DOCTYPE html>
              <html>
              <head>
                <title>Macrominer</title>
                <style>
                div {
                      height: 550px;
                      width: 1200px;
                      overflow: scroll;
                      position: fixed;
                      top: 20%;
                      left: 20%;
                      margin-top: -100px;
                      margin-left: -200px;
                }
              </style>
              </head>
              <body>
              <div><form action="/signin" method="post">
              <font size = "7" color= "red"><label for="story">Macrominer</label></font>
              <textarea id="inputContent" name="inputContent"
              rows="2" cols="50"></textarea>
              <button type="submit"><font size = "6">Happy Search</font></button>
              </form>'''
        urls += '''<font size="6" color="blue">'''
        for item in arr:
            print("Your Input: &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&" + item)
            pr = PagingRank()
            data = pr.start()
            for record in data:
                keywords = record[1].split(" ")
                if item.lower() in keywords:
                    urls +=  '''<a href ="''' +  record[2] + '''"''' + '''>''' + record[2] + '''</a>''' + "<br>"
                    urls +=  '''Description: ''' + record[1] if len(record[1]) < 200 else record[1][0:200] + "<br>"
                    urls += "<br/>"
        for item in descriptors:
            urls += '''<a href ="''' + "http://" + ".".join(item) + "." + "edu" + '''">''' + "http://" + ".".join(item) + "." + "edu" + "</a><br>"
            urls += '''<a href ="''' + "http://" + ".".join(item) + "." + "com" + '''">''' + "http://" + ".".join(item) + "." + "com" + "</a><br>"
            urls += '''<a href ="''' + "http://" + ".".join(item) + "." + "org" + '''">''' + "http://" + ".".join(item) + "." + "org" + "</a><br>"
            urls += '''<a href ="''' + "http://" + ".".join(item) + "." + "net" + '''">''' + "http://" + ".".join(item) + "." + "net" + "</a><br>"
        urls += '''
                    </font>
                  </div>
                </body>
              <html>'''
        return urls
    return signin_form()

def filter_noise(string):
    """pretreat the string and filter the noise words
       Parameters
       -----------
       string: str
           the string from user's input

       Returns
       -----------
       list
           a list of strings after filtering  noise words and removing empty space
    """
    
    arr = string.split(" ")
    res = []
    for item in arr:
        temp = item.strip()
        if temp not in noise and temp != "":
            res.append(temp.strip())
    return res


def shift(arr):
    """Circular shifting the string
       Parameters
       -----------
       arr: list
           a list of string from the key words of users'

       Returns
       -----------
       list
           a list of strings after shifting the words in the string
    """
    res = []
    size = len(arr)
    for i in range(size):
        temp = copy.deepcopy(arr)
        res.append(temp)
        first = arr[0]
        arr.remove(first)
        arr.append(first)
    return res

def alphabetizer(arr):
    """order the shifted string with ascending alphabetical order
       Parameters
       -----------
       arr: list
           a list of string after shifting

       Returns
       -----------
       list
           a list of ordered strings 
    """
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if compare(arr[i], arr[j]) > 0:
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp
    return arr

def compare(arr1, arr2):
    """Compare string with alphabetical order
       Parameters
       -----------
       arr1: list
           a list of string for comparing
       arr2: list
           a list of string for comparing

       Returns
       -----------
       int
           represent the comparison of string1 and string2
    """
    val1 = "".join(arr1)
    val2 = "".join(arr2)
    i = 0
    j = 0
    while i < len(val1) and j < len(val2):
        if alpha_dict[val1[i]] == alpha_dict[val2[j]]:
            i += 1
            j += 1
        else:
            return alpha_dict[val1[i]] - alpha_dict[val2[j]]
    if i == len(val1):
        return len(val2) - j
    else:
        return len(val1) - i

if __name__ == '__main__':
    app.run()
