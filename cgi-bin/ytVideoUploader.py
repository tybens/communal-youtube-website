#!/usr/bin/python

import httplib
import httplib2

import os
import time

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload


# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected, httplib.IncompleteRead, httplib.ImproperConnectionState,  httplib.CannotSendRequest, httplib.CannotSendHeader, httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

scopes = ["https://www.googleapis.com/auth/youtube.upload"]
def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "./CLIENT_SECRETS_FOR_YOUTUBE.json" # this needs to be changed to be your client secrets!

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    path_to_watch = "../uploads/"
    before = dict([(f, None) for f in os.listdir(path_to_watch)])
    while True:
        after = dict([(f, None) for f in os.listdir(path_to_watch)])
        added = [f for f in after if not f in before]
        if added:
            print("File Added: " + ", ".join(added))
        before = after
        print(added)
        for video in added:
            
            title = video.split('.')[0]  # takes the string before a period extension (.mp4)
            
            request_body = {
                'snippet': {
                    'categoryI': 19,
                    'title':title,
                    'description':"This is uploaded video number {}!!".format(len(before))
                },
                'status': {
                    'privatyStatus':'private',
                    'selfDeclaredMadeForKids':False,
                },
                'notifySubscribers': False
            }
            
            insert_request = youtube.videos().insert(
                part='snippet,status',
                body = request_body,
                
                media_body = MediaFileUpload(path_to_watch+video, chunksize=-1, resumable=True)
            )
            resumable_upload(insert_request)
            os.remove(path_to_watch+video)

        # TODO: delete this for the while loop eventually
        time.sleep(60*3)

                
# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print("Video id '%s' was successfully uploaded." % response['id'])
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: " + str(e)

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping {} seconds and then retrying...".format(sleep_seconds))
            time.sleep(sleep_seconds)


if __name__ == "__main__":
    main()
