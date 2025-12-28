# Pomice Advanced Features Guide

## 🎉 Overview

This guide covers the advanced features added to Pomice to enhance your music bot capabilities. These features include track history, queue statistics, playlist management, and advanced track utilities.

### What's New

- **Track History**: Keep track of previously played songs with navigation and search
- **Queue Statistics**: Detailed analytics about queue contents (duration, requesters, etc.)
- **Playlist Manager**: Export/import playlists to JSON and M3U formats
- **Track Utilities**: Advanced filtering, searching, and sorting capabilities

All features are **fully backward compatible** and **optional** - use what you need!

---

## 📚 Table of Contents

1. [Track History](#-track-history)
2. [Queue Statistics](#-queue-statistics)
3. [Playlist Manager](#-playlist-manager)
4. [Track Utilities](#-track-utilities)
5. [Complete Examples](#-complete-examples)
6. [Quick Reference](#-quick-reference)

---

## 🕐 Track History

Keep track of previously played songs with navigation and search capabilities.

### Features
- Configurable maximum history size
- Navigation (previous/next)
- Search through history
- Filter by requester
- Get unique tracks (remove duplicates)

### Basic Usage

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

### Use Cases
- "What was that song that just played?"
- "Show me the last 10 songs"
- "Play the previous track"
- "Show all songs requested by User X"

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

### Basic Usage

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

### Use Cases
- "How long is the queue?"
- "Who added the most songs?"
- "What's the longest track?"
- "Show me queue statistics"

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

### Export Queue
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

### Import Playlist
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

### Export Track List
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

### Merge Playlists
```python
# Merge multiple playlists into one
pomice.PlaylistManager.merge_playlists(
    filepaths=['playlist1.json', 'playlist2.json', 'playlist3.json'],
    output_path='merged_playlist.json',
    name='Mega Playlist',
    remove_duplicates=True  # Remove duplicate tracks
)
```

### Export to M3U
```python
# Export to M3U format (compatible with many players)
tracks = list(player.queue)
pomice.PlaylistManager.export_to_m3u(
    tracks,
    filepath='playlists/my_playlist.m3u',
    name='My Playlist'
)
```

### Get Playlist Info
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

### Use Cases
- "Save this queue for later"
- "Load my favorite playlist"
- "Merge all my playlists"
- "Export to M3U for my media player"

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

### Use Cases
- "Show me all songs by Artist X"
- "Find tracks between 3-5 minutes"
- "Sort queue by duration"
- "Remove duplicate songs"
- "Play 5 random tracks"

---

## 🎯 Complete Examples

### Example 1: Basic Music Bot with History

```python
import pomice
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.history = pomice.TrackHistory(max_size=100)
    
    @commands.Cog.listener()
    async def on_pomice_track_end(self, player, track, _):
        # Add to history when track ends
        self.history.add(track)
    
    @commands.command()
    async def history(self, ctx, limit: int = 10):
        """Show recently played tracks."""
        recent = self.history.get_last(limit)
        
        tracks_list = '\n'.join(
            f"{i}. {track.title} by {track.author}"
            for i, track in enumerate(recent, 1)
        )
        
        await ctx.send(f"**Recently Played:**\n{tracks_list}")
```

### Example 2: Queue Statistics Command

```python
@commands.command()
async def stats(self, ctx):
    """Show queue statistics."""
    player = ctx.voice_client
    stats = pomice.QueueStats(player.queue)
    summary = stats.get_summary()
    
    embed = discord.Embed(title='📊 Queue Statistics', color=discord.Color.green())
    
    embed.add_field(name='Total Tracks', value=summary['total_tracks'], inline=True)
    embed.add_field(name='Total Duration', value=summary['total_duration_formatted'], inline=True)
    embed.add_field(name='Average Duration', value=summary['average_duration_formatted'], inline=True)
    
    if summary['longest_track']:
        embed.add_field(
            name='Longest Track',
            value=f"{summary['longest_track'].title} ({stats.format_duration(summary['longest_track'].length)})",
            inline=False
        )
    
    # Top requesters
    top_requesters = stats.get_top_requesters(3)
    if top_requesters:
        requesters_text = '\n'.join(
            f'{i}. {req.display_name}: {count} tracks'
            for i, (req, count) in enumerate(top_requesters, 1)
        )
        embed.add_field(name='Top Requesters', value=requesters_text, inline=False)
    
    await ctx.send(embed=embed)
```

### Example 3: Export/Import Playlists

```python
@commands.command()
async def export(self, ctx, filename: str = 'playlist.json'):
    """Export current queue to a file."""
    player = ctx.voice_client
    
    pomice.PlaylistManager.export_queue(
        player.queue,
        f'playlists/{filename}',
        name=f"{ctx.guild.name}'s Playlist",
        description=f'Exported from {ctx.guild.name}'
    )
    await ctx.send(f'✅ Queue exported to `playlists/{filename}`')

@commands.command()
async def import_playlist(self, ctx, filename: str):
    """Import a playlist from a file."""
    player = ctx.voice_client
    
    data = pomice.PlaylistManager.import_playlist(f'playlists/{filename}')
    uris = [track['uri'] for track in data['tracks'] if track.get('uri')]
    
    added = 0
    for uri in uris:
        results = await player.get_tracks(query=uri, ctx=ctx)
        if results:
            await player.queue.put(results[0])
            added += 1
    
    await ctx.send(f'✅ Imported {added} tracks from `{data["name"]}`')
```

### Example 4: Filter and Sort Queue

```python
@commands.command()
async def filter_short(self, ctx):
    """Show tracks shorter than 3 minutes."""
    player = ctx.voice_client
    tracks = list(player.queue)
    
    short_tracks = pomice.TrackFilter.by_duration(
        tracks,
        max_duration=180000  # 3 minutes in ms
    )
    
    await ctx.send(f'Found {len(short_tracks)} tracks under 3 minutes!')

@commands.command()
async def sort_queue(self, ctx, sort_by: str = 'duration'):
    """Sort the queue by duration, title, or author."""
    player = ctx.voice_client
    queue_tracks = list(player.queue)
    
    if sort_by == 'duration':
        sorted_tracks = pomice.SearchHelper.sort_by_duration(queue_tracks)
    elif sort_by == 'title':
        sorted_tracks = pomice.SearchHelper.sort_by_title(queue_tracks)
    elif sort_by == 'author':
        sorted_tracks = pomice.SearchHelper.sort_by_author(queue_tracks)
    else:
        return await ctx.send('Valid options: duration, title, author')
    
    # Clear and refill queue
    player.queue._queue.clear()
    for track in sorted_tracks:
        await player.queue.put(track)
    
    await ctx.send(f'✅ Queue sorted by {sort_by}')
```

---

## 📖 Quick Reference

### Track History
```python
history = pomice.TrackHistory(max_size=100)
history.add(track)
recent = history.get_last(10)
results = history.search("query")
previous = history.get_previous()
unique = history.get_unique_tracks()
```

### Queue Statistics
```python
stats = pomice.QueueStats(queue)
total = stats.total_duration
formatted = stats.format_duration(total)
top_users = stats.get_top_requesters(5)
summary = stats.get_summary()
```

### Playlist Manager
```python
# Export
pomice.PlaylistManager.export_queue(queue, 'playlist.json')

# Import
data = pomice.PlaylistManager.import_playlist('playlist.json')

# Merge
pomice.PlaylistManager.merge_playlists(['p1.json', 'p2.json'], 'merged.json')

# M3U
pomice.PlaylistManager.export_to_m3u(tracks, 'playlist.m3u')
```

### Track Utilities
```python
# Filter
short = pomice.TrackFilter.by_duration(tracks, max_duration=180000)
artist = pomice.TrackFilter.by_author(tracks, "Artist Name")

# Search & Sort
results = pomice.SearchHelper.search_tracks(tracks, "query")
sorted_tracks = pomice.SearchHelper.sort_by_duration(tracks)
unique = pomice.SearchHelper.remove_duplicates(tracks)
random = pomice.SearchHelper.get_random_tracks(tracks, 5)
```

---

## 📝 Notes

- All duration values are in **milliseconds**
- History should be maintained per-guild
- Exported playlists are in JSON format by default
- M3U export is compatible with most media players
- All utilities work with standard Pomice Track objects

---

## 🚀 Getting Started

1. **Import the features you need**:
   ```python
   import pomice
   ```

2. **Use them in your commands**:
   ```python
   history = pomice.TrackHistory()
   stats = pomice.QueueStats(player.queue)
   ```

3. **Check the examples** in `examples/advanced_features.py` for a complete bot

4. **Experiment** and customize to fit your needs!

---

## 🎓 Additional Resources

- **Full Example Bot**: See `examples/advanced_features.py`
- **Main Documentation**: See the main Pomice README
- **Discord Support**: Join the Pomice Discord server

---

**Happy coding! 🎵**
