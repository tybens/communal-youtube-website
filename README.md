# [Communal Youtube Website](https://communalyoutube.com)

> This is the front-end website design to support the communal youtube channel. 

## the idea:
Allow any user to anonymously contribute to the same youtube channel... communally.
#### features
a button that allows users to select a video to be anonymously uploaded to the same youtube channel. 


`ytVideoUploader.py` continuously checks the `/uploads` directory for new videos added every 3 minutes. If a video is found, it is uploaded to the [Communal Youtube](https://youtube.com/channel/UC_SReR6zWYD5XQLztnLtP-g) youtube channel before being deleted from the directory.


#### packages required for `ytVideoUploader.py`
```Bash
pip install google-auth-oauthlib google-python-api-client apiclient httplib httplib2
```

## for the future: 
- allow longer videos to be submitted
  - at this point the limit to how short a video needs to be is unknown
- add more security measures
  - allowing users to upload directly to a directory on the back-end is a disgusting security risk
- webcam abilities
