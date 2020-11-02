Before running pytest, ensure the following steps have been completed: 
    1. Install python 3.9.0 and add it to PATH
    2. Install the pytest module via pip install pytest
    3. Install the spotipy module via pip install spotipy
    4. On the command line, navigate to the directory containing unit_test.py
    5. Make sure to log out of any personal Spotify Accounts you may have open
       (becuase spotify will usually keep you logged in)
    6. It's possible (highly unlikely) that you have an old .cache file in the 
       testing directory already, this must be deleted before running the test

How to run:
 - must allow pytest to collect user input with the -s option
  using windows the tests can be ran with: 
    $ python -m pytest -s

 - The test app will then redirect you to an authorization page
   where you will have to login

 - For testing purposes a new Spotify account was created which you
   will need to login to for this test

 - Once requested for a spotify username and password enter:
    username: cmpt370.group5@gmail.com
    password: pennywise_1640

 - After login you will be redirected to a callback page with
    a url of the following format:
        https://example.com/callback?code=.............
    this URL must be copy and pasted as input to the test app once requested

 - After all of this, the test will make a request from the Spotify API
   to return all (up to a limit of 50) the test users playlists 
   (in this case testing0, testing1, testing2) and assert that these 
   playlists are indeed being returned properly