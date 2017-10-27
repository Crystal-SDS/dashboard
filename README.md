#  Crystal Dashboard

Horizon Plugin for Crystal

Crystal Dashboard is an extension for OpenStack Dashboard that provides a UI
for Crystal. With crystal dashboard, a user is able to easily write the
policies and rules for governance of cloud.

## Requirements

* An [OpenStack Horizon](https://github.com/openstack/horizon) installation.
* A [Crystal controller](https://github.com/Crystal-SDS/controller) deployment.
* An [Elastic Stack](https://www.elastic.co/) (Elasticsearch, Logstash, Kibana) installation.

## Installation

To install the Crystal dashboard, clone the repository and run the installation command in the root directory:
```sh
git clone https://github.com/Crystal-SDS/dashboard
cd dashboard
sudo python setup.py install
```

After that, it is necessary to configure the OpenStack Horizon installation in order to enable the Crystal Dashboard.
1. Copy the main Crystal Dashboard entrypoint to the enabled folder of the Horizon installation:

```sh
cp dashboard/crystal_dashboard/enabled/_50_sdscontroller.py /usr/share/openstack-dashboard/openstack_dashboard/enabled/
```
2. Copy the Crystal Dashboard configuration to the Horizon configuration:
```sh
cat dashboard/crystal_dashboard/local/local_settings.py >> /etc/openstack-dashboard/local_settings.py
```

## Overview
![Storage Nodes](http://crystal-sds.org/wp-content/uploads/2016/05/nodes.png)

![Storlet Filters](http://crystal-sds.org/wp-content/uploads/2016/05/storlet_filters.png)

![SWift Monitoring](http://crystal-sds.org/wp-content/uploads/2016/05/monitoring.png)



