"""
Match data analysis and statistics computation.
"""
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict, Counter
import statistics


class MatchAnalyzer:
    """Analyzes match data to extract insights and statistics."""
    
    def __init__(self):
        self.stats_cache = {}
    
    def analyze_player_matches(self, matches: List[Dict], puuid: str) -> Dict:
        """Comprehensive analysis of player's match history."""
        player_matches = []
        
        for match in matches:
            player_data = self._extract_player_data(match, puuid)
            if player_data:
                player_matches.append({
                    "match": match,
                    "player": player_data
                })
        
        if not player_matches:
            return {}
        
        return {
            "total_matches": len(player_matches),
            "win_rate": self._calculate_win_rate(player_matches),
            "champion_stats": self._analyze_champions(player_matches),
            "role_stats": self._analyze_roles(player_matches),
            "performance_trends": self._analyze_trends(player_matches),
            "key_metrics": self._calculate_key_metrics(player_matches),
            "strengths": self._identify_strengths(player_matches),
            "weaknesses": self._identify_weaknesses(player_matches),
            "achievements": self._identify_achievements(player_matches)
        }
    
    def _extract_player_data(self, match: Dict, puuid: str) -> Optional[Dict]:
        """Extract player-specific data from match."""
        participants = match.get("info", {}).get("participants", [])
        for participant in participants:
            if participant.get("puuid") == puuid:
                return participant
        return None
    
    def _calculate_win_rate(self, player_matches: List[Dict]) -> Dict:
        """Calculate win rate statistics."""
        wins = sum(1 for m in player_matches if m["player"].get("win", False))
        total = len(player_matches)
        
        return {
            "wins": wins,
            "losses": total - wins,
            "win_rate": (wins / total * 100) if total > 0 else 0,
            "total_games": total
        }
    
    def _analyze_champions(self, player_matches: List[Dict]) -> Dict:
        """Analyze champion usage and performance."""
        champion_stats = defaultdict(lambda: {
            "games": 0,
            "wins": 0,
            "kda": [],
            "damage": [],
            "gold": []
        })
        
        for match in player_matches:
            player = match["player"]
            champion = player.get("championName", "Unknown")
            
            stats = champion_stats[champion]
            stats["games"] += 1
            if player.get("win", False):
                stats["wins"] += 1
            
            # KDA calculation
            kills = player.get("kills", 0)
            deaths = player.get("deaths", 0)
            assists = player.get("assists", 0)
            kda = (kills + assists) / max(deaths, 1)
            stats["kda"].append(kda)
            
            stats["damage"].append(player.get("totalDamageDealtToChampions", 0))
            stats["gold"].append(player.get("goldEarned", 0))
        
        # Calculate averages
        champion_summary = {}
        for champ, stats in champion_stats.items():
            champion_summary[champ] = {
                "games_played": stats["games"],
                "win_rate": (stats["wins"] / stats["games"] * 100) if stats["games"] > 0 else 0,
                "avg_kda": statistics.mean(stats["kda"]) if stats["kda"] else 0,
                "avg_damage": statistics.mean(stats["damage"]) if stats["damage"] else 0,
                "avg_gold": statistics.mean(stats["gold"]) if stats["gold"] else 0
            }
        
        return champion_summary
    
    def _analyze_roles(self, player_matches: List[Dict]) -> Dict:
        """Analyze performance by role/lane."""
        role_stats = defaultdict(lambda: {
            "games": 0,
            "wins": 0,
            "kda": []
        })
        
        for match in player_matches:
            player = match["player"]
            role = player.get("teamPosition", "UNKNOWN")
            
            stats = role_stats[role]
            stats["games"] += 1
            if player.get("win", False):
                stats["wins"] += 1
            
            kills = player.get("kills", 0)
            deaths = player.get("deaths", 0)
            assists = player.get("assists", 0)
            kda = (kills + assists) / max(deaths, 1)
            stats["kda"].append(kda)
        
        role_summary = {}
        for role, stats in role_stats.items():
            role_summary[role] = {
                "games_played": stats["games"],
                "win_rate": (stats["wins"] / stats["games"] * 100) if stats["games"] > 0 else 0,
                "avg_kda": statistics.mean(stats["kda"]) if stats["kda"] else 0
            }
        
        return role_summary
    
    def _analyze_trends(self, player_matches: List[Dict]) -> Dict:
        """Analyze performance trends over time."""
        # Sort by match timestamp
        sorted_matches = sorted(
            player_matches,
            key=lambda m: m["match"].get("info", {}).get("gameCreation", 0)
        )
        
        # Calculate rolling averages
        window_size = min(10, len(sorted_matches))
        recent_matches = sorted_matches[-window_size:]
        older_matches = sorted_matches[:-window_size] if len(sorted_matches) > window_size else []
        
        def calculate_avg_kda(matches):
            if not matches:
                return 0
            kdas = []
            for m in matches:
                p = m["player"]
                kills = p.get("kills", 0)
                deaths = p.get("deaths", 0)
                assists = p.get("assists", 0)
                kda = (kills + assists) / max(deaths, 1)
                kdas.append(kda)
            return statistics.mean(kdas)
        
        recent_kda = calculate_avg_kda(recent_matches)
        older_kda = calculate_avg_kda(older_matches)
        
        return {
            "recent_performance": {
                "avg_kda": recent_kda,
                "win_rate": sum(1 for m in recent_matches if m["player"].get("win", False)) / len(recent_matches) * 100 if recent_matches else 0
            },
            "improvement": recent_kda - older_kda if older_matches else 0,
            "trend": "improving" if recent_kda > older_kda else "declining" if older_matches else "stable"
        }
    
    def _calculate_key_metrics(self, player_matches: List[Dict]) -> Dict:
        """Calculate key performance metrics."""
        kdas = []
        damages = []
        golds = []
        vision_scores = []
        cs_scores = []
        
        for match in player_matches:
            player = match["player"]
            kills = player.get("kills", 0)
            deaths = player.get("deaths", 0)
            assists = player.get("assists", 0)
            kda = (kills + assists) / max(deaths, 1)
            kdas.append(kda)
            
            damages.append(player.get("totalDamageDealtToChampions", 0))
            golds.append(player.get("goldEarned", 0))
            vision_scores.append(player.get("visionScore", 0))
            cs_scores.append(player.get("totalMinionsKilled", 0) + player.get("neutralMinionsKilled", 0))
        
        return {
            "avg_kda": statistics.mean(kdas) if kdas else 0,
            "avg_damage": statistics.mean(damages) if damages else 0,
            "avg_gold": statistics.mean(golds) if golds else 0,
            "avg_vision_score": statistics.mean(vision_scores) if vision_scores else 0,
            "avg_cs": statistics.mean(cs_scores) if cs_scores else 0,
            "best_kda": max(kdas) if kdas else 0,
            "best_damage": max(damages) if damages else 0
        }
    
    def _identify_strengths(self, player_matches: List[Dict]) -> List[str]:
        """Identify player strengths."""
        strengths = []
        metrics = self._calculate_key_metrics(player_matches)
        
        if metrics["avg_kda"] > 2.5:
            strengths.append("Strong KDA performance")
        if metrics["avg_vision_score"] > 25:
            strengths.append("Excellent vision control")
        if metrics["avg_damage"] > 20000:
            strengths.append("High damage output")
        
        win_rate = self._calculate_win_rate(player_matches)
        if win_rate["win_rate"] > 55:
            strengths.append("Consistent winning performance")
        
        return strengths[:3]  # Top 3
    
    def _identify_weaknesses(self, player_matches: List[Dict]) -> List[str]:
        """Identify areas for improvement."""
        weaknesses = []
        metrics = self._calculate_key_metrics(player_matches)
        
        if metrics["avg_kda"] < 1.5:
            weaknesses.append("KDA could be improved")
        if metrics["avg_vision_score"] < 15:
            weaknesses.append("Vision control needs work")
        if metrics["avg_cs"] < 150:
            weaknesses.append("CS farming could be better")
        
        win_rate = self._calculate_win_rate(player_matches)
        if win_rate["win_rate"] < 45:
            weaknesses.append("Win rate below average")
        
        return weaknesses[:3]  # Top 3
    
    def _identify_achievements(self, player_matches: List[Dict]) -> List[Dict]:
        """Identify notable achievements."""
        achievements = []
        
        # Perfect KDA games
        for match in player_matches:
            player = match["player"]
            if player.get("deaths", 0) == 0 and player.get("kills", 0) > 0:
                achievements.append({
                    "type": "Perfect KDA",
                    "description": f"{player.get('kills', 0)}/{player.get('assists', 0)} KDA with 0 deaths",
                    "match_id": match["match"].get("metadata", {}).get("matchId", "unknown")
                })
        
        # High damage games
        damages = [m["player"].get("totalDamageDealtToChampions", 0) for m in player_matches]
        if damages:
            max_damage = max(damages)
            if max_damage > 50000:
                achievements.append({
                    "type": "Damage Dealer",
                    "description": f"Dealt {max_damage:,} damage in a single game",
                    "match_id": "unknown"
                })
        
        return achievements[:5]  # Top 5

