"""
Generate shareable social media content.
"""
from typing import Dict, List
from datetime import datetime
import json


class SocialContentGenerator:
    """Generates shareable social media content."""
    
    def generate_year_end_card(self, year_summary: Dict) -> Dict:
        """Generate a shareable year-end card."""
        summary = year_summary.get("summary", {})
        
        card = {
            "title": f"🎮 My {year_summary.get('year', 2024)} League of Legends Recap",
            "stats": {
                "total_games": summary.get("total_games", 0),
                "win_rate": f"{summary.get('win_rate', 0):.1f}%",
                "most_played": summary.get("most_played_champions", [{}])[0].get("champion", "N/A") if summary.get("most_played_champions") else "N/A",
                "best_champion": summary.get("best_champion", "N/A")
            },
            "highlights": [
                highlight.get("description", "") for highlight in year_summary.get("highlights", [])[:3]
            ],
            "achievements": len(year_summary.get("achievements", [])),
            "share_text": self._generate_share_text(year_summary)
        }
        
        return card
    
    def generate_achievement_post(self, achievement: Dict) -> str:
        """Generate social media post for an achievement."""
        post = f"""
🏆 Achievement Unlocked! 🏆

{achievement.get('type', 'Achievement')}

{achievement.get('description', '')}

#LeagueOfLegends #RiftRewind #Gaming
"""
        return post.strip()
    
    def generate_comparison_post(self, player_name: str, friend_name: str, comparison: str) -> str:
        """Generate social media post for player comparison."""
        post = f"""
⚔️ Player Comparison ⚔️

{player_name} vs {friend_name}

{comparison[:200]}...

#LeagueOfLegends #RiftRewind #Gaming
"""
        return post.strip()
    
    def generate_insight_card(self, insights: Dict) -> Dict:
        """Generate shareable insight card."""
        card = {
            "title": "💡 Your League Insights",
            "strengths": insights.get("strengths", [])[:3],
            "improvements": insights.get("weaknesses", [])[:3],
            "recommendations": insights.get("recommendations", [])[:3],
            "share_text": self._generate_insight_share_text(insights)
        }
        
        return card
    
    def _generate_share_text(self, year_summary: Dict) -> str:
        """Generate shareable text for year summary."""
        summary = year_summary.get("summary", {})
        year = year_summary.get("year", 2024)
        
        text = f"""
🎮 My {year} League of Legends Year in Review! 🎮

📊 {summary.get('total_games', 0)} games played
🏆 {summary.get('win_rate', 0):.1f}% win rate
⭐ Most played: {summary.get('best_champion', 'N/A')}

{len(year_summary.get('highlights', []))} amazing highlights this year!

#LeagueOfLegends #RiftRewind #Gaming
"""
        return text.strip()
    
    def _generate_insight_share_text(self, insights: Dict) -> str:
        """Generate shareable text for insights."""
        strengths = insights.get("strengths", [])
        improvements = insights.get("weaknesses", [])
        
        text = "💡 My League Insights:\n\n"
        text += "✨ Strengths:\n"
        for strength in strengths[:3]:
            text += f"• {strength}\n"
        
        text += "\n📈 Areas to Improve:\n"
        for improvement in improvements[:3]:
            text += f"• {improvement}\n"
        
        text += "\n#LeagueOfLegends #RiftRewind #Gaming"
        
        return text.strip()
    
    def generate_twitter_thread(self, year_summary: Dict) -> List[str]:
        """Generate a Twitter thread from year summary."""
        summary = year_summary.get("summary", {})
        year = year_summary.get("year", 2024)
        
        thread = [
            f"🎮 My {year} League of Legends Recap Thread 🧵\n\nLet me break down my year in League!",
            f"📊 Stats:\n• {summary.get('total_games', 0)} games\n• {summary.get('win_rate', 0):.1f}% win rate\n• Most played: {summary.get('best_champion', 'N/A')}",
        ]
        
        # Add highlights
        highlights = year_summary.get("highlights", [])[:3]
        if highlights:
            highlight_text = "🏆 Highlights:\n"
            for i, highlight in enumerate(highlights, 1):
                highlight_text += f"{i}. {highlight.get('description', '')}\n"
            thread.append(highlight_text.strip())
        
        # Add achievements
        achievements = year_summary.get("achievements", [])
        if achievements:
            thread.append(f"✨ {len(achievements)} notable achievements this year!")
        
        thread.append(f"Thanks for an amazing {year}! 🎉\n\n#LeagueOfLegends #RiftRewind")
        
        return thread

