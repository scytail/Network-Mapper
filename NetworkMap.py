import sys

#checks for available version (ipaddress module included in 3.3 and after)
version = sys.version_info
if version[0] < 3 or (version[0] == 3 and version[1] < 3):
    raise OSError("You are not using the correct version of Python. Python 3.3 or higher is required for this program to execute.")

import networkx as nx
import matplotlib.pyplot as plt
import ipaddress as ipaddr
import argparse                   #Command line arguments
import os                         #Exception handling

#http://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3
def hierarchy_pos(G, root, width=1, vert_gap = 0.2, vert_loc = 0, xcenter = 0.5 ):
    '''If there is a cycle that is reachable from root, then result will not be a hierarchy.
       G: the graph
       root: the root node of current branch
       width: horizontal space allocated for this branch - avoids overlap with other branches
       vert_gap: gap between levels of hierarchy
       vert_loc: vertical location of root
       xcenter: horizontal location of root
    '''
    def h_recur(G, root, width=1, vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, 
                  pos = None, parent = None, parsed = [] ):
        if(root not in parsed):
            parsed.append(root)
            if pos == None:
                pos = {root:(xcenter,vert_loc)}
            else:
                pos[root] = (xcenter, vert_loc)
            neighbors = G.neighbors(root)
            if parent != None:
                neighbors.remove(parent)
            if len(neighbors)!=0:
                dx = width/len(neighbors)
                nextx = xcenter - width/2 - dx/2
                for neighbor in neighbors:
                    nextx += dx
                    pos = h_recur(G,neighbor, width = dx, vert_gap = vert_gap, 
                                        vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos, 
                                        parent = root, parsed = parsed)
        return pos
        
    return h_recur(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5)

def ipNetworkFromMask(addressString,subnetMaskString):
    '''
       Converts a given address (in the form of a string)
       and a subnet mask (as a string) to an IPv4Network object,
       which allows manipulation and displays as a CIDR notated network.
    '''
    return ipaddr.ip_network("{0}/{1}".format(addressString,subnetMaskString),strict=False)

#Function to make sure user has passed valid file"    
def openFile(fileName):
    try:
        f = open(fileName)
        f.close()
    except OSError:
        print ("Invalid configuration file name, use '-h' argument for help menu")
        sys.exit(0)
        
    return(fileName)
            
def readConfigFile(fileNameString, vlanFileString, contextString):
    if vlanFileString == None:
        print("vlan file string is none")
    '''
       Reads a given firewall configuration file for its VLAN configuations
    '''
    #static variables used when reading the individual vlan data lists
    CONFIG_TAG_INDEX = 0
    NAME_INDEX = 1
    VLAN_IP_INDEX = 2
    VLAN_MASK_INDEX = 3
    VLAN_NAME_INDEX = 1
    
    context = "hostname " + contextString #the line of the context that starts the configuration in the dmz file
    vlanContext = "context " + contextString #the line of the context that starts the configuration in the vlan file
    hostname = "" #the hostname to return
    previousLine = "" #pre-declaring a string to be used in the case of a bridged context
    vlans = [] #the list of interfaces to return
    vlanDataList = []  #list of dmzs with their corresponding vlan data
    vlanDataInfo = "" # string containing the vlan number to be added to the image
    
    #open file containing vlan numbers for interfaces and add them to a list
    if vlanFileString != None:
        with open(vlanFileString) as v:
            for line in v:
                try:
                    while vlanContext not in line:
                        line = next(v)
                    line = next(v)
                    while "!" not in line:
                        vlanDataList.append(line.rstrip())
                        line = next(v)
                    break
                except StopIteration:
                    print("ERROR: "+vlanContext+" not found in "+vlanFileString)
            
    
    #Open file and read in list of vlans to a list
    with open(fileNameString) as f:
        for line in f:
            #Parse through file and look for correct context to map
            if context in line:
                if "transparent" in previousLine:#parsing for a bridged firewall, which is configured differently
                    lineList = line.split()#dissect line into a list for easier parsing  
                    hostname = lineList[NAME_INDEX]
                    insideVlanData = [None,None,None] #pre-set a special container for the "inside" interface
                    
                    #The "main loop" of the function, since we found the context we needed
                    while "passwd" not in line: #loop until we reach the end of the part of the file that we need
                        line = next(f)
                        
                        if "interface" in line:
                            lineList = line.split()
                            
                            if "inside" in lineList:
                                interfaceName = lineList[NAME_INDEX]
                                insideVlanData[0] = interfaceName #set the "inside" object we had before to the proper interface name
                                if insideVlanData[0] != None and insideVlanData[1] != None:
                                    vlans.append(insideVlanData) #special object has been filled, so add it to the list
                                
                            if "outside" in lineList:
                                interfaceName = lineList[NAME_INDEX]
                                ipNetwork = "N/A"#no IP associated with the outside IP network in a bridged firewall
                                for v in vlanDataList: #Get respective vlan number to add to vlanData
                                    if "outside" in v:
                                        splitString = v.split()
                                        vlanDataInfo = splitString[VLAN_NAME_INDEX]
                                vlanData = [interfaceName,ipNetwork, vlanDataInfo]
                                vlans.append(vlanData)
                                
                            if "BVI1" in lineList:
                                #note that the interface name is not written down for this interface, because this interface contains the IP for the "inside" interface
                                
                                while "ip address" not in line:
                                    line = next(f)#skip to the IP address of the interface
                                
                                IPLineList = line.split() 
                                ipNetwork = ipNetworkFromMask(IPLineList[VLAN_IP_INDEX],IPLineList[VLAN_MASK_INDEX])#create an IPv4Network object that can be read as a cidrIP
                                insideVlanData[1] = ipNetwork #set the "inside" object we had before to the proper IP value
                                for v in vlanDataList: #Get respective vlan number to add to vlanData
                                    if "inside" in v:
                                        splitString = v.split()
                                        insideVlanData[2] = splitString[VLAN_NAME_INDEX]
                                if insideVlanData[0] != None and insideVlanData[1] != None:
                                    vlans.append(insideVlanData) #special object has been filled, so add it to the list

                    
                    break #reached end of the part of the file that matters to us; ignore the rest of the file and kill the for loop
                    
                else: #not a bridged connection
                    lineList = line.split()#dissect line into a list for easier parsing  
                    hostname = lineList[NAME_INDEX]
                    
                    #The "main loop" of the function, since we found the context we needed
                    while "passwd" not in line:
                        line = next(f)
                        
                        if "interface" in line:
                            lineList = line.split()
                            interfaceName = lineList[NAME_INDEX] #write down the interface name
                            while "ip address" not in line:
                                line = next(f) #jump to the IP address of the interface
                                
                            lineList = line.split()
                            ipNetwork = ipNetworkFromMask(lineList[VLAN_IP_INDEX],lineList[VLAN_MASK_INDEX])#create an IPv4Network object that can be read as a cidrIP
                            for v in vlanDataList: #Get respective vlan number to add to vlanData
                                if interfaceName in v:
                                    splitString = v.split()
                                    vlanDataInfo = splitString[VLAN_NAME_INDEX]
                            vlanData = [interfaceName,ipNetwork,vlanDataInfo]
                            vlans.append(vlanData)
                    
                    break #reached end of the part of the file that matters to us; ignore the rest of the file and kill the for loop
            
            previousLine = line#keep track of previous line in case of bridged networks
        return (hostname,vlans)

