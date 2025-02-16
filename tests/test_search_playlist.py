import unittest
from server import search_playlist

class TestSearchPlaylist(unittest.TestCase):

    def setUp(self):
        self.playlists = {
            "Running Mood": [
                {"title": "Where You Are", "artist": "John Summit", "genre": "Electronic"},
                {"title": "Summer", "artist": "Calvin Harris", "genre": "Electronic"},
                {"title": "Running Up That Hill (A Deal With God)", "artist": "Kate Bush", "genre": "Synth-Pop"}
            ],
            "Chill Vibes": [
                {"title": "Redbone", "artist": "Childish Gambino", "genre": "R&B"},
                {"title": "Get You", "artist": "Daniel Caesar", "genre": "R&B"},
                {"title": "Location", "artist": "Khalid", "genre": "Pop"}
            ],
            "Rock Anthems": [
                {"title": "Thunderstruck", "artist": "AC/DC", "genre": "Rock"},
                {"title": "Bohemian Rhapsody", "artist": "Queen", "genre": "Rock"},
                {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "genre": "Grunge"}
            ]
    }

    def test_playlist_not_found(self):
        self.assertEqual(search_playlist(self.playlists, "Running Jamz", "title", "Summer"), "Playlist 'Running Jamz' not found")

    def test_artist_found(self):
        result = search_playlist(self.playlists, "Running Mood", "artist", "John Summit")
        self.assertEqual(result, "The artist John Summit was found in the playlist")

    def test_artist_not_found(self):
        result = search_playlist(self.playlists, "Rock Anthems", "artist", "Matchbox Twenty")
        self.assertEqual(result, "No matches found")

    def test_title_found(self):
        result = search_playlist(self.playlists, "Chill Vibes", "title", "Redbone")
        self.assertEqual(result, "The title Redbone was found in the playlist")

    def test_title_not_found(self):
        result = search_playlist(self.playlists, "Chill Vibes", "title", "Over The Rainbow")
        self.assertEqual(result, "No matches found")

    def test_genre_found(self):
        result = search_playlist(self.playlists, "Running Mood", "genre", "Electronic")
        self.assertEqual(result, "The genre Electronic was found in the playlist")

    def test_genre_not_found(self):
        result = search_playlist(self.playlists, "Chill Vibes", "genre", "Country")
        self.assertEqual(result, "No matches found")

    def test_case_insensitive(self):
        result = search_playlist(self.playlists, "Rock Anthems", "title", "bohemian rhapsody")
        self.assertEqual(result, "The title bohemian rhapsody was found in the playlist")

        result = search_playlist(self.playlists, "Running Mood", "artist", "CALVIN HARRIS")
        self.assertEqual(result, "The artist CALVIN HARRIS was found in the playlist")

        result = search_playlist(self.playlists, "Chill Vibes", "genre", "r&B")
        self.assertEqual(result, "The genre r&B was found in the playlist")

if __name__ == '__main__':
    unittest.main()   