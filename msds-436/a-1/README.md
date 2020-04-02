Ferdynand Hebal 2019

## Objective
* Learn about AWS platform, source code control, data ingestion techniques, data storage

## Submissions
* All project artifacts including README.txt & code included in submission and github

### Question 1: {50 points}
* scraper collects links to pages containing data necessary for scraping and outputs links to boxer_links.txt
* scraper visits urls in boxer_links.txt and collect data from html. outputs to pipe_delimited text file boxer_career.txt

### Question 2: {10 points}
* Raw data read into pandas dataframe and loaded to S3 as pipe delimited text file

### Question 3: {20 points}
* S3 bucket was created in the AWS console using credentials provided by AWS Education session

### Question 4: {20 points}
* I used sqlalchemy to connect to my AWS PostgreSQL instance created a data model with a query and pushed the scraped data from s3 using pandas
* 4 SQL queries are included making calls directl to the postgresql instance
