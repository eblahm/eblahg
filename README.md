#### Description

Eblahg is my dedicated blogging app for the Google App Engine platform.  It uses a [Draft](https://draftin.com/) webhook for editing and publishing and it uses Dropbox REST Api to add images to a randomized sidebar.  See a live example [here](http://eblahm.appspot.com)

#### Requirments

- [Google App Engine (GAE) SDK](https://developers.google.com/appengine/downloads)
- [GAE App ID](https://appengine.google.com/)
- Dropbox Developer account with [your own App Token and Secret](https://www.dropbox.com/developers/apps)
- a [Draft](https://draftin.com/) Account

#### Getting Started...

1. Edit app.yaml and config.py to reflect your app's info

2. `appcfg.py update /path/to/eblahg` note: appcfg.py shell command is installed w/ GAE SDK

3. Visit http://yourappid.appspot.com/settings and fill in your dropbox info

4. Click the "sync" button.  This will create the file structure within the Apps folder of your Dropbox

5. add images to the "pics" folders in your Dropbox.  Pictures in this folder form the basis of the random sidebar

6. log into your Draft settings and paste [your webhook url](https://draftin.com/publishers) (hint: your secret webhook url is located on the http://yourappid.appspot.com/settings page)

7. Create a document in [Draft](https://draftin.com/) and click publish!! 

#### tagging and date stamping

Optional Article Tagging and Date Stamping can be inputed via the "title" field in Draft.
The syntax is `title | date:mm/dd/yyyy | tags:foo,bar`

acceptable examples
- `top ten funny things`
- `top ten funny things | tags:humor,top 10 lists`
- `top ten funny things | tags:humor,top 10 lists | date:03/19/2014`

#### Credits:
Twitter Bootstrap  
Jquery  
Mike Knapp - [AppEngine-OAuth-Library](https://github.com/mikeknapp/AppEngine-OAuth-Library)  
Joey Bratton [joeyb-blog](https://github.com/joeyb/joeyb-blog)  
Markdown 2.0.1  
PyRSS2Gen 1.0.0  
