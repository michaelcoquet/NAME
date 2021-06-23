# Group 5

Tuesday Tutorial

Elizabeth Reid  
Sean Warren  
Benjamin Camplin  
Laurence Craig Garcia  
Michael Coquet  

For instructions on running our test suite, read the README.md file in the testing folder.

To build and run our program, follow these steps: 

1. Ensure that [Python 3.9.0](https://www.python.org/downloads/release/python-390/) has been downloaded and added to the PATH. 
2. Install the following modules as outlined below: 

- pip install spotipy==2.16.1 [spotipy](https://spotipy.readthedocs.io/en/2.16.1/)
- pip install lyricsgenius==2.0.2 [lyricsgenius](https://pypi.org/project/lyricsgenius/)
- pip install numpy==1.19.3 [numpy](https://numpy.org/)
- pip install pymongo==3.11.2 [pymongo](https://pymongo.readthedocs.io/en/stable/)
- pip install dnspython==2.0.0 [dnspython](https://www.dnspython.org/)

Note: it is particularly important that the installed version of numpy is 1.19.3, as there are incompatibilites between other versions of numpy and Python 3.9.0. To ensure compatability, make sure that the other packages also match the above versions.

All other modules used in our project should come as part of the Python 3.9.0 distribution, but could also be installed with pip if needed. If this is this case, you will be prompted with a message that the module does not exist when running our program for the first time: simply pip install the missing module and re-run the bin.py file. 

3. Dowload our project from the master branch (it will download as a compressed file). Extract the folders from the compressed file: within the extracted folder, there should be a group5-master folder which will contain our project files (in particular, it should contain the bin.py file). To run the project, navigate to this folder location on the command line and type python bin.py.

4. At this point, the GUI should appear and you can use our app. Do not close the command line while using the app. 

Note: Our project has been fully tested for the Windows OS only. We expect it to work correctly on other operating systems, but there may be unforseen errors that occur. 
