CREATE TABLE IF NOT EXISTS songs (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    album TEXT NOT NULL,
    path TEXT NOT NULL UNIQUE,
    created_at REAL
);

INSERT INTO songs (title, artist, album, path, created_at) VALUES
('15 Step', 'Radiohead', 'In Rainbows',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/In Rainbows/01. 15 Step.mp3', strftime('%s','now')),

('Bodysnatchers', 'Radiohead', 'In Rainbows',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/In Rainbows/02. Bodysnatchers.mp3', strftime('%s','now')),

('Nude', 'Radiohead', 'In Rainbows',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/In Rainbows/03. Nude.mp3', strftime('%s','now')),

('Weird Fishes / Arpeggi', 'Radiohead', 'In Rainbows',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/In Rainbows/04. Weird Fishes , Arpeggi.mp3', strftime('%s','now')),

('All I Need', 'Radiohead', 'In Rainbows',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/In Rainbows/05. All I Need.mp3', strftime('%s','now')),

('Faust Arp', 'Radiohead', 'In Rainbows',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/In Rainbows/06. Faust Arp.mp3', strftime('%s','now')),

('Reckoner', 'Radiohead', 'In Rainbows',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/In Rainbows/07. Reckoner.mp3', strftime('%s','now')),

('House Of Cards', 'Radiohead', 'In Rainbows',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/In Rainbows/08. House Of Cards.mp3', strftime('%s','now')),

('Jigsaw Falling Into Place', 'Radiohead', 'In Rainbows',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/In Rainbows/09. Jigsaw Falling Into Place.mp3', strftime('%s','now')),

('Videotape', 'Radiohead', 'In Rainbows',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/In Rainbows/10. Videotape.mp3', strftime('%s','now'));

INSERT INTO songs (title, artist, album, path, created_at) VALUES
('Feather', 'Nujabes', 'Modal Soul',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Modal Soul/01. Feather (feat. Cise Starr & Akin).mp3', strftime('%s','now')),

('Ordinary Joe', 'Nujabes', 'Modal Soul',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Modal Soul/02. Ordinary Joe (feat. Terry Callier).mp3', strftime('%s','now')),

('Reflection Eternal', 'Nujabes', 'Modal Soul',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Modal Soul/03. Reflection Eternal.mp3', strftime('%s','now')),

('Luv (Sic.) Pt. 3', 'Nujabes', 'Modal Soul',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Modal Soul/04. Luv (Sic.) Pt. 3 (feat. Shing02).mp3', strftime('%s','now')),

('Music Is Mine', 'Nujabes', 'Modal Soul',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Modal Soul/05. Music Is Mine.mp3', strftime('%s','now')),

('Eclipse', 'Nujabes', 'Modal Soul',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Modal Soul/06. Eclipse (feat. Substantial).mp3', strftime('%s','now')),

('The Sign', 'Nujabes', 'Modal Soul',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Modal Soul/07. The Sign (feat. Pase Rock).mp3', strftime('%s','now')),

('Thank You', 'Nujabes', 'Modal Soul',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Modal Soul/08. Thank You (feat. Apani B).mp3', strftime('%s','now')),

('Worlds End Rhapsody', 'Nujabes', 'Modal Soul',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Modal Soul/09. World''s End Rhapsody.mp3', strftime('%s','now')),

('Modal Soul', 'Nujabes', 'Modal Soul',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Modal Soul/10. Modal Soul (feat. Uyama Hiroto).mp3', strftime('%s','now')),

('Flowers', 'Nujabes', 'Modal Soul',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Modal Soul/11. Flowers.mp3', strftime('%s','now')),

('Sea Of Cloud', 'Nujabes', 'Modal Soul',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Modal Soul/12. Sea Of Cloud.mp3', strftime('%s','now')),

('Light On The Land', 'Nujabes', 'Modal Soul',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Modal Soul/13. Light On The Land.mp3', strftime('%s','now')),

('Horizon', 'Nujabes', 'Modal Soul',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Modal Soul/14. Horizon.mp3', strftime('%s','now'));

INSERT INTO songs (title, artist, album, path, created_at) VALUES
('Taxman', 'The Beatles', 'Revolver',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Revolver/01. Taxman.mp3', strftime('%s','now')),

('Eleanor Rigby', 'The Beatles', 'Revolver',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Revolver/02. Eleanor Rigby.mp3', strftime('%s','now')),

('I''m Only Sleeping', 'The Beatles', 'Revolver',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Revolver/03. I''m Only Sleeping.mp3', strftime('%s','now')),

('Love You To', 'The Beatles', 'Revolver',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Revolver/04. Love You To.mp3', strftime('%s','now')),

('Here, There And Everywhere', 'The Beatles', 'Revolver',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Revolver/05. Here, There And Everywhere.mp3', strftime('%s','now')),

('Yellow Submarine', 'The Beatles', 'Revolver',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Revolver/06. Yellow Submarine.mp3', strftime('%s','now')),

('She Said She Said', 'The Beatles', 'Revolver',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Revolver/07. She Said She Said.mp3', strftime('%s','now')),

('Good Day Sunshine', 'The Beatles', 'Revolver',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Revolver/08. Good Day Sunshine.mp3', strftime('%s','now')),

('And Your Bird Can Sing', 'The Beatles', 'Revolver',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Revolver/09. And Your Bird Can Sing.mp3', strftime('%s','now')),

('For No One', 'The Beatles', 'Revolver',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Revolver/10. For No One.mp3', strftime('%s','now')),

('Doctor Robert', 'The Beatles', 'Revolver',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Revolver/11. Doctor Robert.mp3', strftime('%s','now')),

('I Want To Tell You', 'The Beatles', 'Revolver',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Revolver/12. I Want To Tell You.mp3', strftime('%s','now')),

('Got To Get You Into My Life', 'The Beatles', 'Revolver',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Revolver/13. Got To Get You Into My Life.mp3', strftime('%s','now')),

('Tomorrow Never Knows', 'The Beatles', 'Revolver',
'/Users/anantagarwal/Desktop/dev/projects/shazam/songs/Albums/Revolver/14. Tomorrow Never Knows.mp3', strftime('%s','now'));