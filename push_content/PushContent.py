import json
import logging
import os
import time

import requests
from watchdog.events import FileSystemEventHandler
import ntpath

from push_content.Auth import Authenticate


class PushContent:
    acs = None
    destination = None
    remove = False
    auth = None

    def __init__(self, auth: Authenticate, base_url, destination, remove):
        logging.info("Uploading file to {dest}".format(dest=destination))
        base_url = base_url.strip('/')
        self.acs = "{base_url}/alfresco".format(base_url=base_url)
        self.destination = destination
        self.remove = remove
        self.auth = auth

    def upload_content(self, src_path):
        token = self.auth.get_jwt()
        push_content_api = "{acs}/api/-default-/public/alfresco/versions/1/nodes/{destination}/children".format(
            acs=self.acs, destination=self.destination)
        querystring = {"autoRename": "true", "include": "allowableOperations", "majorVersion": "true",
                       "overwrite": "true"}

        file_name = ntpath.basename(src_path)

        headers = {
            "authorization": "Bearer {jwt}".format(jwt=token)
        }

        filedata = {"filedata": open(src_path, 'rb')}
        data = dict(
            majorVersion="true",
            overwrite="true"
        )
        resp = requests.request('POST', push_content_api, headers=headers, data=data, files=filedata)
        if resp.status_code != 201:
            logging.error("Error in uploading the document")
            logging.error(resp.text)
            return None

        fileinfo = resp.json()
        if self.remove:
            os.remove(src_path)
        logging.info("File uploaded with nodeId: {nodeId}".format(nodeId=fileinfo['entry']['id']))


class EventsHandler(FileSystemEventHandler):
    """Monitor for created files, and upload them"""
    pushcontent = None

    def __init__(self, pushcontent: PushContent):
        self.pushcontent = pushcontent

    def on_moved(self, event):
        super(EventsHandler, self).on_moved(event)

    def on_created(self, event):
        super(EventsHandler, self).on_created(event)
        if not event.is_directory:
            self.pushcontent.upload_content(event.src_path)

    def on_deleted(self, event):
        super(EventsHandler, self).on_deleted(event)

    def on_modified(self, event):
        super(EventsHandler, self).on_modified(event)
        if not event.is_directory:
            self.pushcontent.upload_content(event.src_path)


def validate_path(path):
    if path == '/':
        logging.fatal("FATAL: You specified the root of your filesystem. Exiting...")
        exit(1)
