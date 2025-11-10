"""
Weekly summary generator with highlights and signature moves.
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import statistics


class WeeklySummaryGenerator:
    """Generates condensed weekly summaries, highlights, and signature moves."""
    
    def __init__(self):
        pass
    
    def generate_weekly_summary(self, matches: List[Dict], puuid: str, days: int = 7) -> Dict:
        """Generate a condensed weekly summary."""
        # Filter matches from the last N days
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_timestamp = cutoff_date.timestamp() * 1000
        
        recent_matches = []
        for match in matches:
            game_creation = match.get("info", {}).get("gameCreation", 0)
            if game_creation >= cutoff_timestamp:
                recent_matches.append(match)
        
        if not recent_matches:
            return {
                "summary_30_seconds": "No matches played this week.",
                "total_games": 0,
                "highlights": [],
                "signature_moves": []
            }
        
        # Extract player data
        player_matches = []
        for match in recent_matches:
            player_data = self._extract_player_data(match, puuid)
            if player_data:
                player_matches.append({
                    "match": match,
                    "player": player_data
                })
        
        # Generate 30-second summary
        summary_30_seconds = self._generate_30_second_summary(player_matches)
        
        # Generate highlight reel
        highlights = self._generate_highlight_reel(player_matches)
        
        # Identify signature moves
        signature_moves = self._identify_signature_moves(player_matches)
        
        return {
            "summary_30_seconds": summary_30_seconds,
            "total_games": len(player_matches),
            "highlights": highlights,
            "signature_moves": signature_moves,
            "week_stats": self._calculate_week_stats(player_matches)
        }
    
    def _generate_30_second_summary(self, player_matches: List[Dict]) -> str:
        """Generate a condensed 30-second summary of the week."""
        if not player_matches:
            return "No matches this week."
        
        total_games = len(player_matches)
        wins = sum(1 for m in player_matches if m["player"].get("win", False))
        win_rate = (wins / total_games * 100) if total_games > 0 else 0
        
        # Calculate average KDA
        kdas = []
        for m in player_matches:
            p = m["player"]
            kills = p.get("kills", 0)
            deaths = p.get("deaths", 0)
            assists = p.get("assists", 0)
            kda = (kills + assists) / max(deaths, 1)
            kdas.append(kda)
        avg_kda = statistics.mean(kdas) if kdas else 0
        
        # Most played champion
        champion_counts = Counter()
        for m in player_matches:
            champ = m["player"].get("championName", "Unknown")
            champion_counts[champ] += 1
        most_played = champion_counts.most_common(1)[0][0] if champion_counts else "Unknown"
        
        # Best performance
        best_kda = max(kdas) if kdas else 0
        best_match = None
        for m in player_matches:
            p = m["player"]
            kills = p.get("kills", 0)
            deaths = p.get("deaths", 0)
            assists = p.get("assists", 0)
            kda = (kills + assists) / max(deaths, 1)
            if kda == best_kda:
                best_match = {
                    "champion": p.get("championName", "Unknown"),
                    "kda": f"{kills}/{deaths}/{assists}",
                    "win": p.get("win", False)
                }
                break
        
        # Build summary
        summary_parts = [
            f"Played {total_games} games this week",
            f"with a {win_rate:.1f}% win rate",
            f"averaging {avg_kda:.2f} KDA",
            f"Most played: {most_played}"
        ]
        
        if best_match:
            result = "W" if best_match["win"] else "L"
            summary_parts.append(f"Best game: {best_match['kda']} on {best_match['champion']} ({result})")
        
        return ". ".join(summary_parts) + "."
    
    def _generate_highlight_reel(self, player_matches: List[Dict]) -> List[Dict]:
        """Generate text-based highlight moments."""
        highlights = []
        
        # Sort by game creation time (most recent first)
        sorted_matches = sorted(
            player_matches,
            key=lambda m: m["match"].get("info", {}).get("gameCreation", 0),
            reverse=True
        )
        
        # 1. Best KDA game
        best_kda = 0
        best_kda_match = None
        for m in player_matches:
            p = m["player"]
            kills = p.get("kills", 0)
            deaths = p.get("deaths", 0)
            assists = p.get("assists", 0)
            kda = (kills + assists) / max(deaths, 0.5)  # Avoid division by zero
            if kda > best_kda:
                best_kda = kda
                best_kda_match = m
        
        if best_kda_match and best_kda >= 3.0:
            p = best_kda_match["player"]
            champ = p.get("championName", "Unknown")
            result = "Victory" if p.get("win", False) else "Defeat"
            highlights.append({
                "type": "Best Performance",
                "moment": f"{p.get('kills', 0)}/{p.get('deaths', 0)}/{p.get('assists', 0)} KDA on {champ}",
                "description": f"Dominant {result.lower()} with {best_kda:.2f} KDA",
                "champion": champ
            })
        
        # 2. Highest damage game
        max_damage = 0
        max_damage_match = None
        for m in player_matches:
            p = m["player"]
            damage = p.get("totalDamageDealtToChampions", 0)
            if damage > max_damage:
                max_damage = damage
                max_damage_match = m
        
        if max_damage_match and max_damage >= 20000:
            p = max_damage_match["player"]
            champ = p.get("championName", "Unknown")
            highlights.append({
                "type": "Damage Dealer",
                "moment": f"{max_damage:,} damage dealt",
                "description": f"Carried the game on {champ} with massive damage output",
                "champion": champ
            })
        
        # 3. Perfect KDA (no deaths)
        for m in sorted_matches[:5]:  # Check recent 5 games
            p = m["player"]
            deaths = p.get("deaths", 0)
            if deaths == 0 and p.get("kills", 0) + p.get("assists", 0) > 0:
                champ = p.get("championName", "Unknown")
                kills = p.get("kills", 0)
                assists = p.get("assists", 0)
                highlights.append({
                    "type": "Perfect Game",
                    "moment": f"{kills}/{deaths}/{assists} KDA",
                    "description": f"Deathless game on {champ} - flawless execution",
                    "champion": champ
                })
                break
        
        # 4. Win streak
        win_streak = 0
        for m in sorted_matches:
            if m["player"].get("win", False):
                win_streak += 1
            else:
                break
        
        if win_streak >= 3:
            highlights.append({
                "type": "Win Streak",
                "moment": f"{win_streak} consecutive wins",
                "description": f"On fire! {win_streak} wins in a row",
                "champion": None
            })
        
        # 5. Comeback victory (low early, high late)
        for m in sorted_matches[:3]:
            p = m["player"]
            if p.get("win", False):
                gold_earned = p.get("goldEarned", 0)
                damage = p.get("totalDamageDealtToChampions", 0)
                # High damage relative to gold suggests comeback
                if gold_earned > 0 and (damage / gold_earned) > 2.5:
                    champ = p.get("championName", "Unknown")
                    highlights.append({
                        "type": "Comeback",
                        "moment": "Efficient damage output",
                        "description": f"Clutch performance on {champ} - made every gold count",
                        "champion": champ
                    })
                    break
        
        return highlights[:5]  # Return top 5 highlights
    
    def _identify_signature_moves(self, player_matches: List[Dict]) -> List[Dict]:
        """Identify what the player does best (signature moves)."""
        signature_moves = []
        
        if not player_matches:
            return signature_moves
        
        # Calculate averages
        total_damage = 0
        total_gold = 0
        total_vision = 0
        total_kills = 0
        total_assists = 0
        total_deaths = 0
        total_cs = 0
        total_minutes = 0
        
        for m in player_matches:
            p = m["player"]
            total_damage += p.get("totalDamageDealtToChampions", 0)
            total_gold += p.get("goldEarned", 0)
            total_vision += p.get("visionScore", 0)
            total_kills += p.get("kills", 0)
            total_assists += p.get("assists", 0)
            total_deaths += p.get("deaths", 0)
            total_cs += p.get("totalMinionsKilled", 0) + p.get("neutralMinionsKilled", 0)
            
            game_duration = m["match"].get("info", {}).get("gameDuration", 0)
            total_minutes += game_duration / 60.0 if game_duration > 0 else 1
        
        num_games = len(player_matches)
        avg_damage = total_damage / num_games if num_games > 0 else 0
        avg_gold = total_gold / num_games if num_games > 0 else 0
        avg_vision = total_vision / num_games if num_games > 0 else 0
        avg_kills = total_kills / num_games if num_games > 0 else 0
        avg_assists = total_assists / num_games if num_games > 0 else 0
        avg_deaths = total_deaths / num_games if num_games > 0 else 0
        avg_cs_per_min = (total_cs / total_minutes) if total_minutes > 0 else 0
        
        # Identify strengths
        # 1. High damage dealer
        if avg_damage >= 20000:
            signature_moves.append({
                "move": "Damage Dealer",
                "description": f"Averaging {avg_damage:,.0f} damage per game - you're the team's primary damage source",
                "stat": f"{avg_damage:,.0f} avg damage",
                "icon": "💥"
            })
        
        # 2. Vision control
        if avg_vision >= 50:
            signature_moves.append({
                "move": "Vision Master",
                "description": f"{avg_vision:.1f} vision score per game - you control the map",
                "stat": f"{avg_vision:.1f} avg vision",
                "icon": "👁️"
            })
        
        # 3. Farming machine
        if avg_cs_per_min >= 8.0:
            signature_moves.append({
                "move": "CS King",
                "description": f"{avg_cs_per_min:.1f} CS/min - exceptional farming skills",
                "stat": f"{avg_cs_per_min:.1f} CS/min",
                "icon": "🌾"
            })
        
        # 4. Playmaker (high assists)
        if avg_assists >= 8:
            signature_moves.append({
                "move": "Playmaker",
                "description": f"{avg_assists:.1f} assists per game - you set up your team for success",
                "stat": f"{avg_assists:.1f} avg assists",
                "icon": "🎯"
            })
        
        # 5. Cleanup crew (high kills, low deaths)
        if avg_kills >= 6 and avg_deaths <= 3:
            signature_moves.append({
                "move": "Cleanup Specialist",
                "description": f"{avg_kills:.1f} kills, {avg_deaths:.1f} deaths - you secure kills while staying safe",
                "stat": f"{avg_kills:.1f}K/{avg_deaths:.1f}D",
                "icon": "⚔️"
            })
        
        # 6. Gold efficiency
        if avg_gold > 0 and (avg_damage / avg_gold) > 2.0:
            signature_moves.append({
                "move": "Gold Efficient",
                "description": "You maximize damage output relative to gold earned - very efficient playstyle",
                "stat": f"{avg_damage/avg_gold:.2f} damage/gold",
                "icon": "💰"
            })
        
        # 7. Consistent performer (low variance in KDA)
        kdas = []
        for m in player_matches:
            p = m["player"]
            kills = p.get("kills", 0)
            deaths = p.get("deaths", 0)
            assists = p.get("assists", 0)
            kda = (kills + assists) / max(deaths, 1)
            kdas.append(kda)
        
        if len(kdas) >= 5:
            kda_variance = statistics.stdev(kdas) if len(kdas) > 1 else 0
            avg_kda = statistics.mean(kdas)
            if kda_variance < 0.5 and avg_kda >= 2.0:
                signature_moves.append({
                    "move": "Consistent Performer",
                    "description": f"Reliable {avg_kda:.2f} KDA with low variance - you're steady and dependable",
                    "stat": f"{avg_kda:.2f} avg KDA",
                    "icon": "📊"
                })
        
        return signature_moves[:5]  # Return top 5 signature moves
    
    def _calculate_week_stats(self, player_matches: List[Dict]) -> Dict:
        """Calculate weekly statistics."""
        if not player_matches:
            return {}
        
        wins = sum(1 for m in player_matches if m["player"].get("win", False))
        total = len(player_matches)
        
        kdas = []
        for m in player_matches:
            p = m["player"]
            kills = p.get("kills", 0)
            deaths = p.get("deaths", 0)
            assists = p.get("assists", 0)
            kda = (kills + assists) / max(deaths, 1)
            kdas.append(kda)
        
        return {
            "total_games": total,
            "wins": wins,
            "losses": total - wins,
            "win_rate": (wins / total * 100) if total > 0 else 0,
            "avg_kda": statistics.mean(kdas) if kdas else 0,
            "best_kda": max(kdas) if kdas else 0
        }
    
    def _extract_player_data(self, match: Dict, puuid: str) -> Optional[Dict]:
        """Extract player-specific data from match."""
        participants = match.get("info", {}).get("participants", [])
        for participant in participants:
            if participant.get("puuid") == puuid:
                return participant
        return None

