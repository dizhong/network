
# implements a basic parser on top of html.parser

from html.parser import HTMLParser

class Parser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.csrfmiddlewaretoken = ""
        self.urls = []
        self.flag = ""

    def get_csrfmiddlewaretoken(self):
        return self.csrfmiddlewaretoken;

    def get_urls(self):
        temp = self.urls
        self.urls = []
        return temp

    def get_flag(self):
        return self.flag

    def handle_starttag(self, tag, attrs):
        #print("Starttag: ", tag)
        if (tag == "input"):
            attrs = dict(attrs)
            if (("name" in attrs) and (attrs["name"] == "csrfmiddlewaretoken")):
                self.csrfmiddlewaretoken = attrs["value"]
        elif (tag == "a"):
            attrs = dict(attrs)
            #print(attrs)
            if ("href" in attrs) and ("/fakebook" in attrs["href"]):
                #screen out the ones that do not start with /fakebook
                self.urls.append(attrs["href"]);


    def handle_data(self, data):
         #print("Data: ", data)
         if "FLAG:" in data:
             split = data.split(" ")
             self.flag = split[1]
             print(self.flag)
             #print(data)
         