def readCommandlineArguments():
    #Runs through the list of command line arguments
    i=1#start at 1, since the first argument is the script call
    argList = [] #list of all commandline arguments (separated by spaces)
    while i < len(sys.argv):
        argList.append(sys.argv[i].strip()) #append the argument to the list (strip any trailing whitespace)
        i += 1
    return argList
#------------------------------------------------------------------------------------------------------

#Process arguments from user with CONFIG FILE NAME and DMZ's to map
contexts = [] #list to hold dmzs passed in the command line
parser = argparse.ArgumentParser(
    description = 'A python script that visually maps network configurations automatically.',
    epilog = 'example: python NetworkMap.py -f contexts.txt -v sys-level.txt  -d vlan1 vlan2 vlan3')
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument("-f", "--file", nargs="+", help="Name of configuration file", required=True)
parser.add_argument("-v", "--vlan", nargs="+", help="Name of file with vlan data", required=False)
requiredNamed.add_argument("-d", "--dmz", nargs="+", help="Name of DMZ in configuration file", required=True)
args = parser.parse_args()
if args.file:
    for f in args.file:
        fileName = openFile(f)
        
if args.vlan:
    for v in args.vlan:
        vlanFile = openFile(v)
else:
    vlanFile = None
    
if args.dmz:
    for c in args.dmz:
        contexts.append(c)

#Create png for each dmz listed in context
for item in contexts:
    print("Reading file and compiling VLAN data for " +item+ "...")

    hostname,vlans = readConfigFile(fileName, vlanFile, item)
    
    #Check to see if hostname or vlans is NULL. If it is, an invalid dmz name was provided
    if len(hostname)>0 and len(vlans)>0:
        hostname = "{0}\n".format(hostname) #formatting!

        print("Parsing VLAN data for " +item+ "...")

        #static variables used when reading parsed vlan data and compiling the graph information
        VLAN_DATA_NAME = 0
        VLAN_DATA_IP_NETWORK = 1
        VLAN_DATA_INFO = 2

        graphData = []
        maxLabelStringLength = -1
        
        for vlan in vlans:
            #find the longest string length in the VLANs
            if len(vlan[VLAN_DATA_NAME]) > maxLabelStringLength:
                maxLabelStringLength = len(vlan[VLAN_DATA_NAME])
            if len(str(vlan[VLAN_DATA_IP_NETWORK])) > maxLabelStringLength:
                maxLabelStringLength = len(str(vlan[VLAN_DATA_IP_NETWORK]))
            
            dataTuple = (hostname,"\n\n\n{0}\n{1}\n{2}".format(vlan[VLAN_DATA_NAME],str(vlan[VLAN_DATA_IP_NETWORK]),vlan[VLAN_DATA_INFO]))#build the tuple
            graphData.append(dataTuple)#add the tuple to the graph
        
            maxLabelPixelLength = maxLabelStringLength*16 #get the pixel space required for the longest string (each character requires approximately 16 pixels)
            maxTotalPixelLength = maxLabelPixelLength*len(vlans) #get the maximum number of pixels required (the label with the most amount of pixels times the number of lables)
            maxInchWidth = maxTotalPixelLength/80 #80 pixels per inch, so convert the total number of pixels required to inches

        print("Rendering VLAN for " +item+ "...")
        
        graph=nx.Graph()
        graph.add_edges_from(graphData)
        pos = hierarchy_pos(graph,hostname)
        plt.figure(figsize=(maxInchWidth,6)) #size of the image
        nx.draw(graph, pos=pos, with_labels=True, node_shape='s', node_size=1) #, node_size=[len(v) * 300 for v in graph.nodes()]
        plt.savefig(item+".png")
        plt.clf()
        print("Image saved to script directory\n\n")
        #plt.show()
    else:
        print("ERROR: "+item+" IS AN INVALID DMZ NAME\n\n")
