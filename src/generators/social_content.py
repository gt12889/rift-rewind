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
    
    def generate_instagram_story(self, year_summary: Dict) -> Dict:
        """Generate Instagram story format content."""
        summary = year_summary.get("summary", {})
        year = year_summary.get("year", 2024)
        
        story = {
            "slides": [
                {
                    "type": "title",
                    "text": f"🎮 {year} League Recap",
                    "emoji": "🎮"
                },
                {
                    "type": "stats",
                    "text": f"📊 {summary.get('total_games', 0)} Games",
                    "subtext": f"{summary.get('win_rate', 0):.1f}% Win Rate"
                },
                {
                    "type": "champion",
                    "text": f"⭐ {summary.get('best_champion', 'N/A')}",
                    "subtext": "Most Played Champion"
                }
            ]
        }
        
        # Add highlight slides
        highlights = year_summary.get("highlights", [])[:3]
        for highlight in highlights:
            story["slides"].append({
                "type": "highlight",
                "text": highlight.get("type", "Highlight"),
                "subtext": highlight.get("description", "")[:50]
            })
        
        return story
    
    def generate_shareable_moment(self, moment_data: Dict, moment_type: str = "achievement") -> Dict:
        """Generate a shareable moment card for social media."""
        if moment_type == "achievement":
            return {
                "title": "🏆 Achievement Unlocked!",
                "content": moment_data.get("description", ""),
                "image_text": f"{moment_data.get('type', 'Achievement')}\n{moment_data.get('description', '')}",
                "hashtags": "#LeagueOfLegends #RiftRewind #Gaming #Achievement",
                "share_text": f"🏆 Just unlocked: {moment_data.get('type', 'Achievement')}! {moment_data.get('description', '')} #LeagueOfLegends #RiftRewind"
            }
        elif moment_type == "highlight":
            return {
                "title": "⭐ Epic Moment!",
                "content": moment_data.get("description", ""),
                "image_text": f"⭐ {moment_data.get('type', 'Highlight')}\n{moment_data.get('description', '')}",
                "hashtags": "#LeagueOfLegends #RiftRewind #Gaming #EpicPlay",
                "share_text": f"⭐ {moment_data.get('description', '')} #LeagueOfLegends #RiftRewind"
            }
        else:
            return {
                "title": "🎮 League Moment",
                "content": moment_data.get("description", ""),
                "hashtags": "#LeagueOfLegends #RiftRewind #Gaming"
            }
    
    def generate_comparison_card(self, player1_name: str, player2_name: str, 
                                comparison_data: Dict) -> Dict:
        """Generate a visual comparison card for two players."""
        return {
            "title": f"⚔️ {player1_name} vs {player2_name}",
            "player1": {
                "name": player1_name,
                "stats": comparison_data.get("player1", {}).get("stats", {})
            },
            "player2": {
                "name": player2_name,
                "stats": comparison_data.get("player2", {}).get("stats", {})
            },
            "comparison": comparison_data.get("comparison", ""),
            "complementarity": comparison_data.get("complementarity", {}),
            "share_text": f"⚔️ {player1_name} vs {player2_name}\n\n{comparison_data.get('comparison', '')[:200]}...\n\n#LeagueOfLegends #RiftRewind #Comparison",
            "hashtags": "#LeagueOfLegends #RiftRewind #Gaming #PlayerComparison"
        }
    
    def generate_progress_card(self, progress_data: Dict) -> Dict:
        """Generate a progress tracking card."""
        return {
            "title": "📈 Your Progress",
            "time_period": progress_data.get("time_period", "month"),
            "persistent_strengths": progress_data.get("persistent_strengths", [])[:3],
            "persistent_weaknesses": progress_data.get("persistent_weaknesses", [])[:3],
            "improvements": progress_data.get("improvements", []),
            "overall_trend": progress_data.get("summary", {}).get("overall_trend", "stable"),
            "key_insights": progress_data.get("summary", {}).get("key_insights", [])[:3],
            "share_text": self._generate_progress_share_text(progress_data),
            "hashtags": "#LeagueOfLegends #RiftRewind #Gaming #Progress"
        }
    
    def _generate_progress_share_text(self, progress_data: Dict) -> str:
        """Generate shareable text for progress tracking."""
        summary = progress_data.get("summary", {})
        trend = summary.get("overall_trend", "stable")
        
        text = f"📈 My League Progress Update!\n\n"
        text += f"Overall Trend: {trend.title()}\n\n"
        
        strengths = progress_data.get("persistent_strengths", [])[:2]
        if strengths:
            text += "✨ Consistent Strengths:\n"
            for strength in strengths:
                text += f"• {strength.get('pattern', '')}\n"
        
        improvements = progress_data.get("improvements", [])
        if improvements:
            text += f"\n🚀 Made {len(improvements)} improvement(s)!\n"
        
        text += "\n#LeagueOfLegends #RiftRewind #Progress"
        return text

