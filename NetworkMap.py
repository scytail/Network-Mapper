import networkx as nx
import matplotlib.pyplot as plt
import ipaddress as ipaddr

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

def readConfigFile(fileNameString):
    '''
       Reads a given firewall configuration file for its VLAN configuations
    '''
    #static variables used when reading the individual vlan data lists
    CONFIG_TAG_INDEX = 0
    NAME_INDEX = 1
    VLAN_IP_INDEX = 2
    VLAN_MASK_INDEX = 3
    
    #Open file and read in list of vlans to a list
    vlans = []
    with open(fileNameString) as f:
      for line in f:
        if line ==  "!\n":#found relevant data
          print(line)
          #feed the file through to the proper point
          line = next(f)
          lineList = line.split()#dissect line into a list for easier parsing
          if lineList[CONFIG_TAG_INDEX] == "hostname":
            #TODO: Parse the hostname
            pass
          elif lineList[CONFIG_TAG_INDEX] == "interface":
            name = lineList[NAME_INDEX]
            #feed the file through to the proper point
            while "ip" not in line:
              line = next(f)     
            lineList = line.split()  
            ipNetwork = ipNetworkFromMask(lineList[VLAN_IP_INDEX],lineList[VLAN_MASK_INDEX])#create an IPv4Network object that can be read as a cirIP
            vlanData = [name,ipNetwork]#re-create the list with better parsing
            vlans.append(vlanData)
        else:
            line = next(f) #don't need to keep reading the file if we already found what we want, so break the for loop.
    return vlans 
#------------------------------------------------------------------------------------------------------

print("Reading file and compiling VLAN data...")

vlans = readConfigFile("FST-E-WEB-DMZ-Config.txt")#FIXME: HARD-CODED

print("Parsing VLAN data...")

#static variables used when reading parsed vlan data and compiling the graph information
FIREWALL_NAME = "FST-E-WEB-DMZ"
VLAN_DATA_NAME = 0
VLAN_DATA_IP_NETWORK = 1

graphData = []

for vlan in vlans:
    dataTuple = (FIREWALL_NAME,"{0}\n{1}".format(vlan[VLAN_DATA_NAME],str(vlan[VLAN_DATA_IP_NETWORK])))#build the tuple
    graphData.append(dataTuple)#add the tuple to the graph

print("Rendering VLAN data...")

graph=nx.Graph()
graph.add_edges_from(graphData)
pos = hierarchy_pos(graph,FIREWALL_NAME)
nx.draw(graph, pos=pos, with_labels=True, node_shape='s', node_size=1) #, node_size=[len(v) * 300 for v in graph.nodes()]
plt.show()
