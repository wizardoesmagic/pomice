# Pomice Advanced Features

This document describes the new advanced features added to Pomice to enhance your music bot capabilities.

## 📚 Table of Contents

1. [Track History](#track-history)
2. [Queue Statistics](#queue-statistics)
3. [Playlist Manager](#playlist-manager)
4. [Track Utilities](#track-utilities)

---

## 🕐 Track History

Keep track of previously played songs with navigation and search capabilities.

### Features
- Configurable maximum history size
- Navigation (previous/next)
- Search through history
- Filter by requester
- Get unique tracks (remove duplicates)

### Usage

```python
import pomice

# Create a history tracker
history = pomice.TrackHistory(max_size=100)

# Add tracks as they play
history.add(track)

# Get last 10 played tracks
recent = history.get_last(10)

# Search history
results = history.search("Imagine Dragons")

# Get tracks by specific user
user_tracks = history.get_by_requester(user_id=123456789)

# Navigate through history
previous_track = history.get_previous()
next_track = history.get_next()

# Get all unique tracks (removes duplicates)
unique = history.get_unique_tracks()

# Clear history
history.clear()
```

### Properties
- `is_empty` - Check if history is empty
- `current` - Get current track in navigation

---

## 📊 Queue Statistics

Get detailed analytics about your queue contents.

### Features
- Total and average duration
- Longest/shortest tracks
- Requester statistics
- Author distribution
- Duration breakdown
- Stream detection
- Playlist distribution

### Usage

```python
import pomice

# Create stats for a queue
stats = pomice.QueueStats(player.queue)

# Get total duration
total_ms = stats.total_duration
formatted = stats.format_duration(total_ms)  # "1:23:45"

# Get average duration
avg_ms = stats.average_duration

# Find longest and shortest tracks
longest = stats.longest_track
shortest = stats.shortest_track

# Get requester statistics
requester_stats = stats.get_requester_stats()
# Returns: {user_id: {'count': 5, 'total_duration': 900000, 'tracks': [...]}}

# Get top requesters
top_requesters = stats.get_top_requesters(limit=5)
# Returns: [(requester, count), ...]

# Get author distribution
authors = stats.get_author_distribution()
# Returns: {'Artist Name': track_count, ...}

# Get top authors
top_authors = stats.get_top_authors(limit=10)
# Returns: [('Artist Name', count), ...]

# Get duration breakdown
breakdown = stats.get_duration_breakdown()
# Returns: {'short': 10, 'medium': 25, 'long': 5, 'very_long': 2}

# Get stream count
streams = stats.get_stream_count()

# Get comprehensive summary
summary = stats.get_summary()
```

### Summary Dictionary
```python
{
    'total_tracks': 42,
    'total_duration': 7200000,  # milliseconds
    'total_duration_formatted': '2:00:00',
    'average_duration': 171428.57,
    'average_duration_formatted': '2:51',
    'longest_track': Track(...),
    'shortest_track': Track(...),
    'stream_count': 3,
    'unique_authors': 15,
    'unique_requesters': 5,
    'duration_breakdown': {...},
    'loop_mode': LoopMode.QUEUE,
    'is_looping': True
}
```

---

## 💾 Playlist Manager

Export and import playlists to/from JSON and M3U formats.

### Features
- Export queue to JSON
- Import playlists from JSON
- Export to M3U format
- Merge multiple playlists
- Remove duplicates
- Playlist metadata

### Usage

#### Export Queue
```python
import pomice

# Export current queue
pomice.PlaylistManager.export_queue(
    player.queue,
    filepath='playlists/my_playlist.json',
    name='My Awesome Playlist',
    description='Best songs ever',
    include_metadata=True  # Include requester info
)
```

#### Import Playlist
```python
# Import playlist data
data = pomice.PlaylistManager.import_playlist('playlists/my_playlist.json')

# Get just the URIs
uris = pomice.PlaylistManager.get_track_uris('playlists/my_playlist.json')

# Load tracks into queue
for uri in uris:
    results = await player.get_tracks(query=uri)
    if results:
        await player.queue.put(results[0])
```

#### Export Track List
```python
# Export a list of tracks (not from queue)
tracks = [track1, track2, track3]
pomice.PlaylistManager.export_track_list(
    tracks,
    filepath='playlists/favorites.json',
    name='Favorites',
    description='My favorite tracks'
)
```

#### Merge Playlists
```python
# Merge multiple playlists into one
pomice.PlaylistManager.merge_playlists(
    filepaths=['playlist1.json', 'playlist2.json', 'playlist3.json'],
    output_path='merged_playlist.json',
    name='Mega Playlist',
    remove_duplicates=True  # Remove duplicate tracks
)
```

#### Export to M3U
```python
# Export to M3U format (compatible with many players)
tracks = list(player.queue)
pomice.PlaylistManager.export_to_m3u(
    tracks,
    filepath='playlists/my_playlist.m3u',
    name='My Playlist'
)
```

#### Get Playlist Info
```python
# Get metadata without loading all tracks
info = pomice.PlaylistManager.get_playlist_info('playlists/my_playlist.json')
# Returns: {'name': '...', 'track_count': 42, 'total_duration': 7200000, ...}
```

### JSON Format
```json
{
  "name": "My Playlist",
  "description": "Best songs",
  "created_at": "2024-01-15T12:30:00",
  "track_count": 10,
  "total_duration": 1800000,
  "version": "1.0",
  "tracks": [
    {
      "title": "Song Title",
      "author": "Artist Name",
      "uri": "https://...",
      "identifier": "abc123",
      "length": 180000,
      "thumbnail": "https://...",
      "isrc": "USRC12345678",
      "requester_id": 123456789,
      "requester_name": "User#1234"
    }
  ]
}
```

---

## 🔧 Track Utilities

Advanced filtering, searching, and sorting utilities for tracks.

### TrackFilter

Filter tracks by various criteria.

```python
import pomice

tracks = list(player.queue)

# Filter by duration (milliseconds)
short_tracks = pomice.TrackFilter.by_duration(
    tracks,
    min_duration=60000,   # 1 minute
    max_duration=300000   # 5 minutes
)

# Filter by author
artist_tracks = pomice.TrackFilter.by_author(
    tracks,
    author='Imagine Dragons',
    exact=False  # Case-insensitive contains
)

# Filter by title
title_tracks = pomice.TrackFilter.by_title(
    tracks,
    title='Thunder',
    exact=True  # Exact match
)

# Filter by requester
user_tracks = pomice.TrackFilter.by_requester(tracks, requester_id=123456789)

# Filter by playlist
playlist_tracks = pomice.TrackFilter.by_playlist(tracks, playlist_name='Rock Hits')

# Get only streams
streams = pomice.TrackFilter.streams_only(tracks)

# Get only non-streams
non_streams = pomice.TrackFilter.non_streams_only(tracks)

# Custom filter with lambda
long_tracks = pomice.TrackFilter.custom(
    tracks,
    predicate=lambda t: t.length > 600000  # > 10 minutes
)
```

### SearchHelper

Search, sort, and organize tracks.

```python
import pomice

tracks = list(player.queue)

# Search tracks
results = pomice.SearchHelper.search_tracks(
    tracks,
    query='imagine',
    search_title=True,
    search_author=True,
    case_sensitive=False
)

# Sort by duration
sorted_tracks = pomice.SearchHelper.sort_by_duration(
    tracks,
    reverse=True  # Longest first
)

# Sort by title (alphabetically)
sorted_tracks = pomice.SearchHelper.sort_by_title(tracks)

# Sort by author
sorted_tracks = pomice.SearchHelper.sort_by_author(tracks)

# Remove duplicates
unique_tracks = pomice.SearchHelper.remove_duplicates(
    tracks,
    by_uri=True,  # Remove by URI
    by_title_author=False  # Or by title+author combo
)

# Group by author
grouped = pomice.SearchHelper.group_by_author(tracks)
# Returns: {'Artist Name': [track1, track2, ...], ...}

# Group by playlist
grouped = pomice.SearchHelper.group_by_playlist(tracks)

# Get random tracks
random_tracks = pomice.SearchHelper.get_random_tracks(tracks, count=5)
```

---

## 🎯 Complete Example

See `examples/advanced_features.py` for a complete bot example using all these features.

### Quick Example

```python
import pomice
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.history = pomice.TrackHistory(max_size=100)
    
    @commands.command()
    async def stats(self, ctx):
        """Show queue statistics."""
        player = ctx.voice_client
        stats = pomice.QueueStats(player.queue)
        summary = stats.get_summary()
        
        await ctx.send(
            f"**Queue Stats**\n"
            f"Tracks: {summary['total_tracks']}\n"
            f"Duration: {summary['total_duration_formatted']}\n"
            f"Streams: {summary['stream_count']}"
        )
    
    @commands.command()
    async def export(self, ctx):
        """Export queue to file."""
        player = ctx.voice_client
        pomice.PlaylistManager.export_queue(
            player.queue,
            'my_playlist.json',
            name=f"{ctx.guild.name}'s Queue"
        )
        await ctx.send('✅ Queue exported!')
    
    @commands.command()
    async def filter_long(self, ctx):
        """Show tracks longer than 5 minutes."""
        player = ctx.voice_client
        tracks = list(player.queue)
        
        long_tracks = pomice.TrackFilter.by_duration(
            tracks,
            min_duration=300000  # 5 minutes
        )
        
        await ctx.send(f'Found {len(long_tracks)} long tracks!')
```

---

## 📝 Notes

- All duration values are in **milliseconds**
- History is per-guild (you should maintain separate histories for each guild)
- Exported playlists are in JSON format by default
- M3U export is compatible with most media players
- All utilities work with standard Pomice Track objects

## 🤝 Contributing

Feel free to suggest more features or improvements!

---

**Happy coding! 🎵**
