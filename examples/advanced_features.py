"""
Example usage of Pomice's new advanced features.

This example demonstrates:
- Track History
- Queue Statistics
- Playlist Export/Import
- Track Filtering and Search
"""
import asyncio

import discord
from discord.ext import commands

import pomice

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


class AdvancedMusic(commands.Cog):
    """Music cog with advanced features."""

    def __init__(self, bot):
        self.bot = bot
        self.pomice = pomice.NodePool()

        # Track history for each guild
        self.track_histories = {}

    async def start_nodes(self):
        """Start Lavalink nodes."""
        await self.pomice.create_node(
            bot=self.bot,
            host="127.0.0.1",
            port="3030",
            password="youshallnotpass",
            identifier="MAIN",
        )

    @commands.Cog.listener()
    async def on_pomice_track_end(self, player, track, _):
        """Add track to history when it ends."""
        if player.guild.id not in self.track_histories:
            self.track_histories[player.guild.id] = pomice.TrackHistory(max_size=100)

        self.track_histories[player.guild.id].add(track)

    @commands.command(name="play")
    async def play(self, ctx, *, search: str):
        """Play a track."""
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect(cls=pomice.Player)

        player = ctx.voice_client
        results = await player.get_tracks(query=search, ctx=ctx)

        if not results:
            return await ctx.send("No results found.")

        if isinstance(results, pomice.Playlist):
            await player.queue.put(results.tracks)
            await ctx.send(f"Added playlist **{results.name}** with {len(results.tracks)} tracks.")
        else:
            track = results[0]
            await player.queue.put(track)
            await ctx.send(f"Added **{track.title}** to queue.")

        if not player.is_playing:
            await player.do_next()

    @commands.command(name="history")
    async def history(self, ctx, limit: int = 10):
        """Show recently played tracks."""
        if ctx.guild.id not in self.track_histories:
            return await ctx.send("No history available.")

        history = self.track_histories[ctx.guild.id]

        if history.is_empty:
            return await ctx.send("No tracks in history.")

        tracks = history.get_last(limit)

        embed = discord.Embed(title="🎵 Recently Played", color=discord.Color.blue())

        for i, track in enumerate(tracks, 1):
            embed.add_field(name=f"{i}. {track.title}", value=f"by {track.author}", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="stats")
    async def queue_stats(self, ctx):
        """Show detailed queue statistics."""
        if not ctx.voice_client:
            return await ctx.send("Not connected to voice.")

        player = ctx.voice_client
        stats = pomice.QueueStats(player.queue)
        summary = stats.get_summary()

        embed = discord.Embed(title="📊 Queue Statistics", color=discord.Color.green())

        embed.add_field(name="Total Tracks", value=summary["total_tracks"], inline=True)
        embed.add_field(
            name="Total Duration", value=summary["total_duration_formatted"], inline=True,
        )
        embed.add_field(
            name="Average Duration", value=summary["average_duration_formatted"], inline=True,
        )

        if summary["longest_track"]:
            embed.add_field(
                name="Longest Track",
                value=f"{summary['longest_track'].title} ({stats.format_duration(summary['longest_track'].length)})",
                inline=False,
            )

        # Duration breakdown
        breakdown = summary["duration_breakdown"]
        embed.add_field(
            name="Duration Breakdown",
            value=f"Short (<3min): {breakdown['short']}\n"
            f"Medium (3-6min): {breakdown['medium']}\n"
            f"Long (6-10min): {breakdown['long']}\n"
            f"Very Long (>10min): {breakdown['very_long']}",
            inline=False,
        )

        # Top requesters
        top_requesters = stats.get_top_requesters(3)
        if top_requesters:
            requesters_text = "\n".join(
                f"{i}. {req.display_name}: {count} tracks"
                for i, (req, count) in enumerate(top_requesters, 1)
            )
            embed.add_field(name="Top Requesters", value=requesters_text, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="export")
    async def export_queue(self, ctx, filename: str = "playlist.json"):
        """Export current queue to a file."""
        if not ctx.voice_client:
            return await ctx.send("Not connected to voice.")

        player = ctx.voice_client

        if player.queue.is_empty:
            return await ctx.send("Queue is empty.")

        try:
            pomice.PlaylistManager.export_queue(
                player.queue,
                f"playlists/{filename}",
                name=f"{ctx.guild.name}'s Playlist",
                description=f"Exported from {ctx.guild.name}",
            )
            await ctx.send(f"✅ Queue exported to `playlists/{filename}`")
        except Exception as e:
            await ctx.send(f"❌ Error exporting queue: {e}")

    @commands.command(name="import")
    async def import_playlist(self, ctx, filename: str):
        """Import a playlist from a file."""
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect(cls=pomice.Player)

        player = ctx.voice_client

        try:
            data = pomice.PlaylistManager.import_playlist(f"playlists/{filename}")

            # Get URIs and search for tracks
            uris = [track["uri"] for track in data["tracks"] if track.get("uri")]

            added = 0
            for uri in uris:
                try:
                    results = await player.get_tracks(query=uri, ctx=ctx)
                    if results:
                        if isinstance(results, pomice.Playlist):
                            await player.queue.put(results.tracks)
                            added += len(results.tracks)
                        else:
                            await player.queue.put(results[0])
                            added += 1
                except:
                    continue

            await ctx.send(f'✅ Imported {added} tracks from `{data["name"]}`')

            if not player.is_playing:
                await player.do_next()

        except FileNotFoundError:
            await ctx.send(f"❌ Playlist file `{filename}` not found.")
        except Exception as e:
            await ctx.send(f"❌ Error importing playlist: {e}")

    @commands.command(name="filter")
    async def filter_queue(self, ctx, filter_type: str, *, value: str):
        """Filter queue by various criteria.

        Examples:
        !filter author Imagine Dragons
        !filter duration 180000-300000 (3-5 minutes in ms)
        !filter title Thunder
        """
        if not ctx.voice_client:
            return await ctx.send("Not connected to voice.")

        player = ctx.voice_client
        queue_tracks = list(player.queue)

        if filter_type == "author":
            filtered = pomice.TrackFilter.by_author(queue_tracks, value)
        elif filter_type == "title":
            filtered = pomice.TrackFilter.by_title(queue_tracks, value)
        elif filter_type == "duration":
            # Parse duration range (e.g., "180000-300000")
            if "-" in value:
                min_dur, max_dur = map(int, value.split("-"))
                filtered = pomice.TrackFilter.by_duration(
                    queue_tracks, min_duration=min_dur, max_duration=max_dur,
                )
            else:
                return await ctx.send("Duration format: min-max (in milliseconds)")
        else:
            return await ctx.send("Valid filters: author, title, duration")

        if not filtered:
            return await ctx.send("No tracks match the filter.")

        embed = discord.Embed(
            title=f"🔍 Filtered Results ({len(filtered)} tracks)", color=discord.Color.purple(),
        )

        for i, track in enumerate(filtered[:10], 1):
            stats = pomice.QueueStats(player.queue)
            embed.add_field(
                name=f"{i}. {track.title}",
                value=f"by {track.author} - {stats.format_duration(track.length)}",
                inline=False,
            )

        if len(filtered) > 10:
            embed.set_footer(text=f"Showing 10 of {len(filtered)} results")

        await ctx.send(embed=embed)

    @commands.command(name="search_history")
    async def search_history(self, ctx, *, query: str):
        """Search through play history."""
        if ctx.guild.id not in self.track_histories:
            return await ctx.send("No history available.")

        history = self.track_histories[ctx.guild.id]
        results = history.search(query)

        if not results:
            return await ctx.send(f'No tracks found matching "{query}"')

        embed = discord.Embed(
            title=f'🔍 History Search: "{query}"',
            description=f"Found {len(results)} tracks",
            color=discord.Color.gold(),
        )

        for i, track in enumerate(results[:10], 1):
            embed.add_field(name=f"{i}. {track.title}", value=f"by {track.author}", inline=False)

        if len(results) > 10:
            embed.set_footer(text=f"Showing 10 of {len(results)} results")

        await ctx.send(embed=embed)

    @commands.command(name="sort")
    async def sort_queue(self, ctx, sort_by: str = "duration"):
        """Sort the queue.

        Options: duration, title, author
        """
        if not ctx.voice_client:
            return await ctx.send("Not connected to voice.")

        player = ctx.voice_client

        if player.queue.is_empty:
            return await ctx.send("Queue is empty.")

        queue_tracks = list(player.queue)

        if sort_by == "duration":
            sorted_tracks = pomice.SearchHelper.sort_by_duration(queue_tracks)
        elif sort_by == "title":
            sorted_tracks = pomice.SearchHelper.sort_by_title(queue_tracks)
        elif sort_by == "author":
            sorted_tracks = pomice.SearchHelper.sort_by_author(queue_tracks)
        else:
            return await ctx.send("Valid options: duration, title, author")

        # Clear and refill queue
        player.queue._queue.clear()
        for track in sorted_tracks:
            await player.queue.put(track)

        await ctx.send(f"✅ Queue sorted by {sort_by}")


@bot.event
async def on_ready():
    print(f"{bot.user} is ready!")
    await bot.get_cog("AdvancedMusic").start_nodes()


# Add cog
bot.add_cog(AdvancedMusic(bot))

# Run bot
bot.run("YOUR_BOT_TOKEN")
