# Team Hyper-Accelerated Dragon's Data Engineering Project

## Overview 
A data application that extracts, transforms, and loads data from an operational database into a data lake and warehouse hosted in AWS

See: https://github.com/northcoders/de-project-specification/raw/main/mvp.png 

## Description
Our data application is triggered by an AWS EventBridge scheduler to continually extract data from the ToteSys database and archive it in a data lake (an ingestion S3 bucket on AWS).
The ingested data is transformed according to a predefined star schema and stored in a second processed S3 bucket in Parquet format.
A third Python application makes the data available in fact and dimension tables in a remodelled PSQL data warehouse (hosted on RDS).
Progress throughout the data pipeine is logged on Cloudwatch, with email alerts triggered in the event of failure.


The Python code has been developed using test-driven development, with security vulnerabilities checked using safety and bandit packages.


## Installation
The project will be deployed automatically using infrastucture-as-code (Terraform) and CI/CD techniques (GitHub Actions)
For deployment from a local machine, please run ` pip install -r requirements.txt `

## Authors and acknowledgment
Ash Devereux\
Charlotte Handford\
Cris Jarvis\
Gonçalo Cid\
Oleh Fylypiv\
Zabihullah Habibi

An additional thank you to Mick Fay for his insight and guidance throughout