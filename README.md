## Description

Eblahg is a dedicated blogging app for the Google App engine platform.  It uses Markdown and the Dropbox Rest Api.  See a live example [here](http://eblahm.appspot.com)

Its is still a work in progress. Feel free to contribute.

## Requirments

- [Google App Engine (GAE) SDK](https://developers.google.com/appengine/downloads)
- [GAE App ID](https://appengine.google.com/)
- Dropbox Developer account with [your own App Token and Secret](https://www.dropbox.com/developers/apps)

## How to Blog...
Once you clone the repository follow these steps

1. Edit App.yaml and config.py to reflect your app's info

2. Deploy the code to App Engine using the SDK

3. Visit /config and fill in the appropriate info your info

4. Click the "INITIALIZE DROPBOX API CLIENT" button.  This will create the file structure within the APPS folder of your Drobox

5. add content to the "published", "pics", and "sidebar_pics" folders

6. manually launch sync script using the url: /admin/sync
You can make this task reoccur as often as you like using cron.yaml


## Credits:
Twitter Bootstrap  
Mike Knapp - [AppEngine-OAuth-Library](https://github.com/mikeknapp/AppEngine-OAuth-Library)  
Joey Bratton [joeyb-blog](https://github.com/joeyb/joeyb-blog)  
Markdown 2.0.1  
PyRSS2Gen 1.0.0  
