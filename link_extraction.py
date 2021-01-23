## List of professors https://www.cs.purdue.edu/research/
## Common test pages
# https://www.cs.purdue.edu/people/faculty/popescu.html (Contains publications)
# https://www.cs.purdue.edu/people/faculty/rego.html
# https://www.cs.purdue.edu/people/faculty/apothen.html (Contains publications, with links)
# https://www.cs.purdue.edu/people/faculty/apsomas.html (Blank page, only external links)
# https://www.cs.purdue.edu/people/faculty/mingyin.html
# https://www.cs.purdue.edu/people/faculty/dgleich.html (Issues with getting extLinks, no .jpg found?)

from bs4 import BeautifulSoup
import urllib.request
import re

html_page = None
soup = None

#Run whenever using a new site before running any other functions
def getPageData(site):
    global html_page, soup
    html_page = urllib.request.urlopen(site)
    soup = BeautifulSoup(html_page, features='lxml')
    

# Returns array of external links (personal webpage and research pages) from Professor's website
# Can set logData to True to generate a txt file of links and indices found on the page
def getExternalLinks(site, logData=False):
    # html_page = urllib.request.urlopen(site)
    # soup = BeautifulSoup(html_page, features='lxml')
    rawLinks = soup.find_all('a', href=True)
    links = []
    jpgIndex = -1
    footerIndex = -1
    
    for i in range(len(rawLinks)):
        links.append(rawLinks[i].get('href'));
        if(jpgIndex == -1 and links[i].find(".jpg") != -1): #Finds index of jpg file and '#footerone'
            jpgIndex = i
        elif(footerIndex == -1 and links[i] == "#footerone"):
            footerIndex = i
    
    if(logData):
        ## Write links to txt file with indices. Useful for debugging.
        print(links[jpgIndex+1:footerIndex]) #Prints returned values
        with open("links_test.txt", "w") as f: #Logs all links found with indices
            i = 0
            for line in links:
                f.write(str(i) +" " + line + "\n")
                i += 1;
                
    
    return links[jpgIndex+1:footerIndex]

#Returns publications as a dictionary
def getPublications():
    titleArray = [None]
    linkArray = [None]
    soupText = str(soup.body)
    startIndex = soupText.find("Selected Publications")
    if(startIndex != -1):
        #startIndex += 50
        endIndex = soupText.find("lastupdate")
        endIndex -= 26
        targetText = soupText[startIndex : endIndex]
        
        #Remove html tags from text
        targetText = targetText[targetText.find(">")+1:targetText.rfind("</div>")+6]
        targetText = targetText.replace("<em>", "")
        targetText = targetText.replace("</em>", "")
        targetText = targetText.replace("<strong>", "")
        targetText = targetText.replace("</strong>", "")
        targetText = targetText.replace("<p>", "")
        targetText = targetText.replace("</p>", "")
        
        titleIndices = findInstancesOfString(targetText,'<div style="margin-bottom: 1em;">')
        #print(targetText[titleIndices[1]:targetText.find("</div>",titleIndices[1])])
        
        titleArray = [None] * len(titleIndices)
        linkArray = [None] * len(titleIndices)
        
        for i in range(len(titleIndices)):
            titleArray[i] = targetText[titleIndices[i]:targetText.find("</div>",titleIndices[i])]
            titleArray[i] = titleArray[i][targetText.find(">"):] #Removes leading HTML tag
            if(titleArray[i].find("href=") != -1): #If a link is found in the entry:
                linkArray[i] = titleArray[i][titleArray[i].find('="')+2:titleArray[i].find('">')]
            
    return [titleArray, linkArray]


def findInstancesOfString(string, target):
    results = []
    for match in re.finditer(target, string):
        results.append(match.start())
    return results
        
    

## Misc debug lines
#getPageData("https://www.cs.purdue.edu/people/faculty/popescu.html") #Just publications
#getPageData("https://www.cs.purdue.edu/people/faculty/apothen.html") #Publications and links
#getPageData("https://www.cs.purdue.edu/people/faculty/dgleich.html") #No publications
#testSoup = getExternalLinks(True)
#print(getPublications())
#result = getPublications()