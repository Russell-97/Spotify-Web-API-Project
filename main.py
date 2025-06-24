from dotenv import load_dotenv
import os
import spotify
import asyncio

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

client = spotify.Client(client_id=client_id, client_secret=client_secret)

async def main():

    artist_name = input("Enter artist name to get their most popular tracks: ")

    results = await client.search(artist_name, types=["artist"], limit=1)

    if not results.artists:
        print("Artist not found.")
        return

    artist = results.artists[0]
    print(f"\nTop Tracks for {artist.name}:\n")

    top_tracks_data = await client.http.artist_top_tracks(artist.id, market="US")
    top_tracks = top_tracks_data["tracks"]

    for idx, track in enumerate(top_tracks):
        print(f"{idx + 1}. {track.name}")

# Run the async function using asyncio
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())



