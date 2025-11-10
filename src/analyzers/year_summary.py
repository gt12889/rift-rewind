"""
Year-end summary generation and analysis.
"""
from typing import Dict, List
from collections import Counter
from datetime import datetime
from src.analyzers.match_analyzer import MatchAnalyzer


class YearSummaryGenerator:
    """Generates year-end summaries and highlights."""
    
    def __init__(self):
        self.analyzer = MatchAnalyzer()
    
    def generate_year_summary(self, matches: List[Dict], puuid: str, year: int = 2024) -> Dict:
        """Generate comprehensive year-end summary."""
        analysis = self.analyzer.analyze_player_matches(matches, puuid)
        
        # Get most played champions
        champion_games = {}
        for match in matches:
            player_data = self.analyzer._extract_player_data(match, puuid)
            if player_data:
                champ = player_data.get("championName", "Unknown")
                champion_games[champ] = champion_games.get(champ, 0) + 1
        
        most_played = sorted(champion_games.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Calculate year statistics
        year_stats = {
            "total_games": analysis.get("total_matches", 0),
            "win_rate": analysis.get("win_rate", {}).get("win_rate", 0),
            "most_played_champions": [{"champion": champ, "games": games} for champ, games in most_played],
            "best_champion": most_played[0][0] if most_played else "N/A",
            "key_metrics": analysis.get("key_metrics", {}),
            "improvement": analysis.get("performance_trends", {}).get("improvement", 0),
            "achievements": analysis.get("achievements", [])
        }
        
        # Generate highlights
        highlights = self._generate_highlights(matches, puuid, analysis)
        
        return {
            "year": year,
            "summary": year_stats,
            "highlights": highlights,
            "strengths": analysis.get("strengths", []),
            "weaknesses": analysis.get("weaknesses", []),
            "growth_areas": self._identify_growth_areas(analysis)
        }
    
    def _generate_highlights(self, matches: List[Dict], puuid: str, analysis: Dict) -> List[Dict]:
        """Generate key highlights from the year."""
        highlights = []
        
        # Best game (by KDA)
        best_game = None
        best_kda = 0
        best_damage_game = None
        best_damage = 0
        
        for match in matches:
            player_data = self.analyzer._extract_player_data(match, puuid)
            if player_data:
                kills = player_data.get("kills", 0)
                deaths = player_data.get("deaths", 0)
                assists = player_data.get("assists", 0)
                kda = (kills + assists) / max(deaths, 1)
                damage = player_data.get("totalDamageDealtToChampions", 0)
                
                if kda > best_kda:
                    best_kda = kda
                    best_game = {
                        "match_id": match.get("metadata", {}).get("matchId", "unknown"),
                        "kda": f"{kills}/{deaths}/{assists}",
                        "champion": player_data.get("championName", "Unknown"),
                        "win": player_data.get("win", False),
                        "damage": damage,
                        "timestamp": match.get("info", {}).get("gameCreation", 0)
                    }
                
                if damage > best_damage:
                    best_damage = damage
                    best_damage_game = {
                        "match_id": match.get("metadata", {}).get("matchId", "unknown"),
                        "damage": damage,
                        "champion": player_data.get("championName", "Unknown"),
                        "kda": f"{kills}/{deaths}/{assists}"
                    }
        
        if best_game:
            highlights.append({
                "type": "Best Performance",
                "description": f"Best KDA game: {best_game['kda']} on {best_game['champion']}",
                "data": best_game
            })
        
        if best_damage_game and best_damage > 40000:
            highlights.append({
                "type": "Damage Dealer",
                "description": f"Highest damage game: {best_damage:,} damage on {best_damage_game['champion']}",
                "data": best_damage_game
            })
        
        # Win streak
        win_streak = 0
        max_streak = 0
        current_streak_start = None
        max_streak_start = None
        
        sorted_matches = sorted(matches, key=lambda m: m.get("info", {}).get("gameCreation", 0))
        for match in sorted_matches:
            player_data = self.analyzer._extract_player_data(match, puuid)
            if player_data:
                if player_data.get("win", False):
                    if win_streak == 0:
                        current_streak_start = match.get("info", {}).get("gameCreation", 0)
                    win_streak += 1
                    if win_streak > max_streak:
                        max_streak = win_streak
                        max_streak_start = current_streak_start
                else:
                    win_streak = 0
                    current_streak_start = None
        
        if max_streak >= 3:
            highlights.append({
                "type": "Win Streak",
                "description": f"Longest win streak: {max_streak} games in a row!",
                "data": {"streak": max_streak, "start_timestamp": max_streak_start}
            })
        
        # Most improved champion
        champion_improvements = self._calculate_champion_improvements(matches, puuid)
        if champion_improvements:
            top_improvement = max(champion_improvements, key=lambda x: x.get("improvement", 0))
            if top_improvement.get("improvement", 0) > 10:
                highlights.append({
                    "type": "Champion Mastery",
                    "description": f"Biggest improvement on {top_improvement['champion']}: +{top_improvement['improvement']:.1f}% win rate",
                    "data": top_improvement
                })
        
        # Perfect games (no deaths with kills/assists)
        perfect_games = self._find_perfect_games(matches, puuid)
        if perfect_games:
            highlights.append({
                "type": "Perfect Game",
                "description": f"{len(perfect_games)} perfect game(s) with 0 deaths!",
                "data": {"count": len(perfect_games), "games": perfect_games[:3]}
            })
        
        # Most played champion milestone
        champion_stats = analysis.get("champion_stats", {})
        if champion_stats:
            most_played = max(champion_stats.items(), key=lambda x: x[1].get("games_played", 0))
            if most_played[1].get("games_played", 0) >= 50:
                highlights.append({
                    "type": "Champion Mastery",
                    "description": f"Played {most_played[0]} {most_played[1]['games_played']} times - true mastery!",
                    "data": {"champion": most_played[0], "games": most_played[1]['games_played']}
                })
        
        # Most improved (overall performance trend)
        trends = analysis.get("performance_trends", {})
        if trends.get("improvement", 0) > 0.5:
            highlights.append({
                "type": "Improvement",
                "description": f"Significant improvement: +{trends.get('improvement', 0):.2f} KDA in recent games",
                "data": {"improvement": trends.get("improvement", 0)}
            })
        
        return highlights[:10]  # Top 10 highlights
    
    def _calculate_champion_improvements(self, matches: List[Dict], puuid: str) -> List[Dict]:
        """Calculate which champions improved most over time."""
        # Split matches into halves
        sorted_matches = sorted(matches, key=lambda m: m.get("info", {}).get("gameCreation", 0))
        first_half = sorted_matches[:len(sorted_matches)//2]
        second_half = sorted_matches[len(sorted_matches)//2:]
        
        # Calculate win rates per champion in each half
        first_half_stats = {}
        second_half_stats = {}
        
        for match in first_half:
            player_data = self.analyzer._extract_player_data(match, puuid)
            if player_data:
                champ = player_data.get("championName", "Unknown")
                if champ not in first_half_stats:
                    first_half_stats[champ] = {"wins": 0, "games": 0}
                first_half_stats[champ]["games"] += 1
                if player_data.get("win", False):
                    first_half_stats[champ]["wins"] += 1
        
        for match in second_half:
            player_data = self.analyzer._extract_player_data(match, puuid)
            if player_data:
                champ = player_data.get("championName", "Unknown")
                if champ not in second_half_stats:
                    second_half_stats[champ] = {"wins": 0, "games": 0}
                second_half_stats[champ]["games"] += 1
                if player_data.get("win", False):
                    second_half_stats[champ]["wins"] += 1
        
        # Calculate improvements
        improvements = []
        for champ in set(list(first_half_stats.keys()) + list(second_half_stats.keys())):
            first_stats = first_half_stats.get(champ, {"wins": 0, "games": 0})
            second_stats = second_half_stats.get(champ, {"wins": 0, "games": 0})
            
            if first_stats["games"] >= 5 and second_stats["games"] >= 5:
                first_wr = (first_stats["wins"] / first_stats["games"]) * 100
                second_wr = (second_stats["wins"] / second_stats["games"]) * 100
                improvement = second_wr - first_wr
                
                if improvement > 0:
                    improvements.append({
                        "champion": champ,
                        "improvement": improvement,
                        "first_half_wr": first_wr,
                        "second_half_wr": second_wr
                    })
        
        return improvements
    
    def _find_perfect_games(self, matches: List[Dict], puuid: str) -> List[Dict]:
        """Find games with 0 deaths and positive KDA."""
        perfect_games = []
        
        for match in matches:
            player_data = self.analyzer._extract_player_data(match, puuid)
            if player_data:
                deaths = player_data.get("deaths", 0)
                kills = player_data.get("kills", 0)
                assists = player_data.get("assists", 0)
                
                if deaths == 0 and (kills > 0 or assists > 0):
                    perfect_games.append({
                        "match_id": match.get("metadata", {}).get("matchId", "unknown"),
                        "kda": f"{kills}/{deaths}/{assists}",
                        "champion": player_data.get("championName", "Unknown"),
                        "win": player_data.get("win", False)
                    })
        
        return perfect_games
    
    def _identify_growth_areas(self, analysis: Dict) -> List[str]:
        """Identify areas for growth in the coming year."""
        growth_areas = []
        
        weaknesses = analysis.get("weaknesses", [])
        if weaknesses:
            growth_areas.extend(weaknesses)
        
        metrics = analysis.get("key_metrics", {})
        if metrics.get("avg_vision_score", 0) < 20:
            growth_areas.append("Improve vision control and map awareness")
        
        if metrics.get("avg_cs", 0) < 150:
            growth_areas.append("Focus on CS farming efficiency")
        
        return growth_areas[:3]

