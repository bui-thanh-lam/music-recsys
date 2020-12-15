from fastapi import FastAPI
import uvicorn
from apis.recommendations import get_recommendations as recom

app = FastAPI()


@app.get("/recommendations/{user_id}/{playlist_id}")
def get_recomendations(user_id: str, playlist_id: int, n_tracks: int = 10):
    if playlist_id == 1:
        return recom.get_CF_playlist(user_id, n_tracks)
    return None


@app.get("/nextup/{user_id}/{seed_track_id}")
def get_nextup_tracks(user_id: str, seed_track_id: str, n_tracks: int = 5):
    return recom.get_nextup_tracks(user_id, seed_track_id, n_tracks)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
