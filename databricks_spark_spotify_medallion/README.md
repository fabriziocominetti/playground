# Spotify Data Engineering Project with Databricks and Apache Spark

This project demonstrates a **complete data engineering pipeline** using **Databricks** and the **Spotify 30,000 songs dataset** from Kaggle. The goal is to practice **data ingestion, transformation, and aggregation** across multiple layers (Bronze → Silver → Gold), preparing the dataset for analytics or machine learning tasks.

## Dataset
- **Source:** [Spotify 30,000 Songs Dataset on Kaggle](https://www.kaggle.com/datasets/joebeachcapital/30000-spotify-songs)  
- **Content:** Metadata and audio features for 30,000 tracks, including:  
  - Track info: `track_id`, `track_name`, `track_artist`, `track_popularity`  
  - Album info: `track_album_id`, `track_album_name`, `track_album_release_date`  
  - Playlist info: `playlist_name`, `playlist_genre`, `playlist_subgenre`  
  - Audio features: `danceability`, `energy`, `loudness`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, `duration_ms`  

## Project Structure

```
project/
│
├─ notebooks/
│   └─ spotify_songs_de_analysis.ipynb
│
├─ data/
│   └─ spotify_songs.csv
│
└─ README.md
```

## Pipeline Layers

1. **Bronze (Raw)**  
   - Ingests the original CSV dataset into a Delta table  
   - Basic data cleaning  

2. **Silver (Cleaned / Enriched)**  
   - Converts columns to proper types using `try_cast`  
   - Handles missing values  
   - Adds derived columns, e.g., `duration_flag` (tracks ≥ 3 minutes)  

3. **Gold (Aggregated / Analytics-ready)**  
   - Aggregates features by **artist, album, and playlist**  
   - Calculates averages of audio features and popularity metrics  
   - Prepares data for downstream analytics or ML tasks  

## Tools & Libraries
- **Databricks** (Free Edition)  
- **PySpark** for distributed data processing  
- **Delta Lake** for reliable, versioned tables  

## How to Run
1. Upload the Kaggle CSV dataset to your Databricks workspace.  
2. Run `1_ingest_bronze.py` to create the Bronze, Silver, and Gold table.  