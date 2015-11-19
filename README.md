# MyTardis Client
Command Line Interface and Python classes for interacting with MyTardis's API.

Install:
```
$ mkdir ~/virtualenvs/mytardisclient
$ source ~/virtualenvs/mytardisclient/bin/activate
(mytardisclient) $ pip install -e git+https://github.com/wettenhj/mytardisclient.git#egg=mytardisclient
```
```
(mytardisclient) $ which mytardis
/Users/wettenhj/virtualenvs/mytardisclient/bin/mytardis
```

The MyTardis URL, username and API key should be stored in ~/.mytardisclient.cfg:

```
(mytardisclient) $ cat ~/.mytardisclient.cfg 
[mytardisclient]
mytardis_url = http://mytardisdemo.erc.monash.edu.au
username = demofacility
api_key = 644be179cc6773c30fc471bad61b50c90897146c
```

Let's list the experiments which user "demofacility" has access to:

```
(mytardisclient) $ mytardis experiment list
MyTardis Client v0.0.1
Config: /Users/wettenhj/.mytardisclient.cfg
MyTardis URL: http://mytardisdemo.erc.monash.edu.au
Username: demofacility

Model: Experiment
Query: http://mytardisdemo.erc.monash.edu.au/api/v1/experiment/?format=json
Total Count: 9
Limit: 20
Offset: 0

+----+-----------------------------------------------------------+
| ID |                           Title                           |
+====+===========================================================+
| 15 | A's 2nd Test Instrument - Test User1                      |
+----+-----------------------------------------------------------+
| 12 | exp1                                                      |
+----+-----------------------------------------------------------+
| 17 | Steve's Macbook 12 - Test User1                           |
+----+-----------------------------------------------------------+
| 11 | Beamline - Test User2                                     |
+----+-----------------------------------------------------------+
| 19 | Manually created experiment to test filename length in UI |
+----+-----------------------------------------------------------+
| 13 | A's Test Instrument - Test User1                          |
+----+-----------------------------------------------------------+
| 16 | A's 2nd Test Instrument - Test User2                      |
+----+-----------------------------------------------------------+
| 18 | Steve's Macbook 12 - Test User2                           |
+----+-----------------------------------------------------------+
| 14 | A's Test Instrument - Test User2                          |
+----+-----------------------------------------------------------+
```

Now let's create a new experiment called "James Test Exp 001":

```
(mytardisclient) (mytardisclient) $ mytardis experiment create "James Test Exp 001"
MyTardis Client v0.0.1
Config: /Users/wettenhj/.mytardisclient.cfg
MyTardis URL: http://mytardisdemo.erc.monash.edu.au
Username: demofacility

Model: Experiment

+------------------+--------------------+
| Experiment field |       Value        |
+==================+====================+
| ID               | 20                 |
+------------------+--------------------+
| Title            | James Test Exp 001 |
+------------------+--------------------+
| Description      |                    |
+------------------+--------------------+

Experiment created successfully.
```

Now let's create a dataset.  Note that when we run "mytardis dataset create" without the experiment ID and description arguments, we get a usage message telling us the names of the missing arguments.

```
(mytardisclient) $ mytardis dataset create
usage: mytardis dataset create [-h] experiment_id description
mytardis dataset create: error: too few arguments

(mytardisclient) $ mytardis dataset create 20 "James Test Dataset 001"
MyTardis Client v0.0.1
Config: /Users/wettenhj/.mytardisclient.cfg
MyTardis URL: http://mytardisdemo.erc.monash.edu.au
Username: demofacility

Model: Dataset

+---------------+------------------------+
| Dataset field |         Value          |
+===============+========================+
| ID            | 31                     |
+---------------+------------------------+
| Experiments   | /api/v1/experiment/20/ |
+---------------+------------------------+
| Description   | James Test Dataset 001 |
+---------------+------------------------+
| Instrument    | None                   |
+---------------+------------------------+

Dataset created successfully.
```

Now's let's upload a file ('hello.txt') to the dataset we just created:

```
(mytardisclient) $ mytardis datafile
usage: mytardis datafile [-h] {list,download,upload} ...
mytardis datafile: error: too few arguments

(mytardisclient) $ mytardis datafile upload
usage: mytardis datafile upload [-h] dataset_id file_path
mytardis datafile upload: error: too few arguments

(mytardisclient) $ mytardis datafile upload 31 hello.txt
MyTardis Client v0.0.1
Config: /Users/wettenhj/.mytardisclient.cfg
MyTardis URL: http://mytardisdemo.erc.monash.edu.au
Username: demofacility
Uploaded: hello.txt
```

Now let's reload the dataset's datafile list to see the new datafile record:

```
(mytardisclient) $ mytardis dataset get 31
MyTardis Client v0.0.1
Config: /Users/wettenhj/.mytardisclient.cfg
MyTardis URL: http://mytardisdemo.erc.monash.edu.au
Username: demofacility

Model: Dataset

+---------------+------------------------+
| Dataset field |         Value          |
+===============+========================+
| ID            | 31                     |
+---------------+------------------------+
| Experiments   | /api/v1/experiment/20/ |
+---------------+------------------------+
| Description   | James Test Dataset 001 |
+---------------+------------------------+
| Instrument    | None                   |
+---------------+------------------------+


Model: DataFile
Query: http://mytardisdemo.erc.monash.edu.au/api/v1/dataset_file/?format=json&dataset__id=31
Total Count: 1
Limit: 20
Offset: 0

+-----+---------------------+-----------+------------+----------+-----------+----------------------------------+
| ID  |       Dataset       | Directory |  Filename  | Verified |   Size    |             MD5 Sum              |
+=====+=====================+===========+============+==========+===========+==================================+
|  99 | /api/v1/dataset/31/ |           | hello.txt  | True     |  13 bytes | 9af2f8218b150c351ad802c6f3d66abe |
+-----+---------------------+-----------+------------+----------+-----------+----------------------------------+
```

Note that the file has been verified already.  Now let's determine the file size and MD5 checksum locally and ensure that they match the values recorded in MyTardis:

```
(mytardisclient) $ ls -l hello.txt
-rw-r--r--  1 wettenhj  staff  13 19 Nov 11:23 hello.txt

(mytardisclient) $ md5 hello.txt 
MD5 (hello.txt) = 9af2f8218b150c351ad802c6f3d66abe
```

Now let's delete the local copy of 'hello.txt', and download it from MyTardis:

```
(mytardisclient) $ rm hello.txt 

(mytardisclient) $ mytardis datafile download
usage: mytardis datafile download [-h] datafile_id
mytardis datafile download: error: too few arguments

(mytardisclient) $ mytardis datafile download 99
MyTardis Client v0.0.1
Config: /Users/wettenhj/.mytardisclient.cfg
MyTardis URL: http://mytardisdemo.erc.monash.edu.au
Username: demofacility
Downloaded: hello.txt

(mytardisclient) $ ls -l hello.txt 
-rw-r--r--  1 wettenhj  staff  13 19 Nov 11:33 hello.txt
```
