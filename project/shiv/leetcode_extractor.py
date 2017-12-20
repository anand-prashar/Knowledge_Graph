import json
from lxml import html
from os import listdir, getcwd, linesep, path

	
def extract_to_json(htmlDirectory, outputJsonFile):
	fp = open(outputJsonFile, 'w')
	filesLeft = len(htmlDirectory)
	baseUrl = 'https://leetcode.com/'
	errLog = open('ERROR.log','w')
	for htmlFile in htmlDirectory:
		try:
			JsonObject = {}
			domTree = html.parse( open(htmlFile) )

			real_name = domTree.xpath("""//h4[@class='realname']""")
			if real_name: JsonObject['Real_Name'] = real_name[0].strip()
			else: JsonObject['Real_Name'] = None

			user_name = domTree.xpath("""//p[@class='username']""")
			if real_name: JsonObject['User_Name'] = user_name[0].strip()
			else: JsonObject['User_Name'] = None
			
			linkedin = domTree.xpath("""//div[@class='social-icons'][1]//a[@class='fa-stack fa-lg'][3]/@href""")
			if linkedin: JsonObject['Linked_In'] = linkedin[0].strip()
			else: JsonObject['Linked_In'] = None

			googleplus = domTree.xpath("""//div[@class='social-icons'][1]//a[@class='fa-stack fa-lg'][1]/@href""")
			if googleplus: JsonObject['Google_Plus'] = googleplus[0].strip()
			else: JsonObject['Google_Plus'] = None

			github = domTree.xpath("""//div[@class='social-icons'][1]//a[@class='fa-stack fa-lg'][4]/@href""")
			if github: JsonObject['Github'] = github[0].strip()
			else: JsonObject['Github'] = None

			fb = domTree.xpath("""//div[@class='social-icons'][1]//a[@class='fa-stack fa-lg'][2]/@href""")
			if fb: JsonObject['Facebook'] = fb[0].strip()
			else: JsonObject['Facebook'] = None

			website = domTree.xpath("""//li[@class='list-group-item'][1]//span[@class='pull-right content-right-cut'][1]""")
			if website: JsonObject['Website'] = website[0].strip()
			else:  JsonObject['Website'] = None

			country = domTree.xpath("""//li[@class='list-group-item'][2]//span[@class='pull-right content-right-cut'][1]""")
			if country: JsonObject['Country'] = country[0].strip()
			else:  JsonObject['Country'] = None

			occupation = domTree.xpath("""//li[@class='list-group-item'][3]//span[@class='pull-right'][1]""")
			if occupation: JsonObject['Occupation'] = occupation[0].strip()
			else:  JsonObject['Occupation'] = None

			company = domTree.xpath("""//li[@class='list-group-item'][4]//span[@class='pull-right content-right-cut'][1]""")
			if company: JsonObject['Company'] = company[0].strip()
			else:  JsonObject['Company'] = None

			finished_contests = domTree.xpath("""//li[@class='list-group-item'][4]//span[@class='pull-right content-right-cut'][1]""")
			if finished_contests: JsonObject['Finished_Contests'] = finished_contests[0].strip()
			else:  JsonObject['Finished_Contests'] = None

			rating = domTree.xpath("""//li[@class='list-group-item'][4]//span[@class='pull-right content-right-cut'][1]""")
			if rating: JsonObject['Rating'] = rating[0].strip()
			else:  JsonObject['Rating'] = None

			global_ranking = domTree.xpath("""//li[@class='list-group-item'][4]//span[@class='pull-right content-right-cut'][1]""")
			if global_ranking: JsonObject['Global_Ranking'] = global_ranking[0].strip()
			else:  JsonObject['Global_Ranking'] = None
			
			fp.write( json.dumps(JsonObject)+linesep )
			filesLeft-=1; print '--> Files left: '+str(filesLeft)

			

		except Exception as _:
			print 'FAILED IN FILE : '+htmlFile
			errLog.write(htmlFile+'\n')

	fp.close()   
	errLog.close()

	print 'Extracted to: '+outputJsonFile


	
rootDir = getcwd()

currentDirList = [rootDir+'\\'+childDir for childDir in listdir(rootDir) if path.isdir(childDir) ]

for currentDir in currentDirList:
	#aggregatedFilesList = []
	aggregatedFilesList = [currentDir+'\\'+hfile for hfile in listdir(currentDir) if hfile.split('.')[-1]=='html']

	if aggregatedFilesList == []: continue
	currentDir = currentDir.split('\\')[-1]

	extract_to_json(aggregatedFilesList, 'Leetcode_scrapped_'+currentDir+'.jl')
