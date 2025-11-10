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
        
        # Best game
        best_game = None
        best_kda = 0
        for match in matches:
            player_data = self.analyzer._extract_player_data(match, puuid)
            if player_data:
                kills = player_data.get("kills", 0)
                deaths = player_data.get("deaths", 0)
                assists = player_data.get("assists", 0)
                kda = (kills + assists) / max(deaths, 1)
                if kda > best_kda:
                    best_kda = kda
                    best_game = {
                        "match_id": match.get("metadata", {}).get("matchId", "unknown"),
                        "kda": f"{kills}/{deaths}/{assists}",
                        "champion": player_data.get("championName", "Unknown"),
                        "win": player_data.get("win", False)
                    }
        
        if best_game:
            highlights.append({
                "type": "Best Performance",
                "description": f"Best KDA game: {best_game['kda']} on {best_game['champion']}",
                "data": best_game
            })
        
        # Win streak
        win_streak = 0
        max_streak = 0
        for match in sorted(matches, key=lambda m: m.get("info", {}).get("gameCreation", 0)):
            player_data = self.analyzer._extract_player_data(match, puuid)
            if player_data:
                if player_data.get("win", False):
                    win_streak += 1
                    max_streak = max(max_streak, win_streak)
                else:
                    win_streak = 0
        
        if max_streak >= 3:
            highlights.append({
                "type": "Win Streak",
                "description": f"Longest win streak: {max_streak} games",
                "data": {"streak": max_streak}
            })
        
        # Most improved
        trends = analysis.get("performance_trends", {})
        if trends.get("improvement", 0) > 0.5:
            highlights.append({
                "type": "Improvement",
                "description": f"Significant improvement in recent performance",
                "data": {"improvement": trends.get("improvement", 0)}
            })
        
        return highlights
    
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

