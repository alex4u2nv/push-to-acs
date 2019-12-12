This simple python module uses [Alfresco's Public APIs] to upload a new
file to an Alfresco Repository.

The module assumes that Alfresco Content Services is configured with 
Alfresco Identity Management Services, and both are accessible through
a common base DNS.

To use, install the module using
```shell script
pip3 install .
```
Then execute using the following command
```shell script
push-to-acs -a https://yourinstance.dev.alfrescocloud.com/ -f ~/test -u username -p YourPassword -d DESTIONATION-FOLDER-NODE-ID

```


[Alfresco's Public APIs]: https://api-explorer.alfresco.com/api-explorer/