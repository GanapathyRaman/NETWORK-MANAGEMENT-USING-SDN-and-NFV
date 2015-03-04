#Confguration Specific to RemoteA

#@author: Sikandar Khan

echo "Openrc RemoteA"
. ./openrc RemoteA RemoteA

echo "Launching 40.0.0.0/24 network in RemoteA" 
neutron net-create RemoteAftpNetwork --tenant_id $(keystone tenant-list | grep '\sRemoteA' | awk '{print $2}')
neutron subnet-create RemoteAftpNetwork 40.0.0.0/24 --name RemoteAftpNetwork

echo "Creating routers on RemoteA"
neutron router-create R-RemoteAftpServer

echo "Adding Pubic Gateway for R-RemoteAftpServer public"
neutron router-gateway-set R-RemoteAftpServer public

echo "Attaching interface of R-RemoteAftpServer to network RemoteAftpNetwork"
neutron router-interface-add R-RemoteAftpServer $(neutron subnet-list | grep RemoteAftpNetwork | awk '{print $2}')

echo "Exporting image" 
export IMAGE=TinyCore

echo "Launching instances in RemoteA" 
nova boot --flavor m1.tiny --image $(nova image-list | grep $IMAGE'\s' | awk '{print $2}') --nic net-id=$(neutron net-list | grep RemoteAftpNetwork | awk '{print $2}') RA-FTPserver --availability_zone=sak:sak

#Adding Security Rules
echo "Adding Security Rules for RemoteA"

echo "Adding ICMP Rule for RemoteA"
nova secgroup-add-rule default icmp -1 -1 0.0.0.0/0

echo "Adding TCP Rule for RemoteA"
nova secgroup-add-rule default tcp 1 65535 0.0.0.0/0

#RemoteA VPN Configurations
echo "Adding IKE Policy to RemoteA"
neutron vpn-ikepolicy-create remoteAikepolicy

echo "Adding IPSec Policy to RemoteA"
neutron vpn-ipsecpolicy-create remoteAipsecpolicy

echo "Adding VPN Service RemoteA"
neutron vpn-service-create --name remoteAvpn --description "This VPN is to communicate between Proxy server and intermediate server" R-RemoteAftpServer RemoteAftpNetwork

echo "Adding IPSec Site Connections for RemoteA"
neutron ipsec-site-connection-create --name vpnconnection --vpnservice-id remoteAvpn --ikepolicy-id remoteAikepolicy --ipsecpolicy-id remoteAipsecpolicy --peer-address 180.180.180.4 --peer-id 180.180.180.4 --peer-cidr 30.0.0.0/24 --psk opensesame
