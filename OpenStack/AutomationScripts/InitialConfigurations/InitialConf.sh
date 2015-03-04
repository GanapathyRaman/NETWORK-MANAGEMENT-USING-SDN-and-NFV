#Initial Configurations

#@author: Sikandar Khan

sudo ip link set mtu 300 dev br-ex
sudo ip link set mtu 1454 dev eth0
sudo ip link set mtu 1454 dev wlan0

echo "Openrc admin admin"
. ./openrc admin admin

echo "Creating tenant CompanyA"
keystone tenant-create --name CompanyA
keystone user-create --name CompanyA --tenant CompanyA --pass openstack 

echo "Creating tenant CompanyB"
keystone tenant-create --name CompanyB 
keystone user-create --name CompanyB --tenant CompanyB --pass openstack 

echo "Creating tenant RemoteA"
keystone tenant-create --name RemoteA 
keystone user-create --name RemoteA --tenant RemoteA --pass openstack 

echo "Assigning Admin Roles to CompanyA"
keystone user-role-add --user $(keystone user-list | grep '\sCompanyA' | awk '{print $2}') --role $(keystone role-list | grep 'admin' | awk '{print $2}') --tenant_id $(keystone tenant-list | grep '\sCompanyA' | awk '{print $2}')

echo "Assigning Admin Roles to CompanyB"
keystone user-role-add --user $(keystone user-list | grep '\sCompanyB' | awk '{print $2}') --role $(keystone role-list | grep 'admin' | awk '{print $2}') --tenant_id $(keystone tenant-list | grep '\sCompanyB' | awk '{print $2}')

echo "Assigning Admin Roles to RemoteA"
keystone user-role-add --user $(keystone user-list | grep '\sRemoteA' | awk '{print $2}') --role $(keystone role-list | grep 'admin' | awk '{print $2}') --tenant_id $(keystone tenant-list | grep '\sRemoteA' | awk '{print $2}')

echo "Uploading image"
glance image-create --name TinyCore --disk-format iso --container-format bare --is-public True --file /home/ganapathy/Desktop/TinyCore-current.iso

echo "Creating Host aggregate Sak"
nova aggregate-create sak sak

echo "Adding Host to aggregate Sak"
nova aggregate-add-host sak sak
