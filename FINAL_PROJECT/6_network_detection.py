'''
Created on Nov 29, 2017

@author: anand
'''

'''
Created on Nov 14, 2016

@author: anand
'''
import community
import networkx as nx
import matplotlib.pyplot as plt


def readFile():
    fHandle = open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\tableau\\opFile_NetworkAnalysis.txt')
    nodeList = set();edgeList = set()
    
    for fileRow in fHandle:
        #try:
        node1,node2 = fileRow.split(' ')
        #except Exception as _:
        #    pass
        node1 = node1                              # <=================== sorting wont work properly on STRINGS, while printing result
        node2 = node2.split('\n')[0]
        nodeList.add(node1)
        nodeList.add(node2)
        if node1<node2: edgeList.add((node1,node2)) 
        else: edgeList.add((node2,node1)) 
    
    nodeList = list(nodeList)    
    edgeList = sorted( list(edgeList))
    return (nodeList,edgeList)    

def createGraph(nodeList,edgeList):
    
    G=nx.Graph()
    G.add_nodes_from(nodeList)
    G.add_edges_from(edgeList)
    G = G.to_undirected()

    #nx.draw_networkx(G, arrows=False, with_labels = True)
    #plt.axis('off')
    #plt.show()
    
    return G


def get_Partitions(nodeList, inputGraph):
    
    partitionNo = 1
    partitionDict = {}
    nodeListCp = nodeList[:]
    #for node in nodeListCp:
    while nodeListCp != []:
        node = nodeListCp[0]
        propagte_and_remove(node, nodeListCp, partitionDict, inputGraph, partitionNo)
        partitionNo +=1
        
    return partitionDict    

def propagte_and_remove(node, nodeList, partitionDict, inputGraph, partitionNo):
    
    try:
        nodeList.remove(node)
        partitionDict.setdefault(node,partitionNo)
        neighborsList = inputGraph.neighbors(node)
        
        for neighbor in neighborsList:
            propagte_and_remove(neighbor, nodeList, partitionDict, inputGraph, partitionNo)
            
    except ValueError: # Do nothing, if it was already removed
        return

def getBestCommunityGraph(inputGraph, nodeList):
    
    prevModularity = 0

    while True:
        
        prevInputGraph = inputGraph.copy()
             
        edgeBetweennessValues = nx.edge_betweenness_centrality(inputGraph)   # <------------------------------- 
        maxValue = -1
            
        for value in edgeBetweennessValues.itervalues():
            if maxValue < value:
                maxValue = value
            
        for breakEdge,value in edgeBetweennessValues.iteritems():
            if value == maxValue:
                inputGraph.remove_edge(breakEdge[0], breakEdge[1])
                #print '\nMax betweenness for: ',breakEdge,' .... Value=',maxValue  
    ################
    
        partition = get_Partitions(nodeList, inputGraph); 
        print partition
        
        try:
            currModularity = community.modularity( partition, inputGraph ) 
            print 'Modularity = ', currModularity
        except ValueError:
            print 'Modularity = undefined !'
            break # break Loop    
        
        if prevModularity > currModularity: 
            break
        prevModularity = currModularity
        
        print '\n----------------------------------------------- \n'
                   
    
    
    print '\n\n=============================================================\n'
    
    print get_Partitions(nodeList, prevInputGraph)
    print 'Final Modularity = ', prevModularity

    return prevInputGraph

#===============================================================================
# def getTreefromGraph(graph, root, nodeList, edgeList):
#     
#     communityNodeList=nodeList[:]
#     while communityNodeList!=[]:
#         
#===============================================================================
         
######################################################################################################################
######################################################################################################################

(nodeList, edgeList) = readFile()
inputGraph = createGraph(nodeList, edgeList)
inputGraphBkp = inputGraph.copy()

bestGraph = getBestCommunityGraph(inputGraph, nodeList)



########### OUTPUT#############
print '\n\n\n'
partitions = get_Partitions(nodeList, bestGraph)
clusters=[] 
maxPartition= 0
for key,value in partitions.iteritems():   
    if maxPartition< value:
        maxPartition = value
for i in range(0,maxPartition):                  #  ???????????? max+1 
    clusters.append([])
for key,value in partitions.iteritems():   
    clusters[value-1].append(key)
for cluster in clusters:
    print sorted(cluster)    

###### GUI
#nx.draw_networkx(inputGraphBkp, arrows=False, with_labels = True)
#plt.axis('off')
#plt.savefig('anand_prashar_communities.png')
#plt.show()    

#===============================================================================
# pos = nx.spring_layout(inputGraphBkp)
# count = 0
# 
# color = ['b','g','y','m','r','c']
# for com in set(partitions.values()):
#     count = count + 1
#     list_nodes = [nodes for nodes in partitions.keys() if partitions[nodes] == com]
#     selectedColor = color[count % len(color)]
#          
#     nx.draw_networkx_nodes(inputGraphBkp, pos, list_nodes, node_size = 100, node_color= selectedColor, with_labels=True )
#      
# nx.draw_networkx_edges(inputGraphBkp, pos, alpha=0.5)
# 
# plt.axis('off')
# plt.savefig('anand_prashar_communities.png')
# plt.show()  
#===============================================================================
