"""
Rank-based comparison metrics for player statistics.
"""
from typing import Dict, List, Optional
import math


class RankComparisonAnalyzer:
    """Compares player stats against rank/ELO averages."""
    
    # Average stats by rank tier (based on community data)
    # These are approximate averages from League of Legends community statistics
    RANK_AVERAGES = {
        "IRON": {
            "kda": 1.2,
            "cs_per_min": 5.5,
            "win_rate": 50.0
        },
        "BRONZE": {
            "kda": 1.4,
            "cs_per_min": 6.0,
            "win_rate": 50.0
        },
        "SILVER": {
            "kda": 1.6,
            "cs_per_min": 6.5,
            "win_rate": 50.0
        },
        "GOLD": {
            "kda": 1.8,
            "cs_per_min": 7.0,
            "win_rate": 50.0
        },
        "PLATINUM": {
            "kda": 2.0,
            "cs_per_min": 7.5,
            "win_rate": 50.0
        },
        "EMERALD": {
            "kda": 2.2,
            "cs_per_min": 8.0,
            "win_rate": 50.0
        },
        "DIAMOND": {
            "kda": 2.4,
            "cs_per_min": 8.5,
            "win_rate": 50.0
        },
        "MASTER": {
            "kda": 2.6,
            "cs_per_min": 9.0,
            "win_rate": 50.0
        },
        "GRANDMASTER": {
            "kda": 2.8,
            "cs_per_min": 9.5,
            "win_rate": 50.0
        },
        "CHALLENGER": {
            "kda": 3.0,
            "cs_per_min": 10.0,
            "win_rate": 50.0
        }
    }
    
    # Champion-specific average win rates (approximate, varies by rank)
    CHAMPION_AVERAGE_WIN_RATES = {
        "Jinx": 50.5,
        "Ashe": 50.2,
        "Caitlyn": 50.8,
        "Vayne": 49.8,
        "Ezreal": 50.1,
        "Lucian": 50.3,
        "Jhin": 50.6,
        "Kai'Sa": 50.4,
        "Varus": 50.0,
        "Tristana": 50.2,
        # Add more champions as needed
    }
    
    def __init__(self):
        pass
    
    def get_rank_averages(self, tier: str) -> Dict:
        """Get average stats for a given rank tier."""
        tier_upper = tier.upper() if tier else "GOLD"
        return self.RANK_AVERAGES.get(tier_upper, self.RANK_AVERAGES["GOLD"])
    
    def compare_kda(self, player_kda: float, rank_tier: str) -> Dict:
        """Compare player KDA vs rank average."""
        rank_avg = self.get_rank_averages(rank_tier)
        avg_kda = rank_avg["kda"]
        
        difference = player_kda - avg_kda
        percentage_diff = (difference / avg_kda * 100) if avg_kda > 0 else 0
        
        return {
            "player_kda": round(player_kda, 2),
            "rank_average": round(avg_kda, 2),
            "difference": round(difference, 2),
            "percentage_diff": round(percentage_diff, 1),
            "status": "above" if difference > 0 else "below" if difference < 0 else "equal"
        }
    
    def compare_cs_per_min(self, player_cs_per_min: float, rank_tier: str) -> Dict:
        """Compare player CS/min vs rank average."""
        rank_avg = self.get_rank_averages(rank_tier)
        avg_cs = rank_avg["cs_per_min"]
        
        difference = player_cs_per_min - avg_cs
        percentage_diff = (difference / avg_cs * 100) if avg_cs > 0 else 0
        
        return {
            "player_cs_per_min": round(player_cs_per_min, 2),
            "rank_average": round(avg_cs, 2),
            "difference": round(difference, 2),
            "percentage_diff": round(percentage_diff, 1),
            "status": "above" if difference > 0 else "below" if difference < 0 else "equal"
        }
    
    def compare_champion_win_rate(self, player_win_rate: float, champion_name: str, rank_tier: str) -> Dict:
        """Compare player win rate on a champion vs average for that champion in their ELO."""
        # Get base champion average
        champ_avg = self.CHAMPION_AVERAGE_WIN_RATES.get(champion_name, 50.0)
        
        # Adjust slightly based on rank (higher ranks tend to have slightly better win rates)
        rank_adjustment = {
            "IRON": -1.0,
            "BRONZE": -0.5,
            "SILVER": 0.0,
            "GOLD": 0.0,
            "PLATINUM": 0.5,
            "EMERALD": 0.5,
            "DIAMOND": 1.0,
            "MASTER": 1.5,
            "GRANDMASTER": 2.0,
            "CHALLENGER": 2.5
        }
        tier_upper = rank_tier.upper() if rank_tier else "GOLD"
        adjustment = rank_adjustment.get(tier_upper, 0.0)
        adjusted_avg = champ_avg + adjustment
        
        difference = player_win_rate - adjusted_avg
        percentage_diff = (difference / adjusted_avg * 100) if adjusted_avg > 0 else 0
        
        return {
            "player_win_rate": round(player_win_rate, 1),
            "champion_average": round(adjusted_avg, 1),
            "difference": round(difference, 1),
            "percentage_diff": round(percentage_diff, 1),
            "status": "above" if difference > 0 else "below" if difference < 0 else "equal",
            "champion": champion_name
        }
    
    def calculate_player_cs_per_min(self, matches: List[Dict], puuid: str) -> float:
        """Calculate average CS per minute for a player."""
        total_cs = 0
        total_minutes = 0
        
        for match in matches:
            player_data = self._extract_player_data(match, puuid)
            if player_data:
                cs = player_data.get("totalMinionsKilled", 0) + player_data.get("neutralMinionsKilled", 0)
                game_duration = match.get("info", {}).get("gameDuration", 0)  # in seconds
                minutes = game_duration / 60.0 if game_duration > 0 else 1
                
                total_cs += cs
                total_minutes += minutes
        
        return (total_cs / total_minutes) if total_minutes > 0 else 0.0
    
    def _extract_player_data(self, match: Dict, puuid: str) -> Optional[Dict]:
        """Extract player-specific data from match."""
        participants = match.get("info", {}).get("participants", [])
        for participant in participants:
            if participant.get("puuid") == puuid:
                return participant
        return None
    
    def get_champion_win_rate(self, matches: List[Dict], puuid: str, champion_name: str) -> Optional[float]:
        """Get win rate for a specific champion."""
        champion_matches = []
        wins = 0
        
        for match in matches:
            player_data = self._extract_player_data(match, puuid)
            if player_data and player_data.get("championName") == champion_name:
                champion_matches.append(player_data)
                if player_data.get("win", False):
                    wins += 1
        
        if len(champion_matches) == 0:
            return None
        
        return (wins / len(champion_matches)) * 100.0
    
    def get_most_played_champion(self, matches: List[Dict], puuid: str) -> Optional[str]:
        """Get the most played champion from matches."""
        champion_counts = {}
        
        for match in matches:
            player_data = self._extract_player_data(match, puuid)
            if player_data:
                champ = player_data.get("championName")
                if champ:
                    champion_counts[champ] = champion_counts.get(champ, 0) + 1
        
        if not champion_counts:
            return None
        
        return max(champion_counts.items(), key=lambda x: x[1])[0]

