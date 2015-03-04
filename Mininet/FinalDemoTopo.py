#!/usr/bin/python

__author__ = "Sikandar Khan, Ganapathy Raman"

"""
Mininet topology to connect to the openstack via NAT
through eth0 on the host.

Modified the code to suit our needs
"""
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import lg
from mininet.node import Node
from mininet.topolib import TreeNet
from mininet.log import setLogLevel, info
from mininet.node import Controller,RemoteController

#################################
def startNAT( root, root1, root2, inetIntf='eth0', subnet='100.0/8', subnet1='200.0/8',subnet2='150.0/8'):
    """Start NAT/forwarding between Mininet and external network
    root: node to access iptables from
    inetIntf: interface for internet access
    subnet: Mininet subnet (default 10.0/8)="""

    # Identify the interface connecting to the mininet network
    localIntf =  root.defaultIntf()

    # Flush any currently active rules
    root.cmd( 'iptables -F' )
    root1.cmd( 'iptables -F' )
    root2.cmd( 'iptables -F' )
    root.cmd( 'iptables -t nat -F' )
    root1.cmd( 'iptables -t nat -F' )
    root2.cmd( 'iptables -t nat -F' )


    # Create default entries for unmatched traffic
    root.cmd( 'iptables -P INPUT ACCEPT' )
    root1.cmd( 'iptables -P INPUT ACCEPT' )
    root2.cmd( 'iptables -P INPUT ACCEPT' )
    root.cmd( 'iptables -P OUTPUT ACCEPT' )
    root1.cmd( 'iptables -P OUTPUT ACCEPT' )
    root2.cmd( 'iptables -P OUTPUT ACCEPT' )

#    root.cmd( 'iptables -P FORWARD DROP' )
#    root1.cmd( 'iptables -P FORWARD DROP' )

    # Configure NAT for root
    root.cmd( 'iptables -I FORWARD -i', localIntf, '-d', subnet, '-j DROP' )
    root.cmd( 'iptables -A FORWARD -i', localIntf, '-s', subnet, '-j ACCEPT' )
    root.cmd( 'iptables -A FORWARD -i', inetIntf, '-d', subnet, '-j ACCEPT' )
    root.cmd( 'iptables -t nat -A POSTROUTING -o ', inetIntf, '-j MASQUERADE' )
    # Configure NAT for root1
    root1.cmd( 'iptables -I FORWARD -i', localIntf, '-d', subnet1, '-j DROP' )
    root1.cmd( 'iptables -A FORWARD -i', localIntf, '-s', subnet1, '-j ACCEPT' )
    root1.cmd( 'iptables -A FORWARD -i', inetIntf, '-d', subnet1, '-j ACCEPT' )
    root1.cmd( 'iptables -t nat -A POSTROUTING -o ', inetIntf, '-j MASQUERADE' )
    # Configure NAT for root2
    root2.cmd( 'iptables -I FORWARD -i', localIntf, '-d', subnet2, '-j DROP' )
    root2.cmd( 'iptables -A FORWARD -i', localIntf, '-s', subnet2, '-j ACCEPT' )
    root2.cmd( 'iptables -A FORWARD -i', inetIntf, '-d', subnet2, '-j ACCEPT' )
    root2.cmd( 'iptables -t nat -A POSTROUTING -o ', inetIntf, '-j MASQUERADE' )


    # Instruct the kernel to perform forwarding
    root.cmd( 'sysctl net.ipv4.ip_forward=1' )
    root1.cmd( 'sysctl net.ipv4.ip_forward=1' )
    root2.cmd( 'sysctl net.ipv4.ip_forward=1' )


def stopNAT( root, root1 ):
    """Stop NAT/forwarding between Mininet and external network"""
    # Flush any currently active rules in root
    root.cmd( 'iptables -F' )
    root.cmd( 'iptables -t nat -F' )
    root1.cmd( 'iptables -F' )
    root1.cmd( 'iptables -t nat -F' )
    root2.cmd( 'iptables -F' )
    root2.cmd( 'iptables -t nat -F' )
	
    # Instruct the kernel to stop forwarding
    #root.cmd( 'sysctl net.ipv4.ip_forward=0' )

def fixNetworkManager( root, intf ):
    """Prevent network-manager from messing with our interface,
       by specifying manual configuration in /etc/network/interfaces
       root: a node in the root namespace (for running commands)
       intf: interface name"""
    cfile = '/etc/network/interfaces'
    line = '\niface %s inet manual\n' % intf
    config = open( cfile ).read()
    if line not in config:
        print '*** Adding', line.strip(), 'to', cfile
        with open( cfile, 'a' ) as f:
            f.write( line )
        # Probably need to restart network-manager to be safe -
        # hopefully this won't disconnect you
        root.cmd( 'service network-manager restart' )

