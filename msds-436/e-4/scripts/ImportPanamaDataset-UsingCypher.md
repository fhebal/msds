#***********************************************
# File: ImportPanamaDataset-UsingCypher.txt
# Desc: Loading data into Graph database
# Auth: Shreenidhi Bharadwaj
# Date: 10/15/2019
# ALL RIGHTS RESERVED | DO NOT DISTRIBUTE
#************************************************/

# Import the following data into Neo4J
# panama_papers.nodes.address_fixed.csv  { nodes } 
# panama_papers.nodes.intermediary.csv   { nodes }
# panama_papers.nodes.entity.csv         { nodes }
# panama_papers.nodes.officer_fixed.csv  { nodes }
# panama_papers.edges.intermediary_of.csv  		{ relationships }
# panama_papers.edges.officer_of.entities.csv	{ relationships }
# panama_papers.edges.officer_of.others.csv		{ relationships }
# panama_papers.edges.registered_address.entity.csv  { relationships }
# panama_papers.edges.registered_address.officer.csv { relationships }

# login to https://<EC2_PUBLIC_DNS>:7473/browser/ with credentials (user : neo4j)

# delete all data
match (n)
with n limit 10000
DETACH DELETE n;

# Create a preauthenticated URL for S3 Object
aws s3 presign s3://aws-big-data-project/panama/panama_papers.nodes.address_fixed.csv

# Use the output from the previous command and replace it with the URL listed below within quotes.
USING PERIODIC COMMIT 100 LOAD CSV WITH HEADERS FROM 'https://aws-big-data-project.s3.amazonaws.com/panama/panama_papers.nodes.address_fixed.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Expires=3600&X-Amz-Credential=AKIAW32454U5CXMHYQ5S%2F20191013%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-SignedHeaders=host&X-Amz-Date=20191013T192634Z&X-Amz-Signature=07e1284ef5909ac4e40530b6c202664678b1328433316cddb3f04c6056f39912' AS line
CREATE (:Addresses { node_id: toInteger(line.node_id),
                     name: line.name,
                     address: line.address,
                     country_codes: line.country_codes,
                     countries: line.countries,
                     sourceID: line.sourceID,
                     valid_until: line.valid_until,
                     note: line.note })

aws s3 presign s3://aws-big-data-project/panama/panama_papers.nodes.intermediary.csv

https://aws-big-data-project.s3.amazonaws.com/panama/panama_papers.nodes.intermediary.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Expires=3600&X-Amz-Credential=AKIAW32454U5AVFM645S%2F20190909%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-SignedHeaders=host&X-Amz-Date=20190909T231505Z&X-Amz-Signature=d573ce9f59551248884a49c39eb77d30bc3f18db4cb01a77472079639dc0c929

USING PERIODIC COMMIT 100 LOAD CSV WITH HEADERS FROM 'https://aws-big-data-project.s3.amazonaws.com/panama/panama_papers.nodes.intermediary.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Expires=3600&X-Amz-Credential=AKIAW32454U5AVFM645S%2F20190909%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-SignedHeaders=host&X-Amz-Date=20190909T231505Z&X-Amz-Signature=d573ce9f59551248884a49c39eb77d30bc3f18db4cb01a77472079639dc0c929' AS line
CREATE (:Intermediaries { node_id: toInteger(line.node_id),
                          name: line.name,
                          country_codes: line.country_codes,
                          countries: line.countries,
                          status: line.status,
                          sourceID: line.sourceID,
                          valid_until: line.valid_until,
                          note: line.note })


aws s3 presign s3://aws-big-data-project/panama/panama_papers.nodes.entity.csv

https://aws-big-data-project.s3.amazonaws.com/panama/panama_papers.nodes.entity.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Expires=3600&X-Amz-Credential=AKIAW32454U5AVFM645S%2F20190909%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-SignedHeaders=host&X-Amz-Date=20190909T232020Z&X-Amz-Signature=604a7da2a4c416d36b7cbae825fb7c9852209db089cbd8cc2d243fd619c3d948

USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'https://aws-big-data-project.s3.amazonaws.com/panama/panama_papers.nodes.entity.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Expires=3600&X-Amz-Credential=AKIAW32454U5AVFM645S%2F20190909%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-SignedHeaders=host&X-Amz-Date=20190909T232020Z&X-Amz-Signature=604a7da2a4c416d36b7cbae825fb7c9852209db089cbd8cc2d243fd619c3d948' AS line
CREATE (:Entities { node_id: toInteger(line.node_id),
                    name: line.name,
                    jurisdiction: line.jurisdiction,
                    jurisdiction_description: line.jurisdiction_description,
                    country_codes: line.country_codes,
                    countries: line.countries,
                    incorporation_date: line.incorporation_date,
                    inactivation_date: line.inactivation_date,
                    struck_off_date: line.struck_off_date,
                    closed_date: line.closed_date,
                    ibcRUC: toInteger(line.ibcRUC) ,
                    status: line.status,
                    company_type: line.company_type,
                    service_provider: line.service_provider,
                    sourceID: line.sourceID,
                    valid_until: line.valid_until,
                    note: line.note })


