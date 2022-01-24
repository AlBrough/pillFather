# Rapt Pill to brewfather. 

### Can be deployed to heroku for free

set variables as follows:

HYDRO_KEY - the ID of the pill from the Rapt API
RAPT_USER - Usually your email 
RAPT_Password - the API secret generated on the RAPT APP*
BF_Pass - The token after the URL generated in brewfather- eg:

http://log.brewfather.net/stream?id=<THIS TOKEN HERE>

You can set the heroku config like this:
``heroku config:set HYDRO_KEY=xx RAPT_USER=xx RAPT_PW=XX BF_PASS=xx``

I used the heroku scheduler to run this hourly- added with the following command:

git add .
git commit -m 'deploy'
git push heroku main
heroku ps:scale web=1
REM heroku open
REM heroku addons:create scheduler:standard
