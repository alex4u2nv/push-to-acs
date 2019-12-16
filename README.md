# Description
This simple python module uses [Alfresco's Public APIs] to upload a 
file to an Alfresco Repository.

It does so by monitoring a folder on your local filesystem for new files.
When a new file enters the folder, the module will upload it to ACS using the APIs.
This project is another example of using Alfresco's REST API with OAuth authentication.

The module assumes that Alfresco Content Services is configured with 
Alfresco Identity Management Services, and both are accessible through
a common base DNS.

# Installation
To use, install the module using
```shell script
pip3 install .
```

# Usage
Then execute using the following command
```shell script
push-to-acs -a https://yourinstance.dev.alfrescocloud.com/ -f ~/test -u username -p YourPassword -d DESTIONATION-FOLDER-NODE-ID

```

# Structure
* `bin/push-to-acs` This is the python executable
* `push_content/Auth.py` This module contains a class that handles authentication.
* `push_content/PushContent.py` This module contains the classes to monitor the the filesystem events, and upload the 
content to ACS.

# Authentication
1. Request an JWT token using the AIMS token API, and sending the user name and password of the service account
2. Store the Token data. Such as Token Timeout, Access Token, and Refresh Token
3. If the Access token is still valid, then return it.
4. If the Access token is about to time out, based on the token timeout value, then we refresh the token.
5. We check on the token every 5 seconds, so that it can refresh as needed. So that when a file is uploaded, the token
is good for upload.


# Upload
1. Currently you must use the Node ID's guid as your destination reference
2. The ACS multidata form upload method is used
3. We allow for versioning a new document

# Filesystem Monitoring
1. We check for new and modified files and upload them. Incase we don't clean up the monitored directory
2. Optionally, files that have been uploaded can be removed from the folder.
3. Nested folder structures aren't supported in this poc






[Alfresco's Public APIs]: https://api-explorer.alfresco.com/api-explorer/