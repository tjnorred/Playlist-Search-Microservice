# Name: TJ Norred
# Course: CS361 - Software Engineering I
# Assignment: 8
# Due Date: 02/25/2025
# Description: Microservice A - Playlist Search

import zmq
import json
import logging
import argparse

logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def search_playlist(playlists: dict, playlist_name: str, search_category: str, search_term: str) -> str:
    """Searches a playlist by category and the search term. Returns string notifying the user if there was a match or not"""

    # Check if the playlist exists
    if playlist_name not in playlists:
        return f"Playlist '{playlist_name}' not found"

    # Get the songs in the specified playlist
    songs = playlists[playlist_name]

    # Iterate through all the songs in the playlist
    for song in songs:
        # Check for a match
        if search_term.lower() in song[search_category.lower()].lower():
            return f"The {search_category} {search_term} was found in the playlist"

    return "No matches found"

def server(port: int) -> None:
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")

    print(f"INFO: Server is listening on port {port}")
    logging.info(f"Server is listening on port {port}")

    while True:
        try:
            received_data = json.loads(socket.recv_string())
            client_ip = socket.getsockopt_string(zmq.LAST_ENDPOINT).split("://")[1].split(":")[0]
            log_message = f"Received request from {client_ip}: {received_data}"
            print(f"Received request from {client_ip}: Searching playlist {received_data["playlist_name"]} for {received_data["search_category"]} '{received_data["search_term"]}'")
            logging.info(log_message)

            results = search_playlist(received_data["playlists"], received_data["playlist_name"], received_data["search_category"], received_data["search_term"])

            socket.send_string(results)
            log_message = f"Sent response to {client_ip}: {results}"
            print(log_message)
            logging.info(log_message)
        
        except KeyboardInterrupt:
            socket.close()
            context.term()
            log_message = "Server shutting down"
            print(log_message)
            logging.warning(log_message)
            break
        except Exception as e:
            client_ip = socket.getsockopt_string(zmq.LAST_ENDPOINT).split("://")[1].split(":")[0]
            log_message = f"An unexpected error occurred from {client_ip}: {e}"
            print(log_message)
            logging.exception(log_message)
            socket.send_string(f"ERROR: An unexpected error occurred. Check your data and try again.")

def main() -> None:
    parser = argparse.ArgumentParser(description="Playlist Search")
    parser.add_argument("-p", "--port", type=int, default=5555, help="Port number to listen on (default: 5555)")
    args = parser.parse_args()

    port = args.port

    server(port)

if __name__ == "__main__":
    main()

