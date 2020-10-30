from example_class import User

# Test list for the hasSpotifyAccount method
hasSpotifyAccount_tests = [
    {
        "test ID": 0, # maybe useful to match with our documentation if we assign specific IDs to tests
        "class_attributes": ["Member"],
        "inputs": [],
        "output": True,
        "message": "User did have a linked Spotify account, but the method returned False"
    },
    {
        "test ID": 1,
        "class_attributes": ["Guest"],
        "inputs": [],
        "output": False,
        "message": "User did not have a linked Spotify account, but the method returned True"
    }
]

# Test list for the isGuest method
isGuest_tests = [
    {
        "test ID": 3,
        "class_attributes": ["Guest"],
        "inputs": [],
        "output": True,
        "message": "User is a Guest, but the method returned False"
    },
    {
        "test ID": 4,
        "class_attributes": ["Member"],
        "inputs": [],
        "outputs": False,
        "message": "User is not a Guest, but the method returned True"
    }
]

# Test driver for hasSpotifyAccount
for test in hasSpotifyAccount_tests:
    user = User(test["class_attributes"][0])
    result = user.hasSpotifyAccount()
    assert result == test["output"], test["message"]

# Test driver for isGuest
for test in isGuest_tests:
    user = User(test["class_attributes"][0])
    result = user.isGuest()
    assert result == test["output"], test["message"]