aws s3 presign s3://aws-big-data-project/panama/panama_papers.nodes.officer_fixed.csv

https://aws-big-data-project.s3.amazonaws.com/panama/panama_papers.nodes.officer_fixed.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Expires=3600&X-Amz-Credential=AKIAW32454U5AVFM645S%2F20190909%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-SignedHeaders=host&X-Amz-Date=20190909T232228Z&X-Amz-Signature=eed40bbe4a725372d1876709aa6f63bbbf59f23f3fd9c72c160c1fabb3c8998a

USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'https://aws-big-data-project.s3.amazonaws.com/panama/panama_papers.nodes.officer_fixed.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Expires=3600&X-Amz-Credential=AKIAW32454U5AVFM645S%2F20190909%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-SignedHeaders=host&X-Amz-Date=20190909T232228Z&X-Amz-Signature=eed40bbe4a725372d1876709aa6f63bbbf59f23f3fd9c72c160c1fabb3c8998a' AS line
CREATE (:Officers { node_id: toInteger(line.node_id),
                    name: line.name,
                    country_codes: line.country_codes,
                    countries: line.countries,
                    sourceID: line.sourceID,
                    valid_until: line.valid_until,
                    note: line.note })

# Import from local machine

CREATE INDEX ON :Intermediaries(node_id)
CREATE INDEX ON :Entities(node_id)
CREATE INDEX ON :Officers(node_id)
CREATE INDEX ON :Addresses(node_id)


USING PERIODIC COMMIT 100 LOAD CSV WITH HEADERS FROM 'file:///panama_papers.edges.intermediary_of.csv' AS line
MATCH (n1:Intermediaries { node_id: toInteger(line.START_ID)}),(n2:Entities { node_id: toInteger(line.END_ID)})
USING INDEX n1:Intermediaries(node_id)
USING INDEX n2:Entities(node_id)
CREATE (n1)-[:intermediary_of { link: line.link,
                          start_date: line.start_date,
                          end_date: line.end_date,
                          sourceID: line.sourceID,
                          valid_until: line.valid_until
                        }
            ]->(n2)


USING PERIODIC COMMIT 100 LOAD CSV WITH HEADERS FROM 'file:///panama_papers.edges.officer_of.entities.csv' AS line
MATCH (n1:Officers { node_id: toInteger(line.START_ID)}),(n2:Entities { node_id: toInteger(line.END_ID)})
USING INDEX n1:Officers(node_id)
USING INDEX n2:Entities(node_id)
CREATE (n1)-[:officer_of { link: line.link,
                          start_date: line.start_date,
                          end_date: line.end_date,
                          sourceID: line.sourceID,
                          valid_until: line.valid_until
                        }
            ]->(n2)


USING PERIODIC COMMIT 1 LOAD CSV WITH HEADERS FROM 'file:///panama_papers.edges.officer_of.others.csv' AS line
MATCH (n1:Officers { node_id: toInteger(line.START_ID)}),(n2 { node_id: toInteger(line.END_ID)})
USING INDEX n1:Officers(node_id)
CREATE (n1)-[:officer_of { link: line.link,
                          start_date: line.start_date,
                          end_date: line.end_date,
                          sourceID: line.sourceID,
                          valid_until: line.valid_until
                        }
            ]->(n2)


USING PERIODIC COMMIT 100 LOAD CSV WITH HEADERS FROM 'file:///panama_papers.edges.registered_address.entity.csv' AS line
MATCH (n1:Entities { node_id: toInteger(line.START_ID)}),(n2:Addresses { node_id: toInteger(line.END_ID)})
USING INDEX n1:Entities(node_id)
USING INDEX n2:Addresses(node_id)
CREATE (n1)-[:registered_address { link: line.link,
                          start_date: line.start_date,
                          end_date: line.end_date,
                          sourceID: line.sourceID,
                          valid_until: line.valid_until
                        }
            ]->(n2)


USING PERIODIC COMMIT 100 LOAD CSV WITH HEADERS FROM 'file:///panama_papers.edges.registered_address.officer.csv' AS line
MATCH (n1:Officers { node_id: toInteger(line.START_ID)}),(n2:Addresses { node_id: toInteger(line.END_ID)})
USING INDEX n1:Officers(node_id)
USING INDEX n2:Addresses(node_id)
CREATE (n1)-[:registered_address { link: line.link,
                          start_date: line.start_date,
                          end_date: line.end_date,
                          sourceID: line.sourceID,
                          valid_until: line.valid_until
                        }
            ]->(n2)

# VERIFICATION : Once the import is done check counts
# Total node count - 559600
# Total edge count - 674102

# Queries 

