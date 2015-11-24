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

Configuration:

```
(mytardisclient) $ mytardis config
MyTardis URL? http://mytardisdemo.erc.monash.edu.au
MyTardis Username? demofacility
MyTardis API key? 644be179cc6773c30fc471bad61b50c90897146c

Wrote settings to /Users/wettenhj/.config/mytardisclient/mytardisclient.cfg
```

Let's list the experiments which user "demofacility" has access to:

```
(mytardisclient) $ mytardis experiment list

Model: Experiment
Query: http://mytardisdemo.erc.monash.edu.au/api/v1/experiment/?format=json
Total Count: 10
Limit: 20
Offset: 0

+----+-------------------+-----------------------------------------------------------+
| ID |    Institution    |                           Title                           |
+====+===================+===========================================================+
| 20 | Monash University | James Exp 001                                             |
+----+-------------------+-----------------------------------------------------------+
| 15 | Monash University | A's 2nd Test Instrument - Test User1                      |
+----+-------------------+-----------------------------------------------------------+
| 12 | Monash University | exp1                                                      |
+----+-------------------+-----------------------------------------------------------+
| 17 | Monash University | Steve's Macbook 12 - Test User1                           |
+----+-------------------+-----------------------------------------------------------+
| 11 | Monash University | Beamline - Test User2                                     |
+----+-------------------+-----------------------------------------------------------+
| 19 | Monash University | Manually created experiment to test filename length in UI |
+----+-------------------+-----------------------------------------------------------+
| 13 | Monash University | A's Test Instrument - Test User1                          |
+----+-------------------+-----------------------------------------------------------+
| 16 | Monash University | A's 2nd Test Instrument - Test User2                      |
+----+-------------------+-----------------------------------------------------------+
| 18 | Monash University | Steve's Macbook 12 - Test User2                           |
+----+-------------------+-----------------------------------------------------------+
| 14 | Monash University | A's Test Instrument - Test User2                          |
+----+-------------------+-----------------------------------------------------------+
```

Now let's create a new experiment called "James Test Exp 001":

```
(mytardisclient) (mytardisclient) $ mytardis experiment create "James Test Exp 001"
MyTardis Client v0.0.1
Config: /Users/wettenhj/.config/mytardisclient/mytardisclient.cfg
MyTardis URL: http://mytardisdemo.erc.monash.edu.au
Username: demofacility

Model: Experiment

+------------------+--------------------+
| Experiment field |       Value        |
+==================+====================+
| ID               | 20                 |
+------------------+--------------------+
| Institution      | Monash University  |
+------------------+--------------------+
| Title            | James Test Exp 001 |
+------------------+--------------------+
| Description      |                    |
+------------------+--------------------+

Experiment created successfully.
```
The default institution ("Monash University") is set in MyTardis's settings.py (on the MyTardis server).

Now let's create a dataset.  Note that when we run "mytardis dataset create" without the experiment ID and description arguments, we get a usage message telling us the names of the missing arguments.

```
(mytardisclient) $ mytardis dataset create
usage: mytardis dataset create [-h] experiment_id description
mytardis dataset create: error: too few arguments

(mytardisclient) $ mytardis dataset create 20 "James Test Dataset 001"
MyTardis Client v0.0.1
Config: /Users/wettenhj/.config/mytardisclient/mytardisclient.cfg
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
Config: /Users/wettenhj/.config/mytardisclient/mytardisclient.cfg
MyTardis URL: http://mytardisdemo.erc.monash.edu.au
Username: demofacility
Uploaded: hello.txt
```

Now let's reload the dataset's datafile list to see the new datafile record:

```
(mytardisclient) $ mytardis dataset get 31
MyTardis Client v0.0.1
Config: /Users/wettenhj/.config/mytardisclient/mytardisclient.cfg
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

+-----+-----------+--------------+----------------------------------------------+----------+-----------+----------------------------------+
| ID  | Directory |   Filename   |                     URI                      | Verified |   Size    |             MD5 Sum              |
+=====+===========+==============+==============================================+==========+===========+==================================+
|  99 |           | hello.txt    | James Test Dataset 001-31/hello.txt          | True     |  13 bytes | 9af2f8218b150c351ad802c6f3d66abe |
+-----+-----------+--------------+----------------------------------------------+----------+-----------+----------------------------------+
```

Note that the file has been verified already.  Now let's determine the file size and MD5 checksum locally and ensure that they match the values recorded in MyTardis:

```
(mytardisclient) $ ls -l hello.txt
-rw-r--r--  1 wettenhj  staff  13 19 Nov 11:23 hello.txt
```
```
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
Config: /Users/wettenhj/.config/mytardisclient/mytardisclient.cfg
MyTardis URL: http://mytardisdemo.erc.monash.edu.au
Username: demofacility
Downloaded: hello.txt

(mytardisclient) $ ls -l hello.txt 
-rw-r--r--  1 wettenhj  staff  13 19 Nov 11:33 hello.txt
```
Results can also be retrieved in JSON format.  Let's retrieve the JSON representation of the datafile record for the file
'hello.txt' in dataset ID 31 (which has a datafile ID of 99):

