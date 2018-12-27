from bs4 import BeautifulSoup
import requests
import re
from constants import limit,skip_words
import optparse

def parse_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--url', dest="url",help="Valid URL string", default='https://hiverhq.com/')
    parser.add_option('-l', '--limit', dest="limit", help="Limit of top words",default=limit)
    return parser.parse_args()

def fetch_top_words(url,limit=limit):
    #Request the given URL
    try:
        home_page_html_data=requests.get(url)
    except requests.exceptions.RequestException as error_message:
        print (error_message)
        exit(1)

    #Soup the output response
    soup = BeautifulSoup(home_page_html_data.content,'html.parser')

    #remove the script tag. Removing all the Javascript content
    [script_tag.extract() for script_tag in soup.findAll('script')]

    #Extract text out of the remaing HTML content
    text_data=soup.get_text()

    #Remove all the new line charcaters
    text_data=text_data.replace('\n',' ')

    #Remove special characters. More characters can be added to the existing list
    text_data=re.sub(r'[0-9|+|-|,|*|?|(|)|/]',r'',text_data)
    word_list=text_data.split()
    word_hash_map={}
    for word in word_list:
        word=word.strip()

        #Ignore the words with length 1 and pre-defined set of "skip words"
        if len(word)>1 and word not in skip_words:
            word_hash_map.setdefault(word,0)
            word_hash_map[word]= word_hash_map[word]+1

    #Sort the hash_map
    sorted_word_list = sorted(word_hash_map.items(), key=lambda kv: kv[1],reverse=True)
    for i in range(limit):
        print ("{} : {}".format(sorted_word_list[i][0],sorted_word_list[i][1]))

if __name__ == '__main__':
    options, args = parse_arguments()
    print("Please wait. Listing the top {} most occuring words".format(options.limit))
    fetch_top_words(options.url,int(options.limit))
