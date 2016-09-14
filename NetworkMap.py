import networkx as nx
import matplotlib.pyplot as plt
import ipaddress as ipaddr

#http://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3
def hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5 ):
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
       `ipaddress` objects also error check for incorrect networks.
    '''
    return ipaddr.ip_network("{0}/{1}".format(addressString,subnetMaskString))
#------------------------------------------------------------------------------------------------------


   
graph=nx.Graph()
graph.add_edges_from([("Firewall-a","b-DMZ\n{0}".format(ipNetworkFromMask("192.168.1.0","255.255.255.0"))),
                  ("Firewall-a","c-VLAN1\n{0}".format(ipNetworkFromMask("192.168.0.0","255.255.0.0"))),
                  ("Firewall-a","d-VLAN2\n{0}".format(ipNetworkFromMask("192.0.0.0","255.0.0.0")))
                ])
pos = hierarchy_pos(graph,"Firewall-a")
nx.draw(graph, pos=pos, with_labels=True)
plt.show()
