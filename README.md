# [Communal Youtube Website](https://communalyoutube.com)

> This is the front-end website design for the project of a communal youtube channel. 

## the idea:
Allow any user to anonymously contribute to the same youtube channel... communally.
#### the features:
a button that allows users to select a video to be anonymously uploaded to the same youtube channel. 


youtubevideouploader.py continuously checks the /uploads directory for new videos added every 3 minutes. If a video is found, it is uploaded to the Communal Youtube youtube channel before being deleted from the directory.

## for the future: 
- allow longer videos to be submitted
  - at this point the limit to how short a video needs to be is unknown
- add more security measures
  - allowing users to upload directly to a directory on the back-end is a disgusting security risk
- webcam abilities