```
(mytardisclient) $ mytardis datafile get --help
usage: mytardis datafile get [-h] [--json] datafile_id

positional arguments:
  datafile_id  The datafile ID.

optional arguments:
  -h, --help   show this help message and exit
  --json       Display results in JSON format.
```
```
(mytardisclient) $ mytardis datafile get 99 --json
{
  "created_time": "2015-11-19T11:23:53", 
  "datafile": null, 
  "dataset": "/api/v1/dataset/31/", 
  "deleted": false, 
  "deleted_time": null, 
  "directory": "", 
  "filename": "hello.txt", 
  "id": 99, 
  "md5sum": "9af2f8218b150c351ad802c6f3d66abe", 
  "mimetype": "text/plain", 
  "modification_time": null, 
  "parameter_sets": [], 
  "replicas": [
    {
      "created_time": "2015-11-19T11:24:23.486259", 
      "datafile": "/api/v1/dataset_file/99/", 
      "id": 98, 
      "last_verified_time": "2015-11-19T11:24:28.548830", 
      "resource_uri": "/api/v1/replica/98/", 
      "uri": "James Test Dataset 001-31/hello.txt", 
      "verified": true
    }
  ], 
  "resource_uri": "/api/v1/dataset_file/99/", 
  "sha512sum": "44c4f73161332b2b058360310640c6704796ece76593e22ca32f76ccbc2c469d5b26ae64b996c78165929ac1af7f9a0ae6132010c917f6b104196b8648e108d3", 
  "size": "13", 
  "version": 1
}
```
And if a lookup fails, we get a non-zero exit code:

```
(mytardisclient) $ mytardis datafile get 99 > /dev/null
(mytardisclient) $ echo $?
0
```

```
(mytardisclient) $ mytardis datafile get -123 >& /dev/null
(mytardisclient) $ echo $?
1
```

We previously demonstrated how to upload 'hello.txt' to MyTardis via HTTP POST using "mytardis datafile upload ...".  We can also create a datafile record without uploading it, and implement a different file transfer mechanism.  Suppose the MyTardis server has temporary access to user james's account on an HPC system called "analyzer" via SSHFS with an SSH certificate or key-pair.  Then to register file "test.txt" from the "analyzer" HPC system in MyTardis, we create a record for it using "mytardis datafile create".  The "james-analyzer" storage box could be created on MyTardis with location "/mnt/sshfs/james-analyzer" on the MyTardis server.  Now to allow MyTardis to verify the 'test.txt' file, we could either implement a custom storage box (so MyTardis knows it is not in a [dataset-description]-[dataset_id] folder as would normally be the case on MyTardis).  Or we could create a symbolic link on the analyzer HPC system, e.g. ~/.mytardisclient/dataset-links/James Test Dataset 001-31 which points to the actual location of 'test.txt'.

```
(mytardisclient) $ mytardis datafile create --storagebox james-analyzer 31 ./test.txt 

Model: DataFile

+----------------+------------------------------------+
| DataFile field |               Value                |
+================+====================================+
| ID             | 119                                |
+----------------+------------------------------------+
| Dataset        | /api/v1/dataset/31/                |
+----------------+------------------------------------+
| Filename       | test.txt                           |
+----------------+------------------------------------+
| URI            | James Test Dataset 001-31/test.txt |
+----------------+------------------------------------+
| Verified       | False                              |
+----------------+------------------------------------+
| Size           |   5 bytes                          |
+----------------+------------------------------------+
| MD5 Sum        | 2205e48de5f93c784733ffcca841d2b5   |
+----------------+------------------------------------+

DataFile created successfully.
```

We can create an experiment record with parameters as follows:
```
(mytardisclient) $ cat << EOF > experiment_params.json
[
    {
        "schema": "https://mytardis.org/sample-experiment-schema",
        "parameters": [
            {
                "name": "sample_parameter_name",
                "value": "Sample Parameter Value"
            }
        ]
    }
]
EOF

(mytardisclient) $ mytardis experiment create --params experiment_params.json "Experiment With Params"
+------------------+------------------------------+
| Experiment field |            Value             |
+==================+==============================+
| ID               | 27                           |
+------------------+------------------------------+
| Institution      | Monash University            |
+------------------+------------------------------+
| Title            | Experiment With Params       |
+------------------+------------------------------+
| Description      |                              |
+------------------+------------------------------+

+------------------------+--------------------------+-----------------------+------------------------+-----------------+----------------+---------+
| ExperimentParameter ID |          Schema          |    Parameter Name     |      String Value      | Numerical Value | Datetime Value | Link ID |
+========================+==========================+=======================+========================+=================+================+=========+
|                     34 | Sample Experiment Schema | Sample Parameter Name | Sample Parameter Value |                 |                |         |
+------------------------+--------------------------+-----------------------+------------------------+-----------------+----------------+---------+

Experiment created successfully.

We are used an experiment schema which is defined as follows:

(mytardisclient) $ mytardis schema get 12
+--------------+-----------------------------------------------+
| Schema field |                     Value                     |
+==============+===============================================+
| ID           | 12                                            |
+--------------+-----------------------------------------------+
| Name         | Sample Experiment Schema                      |
+--------------+-----------------------------------------------+
| Namespace    | https://mytardis.org/sample-experiment-schema |
+--------------+-----------------------------------------------+
| Type         | Experiment schema                             |
+--------------+-----------------------------------------------+
| Subtype      |                                               |
+--------------+-----------------------------------------------+
| Immutable    | False                                         |
+--------------+-----------------------------------------------+
| Hidden       | False                                         |
+--------------+-----------------------------------------------+

+------------------+-----------------------+-----------------------+-----------+-------+-----------+---------------+-------+---------+-----------------+
| ParameterName ID |       Full Name       |         Name          | Data Type | Units | Immutable | Is Searchable | Order | Choices | Comparison Type |
+==================+=======================+=======================+===========+=======+===========+===============+=======+=========+=================+
|               33 | Sample Parameter Name | sample_parameter_name | String    |       | False     | False         | 9999  |         | Exact value     |
+------------------+-----------------------+-----------------------+-----------+-------+-----------+---------------+-------+---------+-----------------+
```

