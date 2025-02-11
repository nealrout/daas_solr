# daas_solr

## Project

Refrence of DaaS Project - https://github.com/nealrout/daas_docs

## Description
Project to hold common components that will be used by other projects.  

## Table of Contents
- [Requirements](#requirements)
- [Usage](#usage)
- [Features](#features)
- [Miscellaneous](#miscellaneous)
- [Contact](#contact)

## Requirements
### [Zookeeper](https://zookeeper.apache.org/) ### 

### [SOLR 9.x](https://solr.apache.org/downloads.html) ### 

## Usage
__Start zookeeper:__  
zKServer.cmd 

__Start SOLR:__  
solr start -c -z localhost:2181

__Delete Collections:__  
solr delete -Duser=<UPDATEME> -Dpassword=<UPDATEME> -c facility  
solr delete -c asset  

__Create Collections:__  
solr create -c facility -d D:\src\github\daas_solr\facility  
solr create -c asset -d D:\src\github\daas_solr\asset  

__Cloud:__  

-- REMOVE  
curl --user user:password "http://localhost:8983/solr/admin/collections?action=DELETE&name=facility"  
curl --user user:password "http://localhost:8983/solr/admin/collections?action=DELETE&name=asset"  

-- UPLOAD CONFIGS TO ZOOKEEPER  
solr zk upconfig -n facility -d D:\src\github\daas_solr\facility -z localhost:2181  
solr zk upconfig -n asset -d D:\src\github\daas_solr\asset -z localhost:2181  

-- ADD COLLECTIONS  
curl --user user:password "http://localhost:8983/solr/admin/collections?action=CREATE&name=facility&  numShards=1&replicationFactor=1&collection.configName=facility"  
curl --user user:password "http://localhost:8983/solr/admin/collections?action=CREATE&name=asset&numShards=1&replicationFactor=1&collection.configName=asset"


## Features
-

## Miscellaneous
No additional modules are needed currently.  We are only using the built in logging module.

## Contact
Neal Routson  
nroutson@gmail.com