def connectToInternet( network, switch='s1', switch1='s2',switch2='s0' , rootip='100.254', subnet='100.0/8', rootip1='200.254', subnet1='200.0/8',rootip2='150.254', subnet2='150.0/8'):
    """Connect the network to the internet
       switch: switch to connect to root namespace
       rootip: address for interface in root namespace
       subnet: Mininet subnet"""
    switch  = network.get( switch )
    switch1 = network.get( switch1 )
    switch2 = network.get( switch2 )

    prefixLen = subnet.split( '/' )[ 1 ]
    prefixLen1 = subnet1.split( '/' )[ 1 ]
    prefixLen2 = subnet2.split( '/' )[ 1 ]
    # Create a node in root namespace
    root = Node( 'root', inNamespace=False )
    root1 = Node( 'root1', inNamespace=False )
    root2 = Node( 'root2', inNamespace=False )
    # Prevent network-manager from interfering with our interface
    fixNetworkManager( root, 'root-eth0' )
    fixNetworkManager( root1, 'root1-eth0' )
    fixNetworkManager( root2, 'root2-eth0' )
 

    # Create lnk between root NS and switch
    link = network.addLink( root, switch )
    link1 = network.addLink( root1, switch1 )
    link2 = network.addLink( root2, switch2 )
    link.intf1.setIP( rootip, prefixLen )
    link1.intf1.setIP( rootip1, prefixLen1 )
    link2.intf1.setIP( rootip2, prefixLen2 )


    # Start network that now includes link to root namespace
    network.start()

    # Start NAT and establish forwarding
    startNAT( root , root1 , root2 )

    # Establish routes from end hosts
    for host in network.hosts:
        host.cmd( 'ip route flush root 0/0' )

    info( '*** Adding Default Route\n')
    h1.cmd( 'route add -net', subnet2, 'dev', h1.defaultIntf() )
    h1.cmd( 'route add default gw', rootip2 )
    h2.cmd( 'route add -net', subnet2, 'dev', h2.defaultIntf() )
    h2.cmd( 'route add default gw', rootip2 )
    h3.cmd( 'route add -net', subnet2, 'dev', h3.defaultIntf() )
    h3.cmd( 'route add default gw', rootip2 )
    h4.cmd( 'route add -net', subnet2, 'dev', h4.defaultIntf() )
    h4.cmd( 'route add default gw', rootip2 )
    h5.cmd( 'route add -net', subnet, 'dev', h5.defaultIntf() )
    h5.cmd( 'route add default gw', rootip )
    h6.cmd( 'route add -net', subnet, 'dev', h6.defaultIntf() )
    h6.cmd( 'route add default gw', rootip )
    h7.cmd( 'route add -net', subnet, 'dev', h7.defaultIntf() )
    h7.cmd( 'route add default gw', rootip )
    h8.cmd( 'route add -net', subnet, 'dev', h8.defaultIntf() )
    h8.cmd( 'route add default gw', rootip )	
    h9.cmd( 'route add -net', subnet1, 'dev', h9.defaultIntf() )
    h9.cmd( 'route add default gw', rootip1 )
    h10.cmd( 'route add -net', subnet1, 'dev', h10.defaultIntf() )
    h10.cmd( 'route add default gw', rootip1 )
    h11.cmd( 'route add -net', subnet1, 'dev', h11.defaultIntf() )
    h11.cmd( 'route add default gw', rootip1 )
    h12.cmd( 'route add -net', subnet1, 'dev', h12.defaultIntf() )
    h12.cmd( 'route add default gw', rootip1 )

    return root, root1, root2

if __name__ == '__main__':
    lg.setLogLevel( 'info' )
    net = Mininet( topo=None, build=False)

    info( '*** Adding controller\n' )
    net.addController(name='c0', controller=RemoteController, ip='172.16.201.129')
    info( '*** Add switches\n')
    s0 = net.addSwitch('s0')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
    s6 = net.addSwitch('s6')

    info( '*** Add hosts\n')
	#For switch0 "The pool of servers" 
    h1 = net.addHost('h1', ip='150.0.0.1')
    h2 = net.addHost('h2', ip='150.0.0.2')
    h3 = net.addHost('h3', ip='150.0.0.129')
    h4 = net.addHost('h4', ip='150.0.0.130')
	
	#For 100 subnet 
    h5 = net.addHost('h5', ip='100.0.0.1')
    h6 = net.addHost('h6', ip='100.0.0.2')
    h7 = net.addHost('h7', ip='100.0.0.3')
    h8 = net.addHost('h8', ip='100.0.0.4')
	
	#For 200 subnet
    h9  = net.addHost('h9',  ip='200.0.0.1')
    h10 = net.addHost('h10', ip='200.0.0.2')
    h11 = net.addHost('h11', ip='200.0.0.3')
    h12 = net.addHost('h12', ip='200.0.0.4')

    info( '*** Add Host-Switch links\n')
   #server pool in core switch 
    net.addLink(h1, s0)
    net.addLink(h2, s0)
    net.addLink(h3, s0)
    net.addLink(h4, s0)
   #hosts in the access network
    net.addLink(h5, s3)
    net.addLink(h6, s3)
    net.addLink(h7, s4)
    net.addLink(h8, s4)
    net.addLink(h9, s5)
    net.addLink(h10, s5)
    net.addLink(h11, s6)
    net.addLink(h12, s6)

    info( '*** Add Switch-Switch links\n')
    
    net.addLink(s0, s1)
    net.addLink(s0, s2)
	#primary links
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s1, s4)
	#secondary links
    net.addLink(s1, s5)
    net.addLink(s2, s4)
    net.addLink(s3, s4)
    net.addLink(s5, s6)
	#primary links
    net.addLink(s2, s5)
    net.addLink(s2, s6)
	

    # Configure and start NATted connectivity
    rootnode, rootnode1, rootnode2 = connectToInternet( net )
    info( '*** Hosts are running and should have internet connectivity' )
    info( '*** Type \'exit\' or control-D to shut down network' )
    CLI( net )
    # Shut down NAT
    stopNAT( rootnode, rootnode1, rootnode2)
    net.stop()

