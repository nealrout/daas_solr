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
solr delete -c facility  
solr delete -c asset

__Create Collections:__  
solr create -c asset -d D:\src\github\daas_solr\asset  
solr create -c facility -d D:\src\github\daas_solr\facility

__Cloud:__  
solr create -c asset -n asset -d D:\src\github\daas_solr\asset -shards 1 -replicationFactor 1
solr zk upconfig -n asset -d D:\src\github\daas_solr\asset -z localhost:2181

## Features
-

## Miscellaneous
No additional modules are needed currently.  We are only using the built in logging module.

## Contact
Neal Routson  
nroutson@gmail.com
