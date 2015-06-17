# bagcat

bagcat is a small command line utility for managing a collection of
[BagIt](https://en.wikipedia/wiki/BagIt) packages in Amazon S3. 

This is alpha software still under development :-) Your
[feedback](https://github.com/umd-mith/bagcat/issues) is welcome!

```

% bagcat config
aws_access_key_id: skljfs
aws_secret_access_key: sldkfjslkjf
bucket: s3://my-bags

% bagcat list

E967BD40-FC32-477F-9E5E-92C61B22807A (1.8GB)
Payload-Oxum: 1972372624.2
Contact-Name: Ed Summers
License: UMD Only
Contact-Email: ehs@pobox.com
Bagging-Date: 2015-05-20
External-Description: This is a dataset of tweets collected during April 15, 2015 and May 13, 2015
 that mention the hashtag #FreddieGray. One portion of the tweets was collected
 from Twitter's search API and the other set is from the streaming API.
 Both sets were collected using the twarc tool. The total dataset includes
 2,983,934 tweets. Freddie Gray was an African-American man who was arrested
 by the Baltimore Police Department on April 12, 2015, and died on April 19,
 2015 due to an injury to his spinal cord that was believed to be the result
 of his treatment by the police.
Bag-Software-Agent: bagit.py <http://github.com/libraryofcongress/bagit-python>
Identifier: E967BD40-FC32-477F-9E5E-92C61B22807A

fe28a093-d3f4-42d7-83ba-f5ba1b1cc765 (8.4GB)
Payload-Oxum: 8975261027.15
Contact-Name: Ed Summers
License: UMD only
Contact-Email: ehs@pobox.com
Bagging-Date: 2014-08-30
External-Description: A collection of 13,238,863 tweets mentioning 'ferguson' from 2014-08-10 22:44:43 to 2014-08-27 15:15:50. The tweets were collected
 from the Twitter Search API using the twarc utility. They were subsequently
 run through deduplication process and also a URL unshortening process that
 added the unshortened_url key to url entities in the original json data.
Identifier: fe28a093-d3f4-42d7-83ba-f5ba1b1cc765
Source-Organization: Twitter

...
```
