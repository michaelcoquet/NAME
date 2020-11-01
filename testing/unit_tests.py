from proof_of_concept import Playlist
from proof_of_concept import Song
from proof_of_concept import Member

def main():
    # get to the testers user ID
    myID = input("To run this test please enter your Spotify ID (also make sure to have 1 or more playlists): ")

    me = Member(myID)

    # print out each of the users saved playlists
    playlists = me.getSpotifyPlaylists()

    # manually check if the playlists are correct
    print(playlists)
    response = input("Are the playlists returned correct? (yes/no)")
    
    if(response == "yes" or response == "y"):
        print("test passed")
    else:
        print("test failed")

if __name__ == "__main__":
    main()