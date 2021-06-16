import urllib.request
import urllib.error
import urllib.parse
import threading
import queue

threads       = 50
target        = input("Enter Target URL: ")
wordlist      = "/home/zeus/Desktop/SVN_wordlist/all.txt"
resume        = None
user_agent    = "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"

print("\n\tX X X X  WEBSITE BRUTE FORCE ATTACK   X X X X Xby ZEUS\n\n")

def build_wordlist(wordlist):
    print("[*] Building Wordlist")
    # read in the word list
    fd = open(wordlist,"r")
    raw_words = [line.rstrip('\n') for line in fd]
    fd.close()
    word = raw_words
    found_resume = False
    words        = queue.Queue()

    for word in raw_words:

        if resume:

            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True 
                    print("Resuming wordlist from: %s" % (resume))
        else:
            words.put(word)
    print("[*] Wordlist Build\n")
    return words 



def dir_bruter(extensions=None):
    
    while not word_queue.empty():
        attempt = word_queue.get()
        
        attempt_list = []
        
        # check to see if there is a file extension, if not,
        # it's a directory path we are bruting
        if "." not in attempt:
            attempt_list.append("/%s/" % (attempt))
        else:
            attempt_list.append("/%s" % (attempt))

        # if we want to bruteforce extensions 
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s" % (attempt, extension))

        # iterate over our list of attempts
        for brute in attempt_list:

            url = "%s%s" % (target, urllib.parse.quote(brute))

            try:
                header = {"User-Agent": user_agent}
                request = urllib.request.Request(url, headers=header)  

                response = urllib.request.urlopen(request)

                if len(response.read()):
                    print("[%d] => %s" % (response.code, url))

            except urllib.error.HTTPError as e:
                if e.code != 404:
                    print("!!! %d => %s" % (e.code, url))
               
                pass
                
            except urllib.error.URLError:
                pass        


word_queue = build_wordlist(wordlist)
extensions = [".php",".bak",".orig",".inc"]
print("[*] Starting Content Brute Forcing with Wordlist\n")

temp = 0
for i in range(threads):
    temp = temp + 1;
    t = threading.Thread(target=dir_bruter,args=(extensions,))
    t.start() 
    
if temp == 49:
    print("\n----------BRUTE FORCE ATTACK FINISHED------------")    
