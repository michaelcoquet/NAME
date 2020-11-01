Before running pytest, ensure the following steps have been completed: 
    1. Install python 3.9.0 and add it to PATH
    2. Install the pytest module via pip install pytest
    3. Install the spotipy module via pip install spotipy
    4. On the command line, navigate to the directory containing unit_test.py


to run this test you must allow pytest to collect user input with the -s option
using windows the tests can be ran with: 
    $ python -m pytest -s

    if this is the first run of the test app the spotify API will redirect you to
    a url of the following format:
        https://example.com/callback?code=.............
    this URL must be copy and pasted as input to the test once requested