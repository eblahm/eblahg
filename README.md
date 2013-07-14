## Description

Eblahg is my dedicated blogging app for the Google App Engine platform.  It uses a [Draft](https://draftin.com/) webhook for editing and publishing and it uses Dropbox REST Api to add images to a randomized sidebar.  See a live example [here](http://eblahm.appspot.com)

## Requirments

- [Google App Engine (GAE) SDK](https://developers.google.com/appengine/downloads)
- [GAE App ID](https://appengine.google.com/)
- Dropbox Developer account with [your own App Token and Secret](https://www.dropbox.com/developers/apps)

## How to Blog...
Once you clone the repository follow these steps

1. Edit app.yaml and config.py to reflect your app's info

2. Deploy the code to App Engine using the SDK

3. Visit /settings and fill in your dropbox info

4. Click the "sync" button.  This will create the file structure within the Apps folder of your Dropbox

5. add images to the "pics" folders.  Pictures in this folder form the basis of the random sidebar

6. [Add your draft webhook url](https://draftin.com/publishers) (hint: your secret url is located @ /settings page)

## Credits:
Twitter Bootstrap
Jquery  
Mike Knapp - [AppEngine-OAuth-Library](https://github.com/mikeknapp/AppEngine-OAuth-Library)  
Joey Bratton [joeyb-blog](https://github.com/joeyb/joeyb-blog)  
Markdown 2.0.1  
PyRSS2Gen 1.0.0  
