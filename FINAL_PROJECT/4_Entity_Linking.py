'''
Created on Nov 26, 2017

@author: anand
'''
## paste in file: 1_github_merger to make it work

def entity_linking_algorithm(githubDict):
    
    entity_linking_Dict={}
    
    ignoreSet = set(['http://none','http://www.google.com','http://google.com','http://n/a','http://N/A','http://stackoverflow.com','http://www.stackoverflow.com',
        'http://NA','http://localhost','http://na','http://www.example.com','http://127.0.0.1','http://www.yahoo.com','http://no','http://example.com',
        'http://stackoverflow.com/','http://localhost/','http://google','http://none.com','http://-','http://www.gmail.com','http://www.google.com/',
        'http://about:blank','http://www.facebook.com','http://nil','http://www.google.co.uk','http://www.microsoft.com','http://www.none.com',
        'http://www','http://donthaveone','http://noneyet','http://www.google.ca','http://nope','http://home','http://127.0.0.1/','http://nothing',
        'http://nowebsite','http://NONE','http://undefined','http://yahoo.com',
        'http://www.hackerrank.com','http://Donthaveone','http://notyet','http://www.google.de','http://www.google.co.in','http://Google',
        'http://stackoverflow.com/questions/ask','http://www.cafcat.com','http://www.slashdot.org','http://gmail.com',
        'http://comingsoon','http://www.jetbrains.com','http://yahoo','http://slashdot.org','http://www.reddit.com','http://www.asp.net',
        'http://facebook.com','http://non','http://hotmail.com','http://ld','http://test.com','http://google.com/','http://www.com','http://www.ebuildy.com',
        'http://example.org','http://Nowebsite','http://www.thoughtworks.com','http://www.nowebsite.com','http://donthave','http://www.zombo.com',
        'http://msdn.microsoft.com','http://noneatm','http://google.ca','http://www.hotmail.com','http://hackerrank.com','http://NULL','http://N.A',
        'http://www.example.com/','http://www.nowhere.com','http://asd','http://www.oracle.com','http://www.telerik.com','http://google.co.in',
        'http://localhost:8080','http://yes','http://www.apple.com','http://Website','http://android','http://NIL','http://underconstruction',
        'http://www.newrelic.com','http://www.redgum.com.au','http://www.msn.com','http://www.interactivemesh.com','http://NoneYet','http://www.alphabricks.com',
        'http://soon','http://www.google.com.au','http://nohomepage','http://inprogress','http://test','https://www.hackerrank.com/abhishek008',
        'http://.','https://stackoverflow.com/users/510573/alan-souza','http://www.yammer.com','http://N/a','http://mtaulty.com','http://www.epam.com',
        'http://www.google.nl','linkedin.com','a.com','http://None','undefined',
        'https://www.linkedin.com/profile/public-profile-settings?trk=prof-edit-edit-public_profile'])

    
    #process blog file
    with open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\Reference\\blogFile.csv','rb') as f:
        csvR= csv.reader(f, delimiter=',', quoting = csv.QUOTE_ALL)
        for row in csvR:
            if row[0] in ignoreSet: continue
            #print row[0]
            try:
                if not (len(row[0].split('http://')[1])>1 and '.' in row[0].split('http://')[1] ): continue
            except Exception as _:
                pass
            new_common_set = set(row)
            for url in row:

                
                if url not in entity_linking_Dict:
                    entity_linking_Dict[url] = new_common_set
                else:    
                    entity_linking_Dict[url] = entity_linking_Dict[url] | new_common_set
    
    #process githubDict itself
    for k, jsonObj in githubDict.iteritems():

        if jsonObj['LinkedEntity'] == None:
            jsonObj['LinkedEntity'] = set([jsonObj['url']])
        elif jsonObj['url'] not in jsonObj['LinkedEntity']:
            jsonObj['LinkedEntity'] = set([jsonObj['url']]) | jsonObj['LinkedEntity']
            
            
        if jsonObj['url'] not in entity_linking_Dict:
            entity_linking_Dict[ jsonObj['url']] = jsonObj['LinkedEntity']
        else:
            try:
                new_common_set = entity_linking_Dict[ jsonObj['url']] | jsonObj['LinkedEntity']
                for url in list(jsonObj['LinkedEntity']):
                    entity_linking_Dict[url] = new_common_set
            except Exception as _:
                pass
                
    print 'Linked :)'
    
    opFile = 'C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\gitHub_linking_mapper.csv'
    
    f_mapper = open(opFile,'wb')
    csv_f_mapper = csv.writer(f_mapper, delimiter=',', quoting = csv.QUOTE_ALL)
    uniqueMappingSet = set([])
    for mapping in entity_linking_Dict.itervalues():
        mapping = tuple(sorted(mapping))
        if mapping not in uniqueMappingSet:
            uniqueMappingSet.add( mapping)
    # reorder and save mapping, to be used by other files
    #uniqueMappingList = map( list, uniqueMappingSet))
    uniqueMappingList = [(len(x),x) for x in list(uniqueMappingSet) if len(x)>1]
    uniqueMappingList = sorted( uniqueMappingList, key = lambda x: x[0], reverse = True)

    for rowList in uniqueMappingList:
        csv_f_mapper.writerow( list(rowList[1]))
    
    print 'saved File'    
    