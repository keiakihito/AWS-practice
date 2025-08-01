CREATE TABLE albums (
  album_id SERIAL PRIMARY KEY,
  title TEXT,
  composer TEXT,
  artist TEXT,
  conductor TEXT,
  orchestra TEXT,
  label TEXT,
  release_date DATE,
  genre TEXT[],
  period TEXT,
  cover_url TEXT,
  s3_prefix TEXT,

  original_format TEXT,
  digitized_format TEXT,
  licensing_status TEXT,
  third_party_link TEXT,
  notes TEXT,
  has_metadata_entry BOOLEAN DEFAULT TRUE,

  total_duration INTERVAL,                           -
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE tracks (
  id SERIAL PRIMARY KEY,
  album_id INTEGER REFERENCES albums(album_id) ON DELETE CASCADE,
  track_no INTEGER,
  title TEXT,
  duration INTERVAL,
  tags TEXT[],
  soloists TEXT,               
  s3_key TEXT UNIQUE,
  preview_url TEXT,

  original_format TEXT,
  digitized_format TEXT,
  licensing_status TEXT,
  third_party_link TEXT,
  notes TEXT,
  has_metadata_entry BOOLEAN DEFAULT TRUE,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

