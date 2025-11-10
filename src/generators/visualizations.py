"""
Generate visualizations for player statistics and trends.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import base64
from io import BytesIO
import pandas as pd


class VisualizationGenerator:
    """Generates visualizations for player data."""
    
    def __init__(self):
        sns.set_style("darkgrid")
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def generate_win_rate_chart(self, matches: List[Dict], puuid: str) -> str:
        """Generate win rate over time chart."""
        # Extract win/loss data over time
        match_data = []
        for match in sorted(matches, key=lambda m: m.get("info", {}).get("gameCreation", 0)):
            player_data = self._extract_player_data(match, puuid)
            if player_data:
                match_data.append({
                    "date": match.get("info", {}).get("gameCreation", 0),
                    "win": 1 if player_data.get("win", False) else 0,
                    "kda": self._calculate_kda(player_data)
                })
        
        if not match_data:
            return None
        
        df = pd.DataFrame(match_data)
        df['date'] = pd.to_datetime(df['date'], unit='ms')
        df['win_rate_rolling'] = df['win'].rolling(window=10, min_periods=1).mean() * 100
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['win_rate_rolling'],
            mode='lines',
            name='Win Rate (10-game rolling)',
            line=dict(color='#4CAF50', width=2)
        ))
        
        fig.update_layout(
            title='Win Rate Over Time',
            xaxis_title='Date',
            yaxis_title='Win Rate (%)',
            template='plotly_dark',
            height=400
        )
        
        return self._fig_to_base64(fig)
    
    def generate_champion_performance(self, champion_stats: Dict) -> str:
        """Generate champion performance visualization."""
        if not champion_stats:
            return None
        
        # Get top 10 champions by games played
        sorted_champs = sorted(
            champion_stats.items(),
            key=lambda x: x[1].get("games_played", 0),
            reverse=True
        )[:10]
        
        champions = [champ for champ, _ in sorted_champs]
        win_rates = [stats.get("win_rate", 0) for _, stats in sorted_champs]
        games = [stats.get("games_played", 0) for _, stats in sorted_champs]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=champions,
            y=win_rates,
            name='Win Rate',
            marker_color='#2196F3',
            text=[f"{wr:.1f}%" for wr in win_rates],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Champion Performance (Top 10 by Games Played)',
            xaxis_title='Champion',
            yaxis_title='Win Rate (%)',
            template='plotly_dark',
            height=400
        )
        
        return self._fig_to_base64(fig)
    
    def generate_kda_trend(self, matches: List[Dict], puuid: str) -> str:
        """Generate KDA trend over time."""
        match_data = []
        for match in sorted(matches, key=lambda m: m.get("info", {}).get("gameCreation", 0)):
            player_data = self._extract_player_data(match, puuid)
            if player_data:
                match_data.append({
                    "date": match.get("info", {}).get("gameCreation", 0),
                    "kda": self._calculate_kda(player_data),
                    "kills": player_data.get("kills", 0),
                    "deaths": player_data.get("deaths", 0),
                    "assists": player_data.get("assists", 0)
                })
        
        if not match_data:
            return None
        
        df = pd.DataFrame(match_data)
        df['date'] = pd.to_datetime(df['date'], unit='ms')
        df['kda_rolling'] = df['kda'].rolling(window=10, min_periods=1).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['kda_rolling'],
            mode='lines',
            name='KDA (10-game rolling average)',
            line=dict(color='#FF9800', width=2)
        ))
        
        fig.update_layout(
            title='KDA Trend Over Time',
            xaxis_title='Date',
            yaxis_title='KDA',
            template='plotly_dark',
            height=400
        )
        
        return self._fig_to_base64(fig)
    
    def generate_role_performance(self, role_stats: Dict) -> str:
        """Generate role performance comparison."""
        if not role_stats:
            return None
        
        roles = list(role_stats.keys())
        win_rates = [role_stats[role].get("win_rate", 0) for role in roles]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=roles,
            y=win_rates,
            marker_color='#9C27B0',
            text=[f"{wr:.1f}%" for wr in win_rates],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Performance by Role',
            xaxis_title='Role',
            yaxis_title='Win Rate (%)',
            template='plotly_dark',
            height=400
        )
        
        return self._fig_to_base64(fig)
    
    def _extract_player_data(self, match: Dict, puuid: str):
        """Extract player data from match."""
        participants = match.get("info", {}).get("participants", [])
        for participant in participants:
            if participant.get("puuid") == puuid:
                return participant
        return None
    
    def _calculate_kda(self, player_data: Dict) -> float:
        """Calculate KDA ratio."""
        kills = player_data.get("kills", 0)
        deaths = player_data.get("deaths", 0)
        assists = player_data.get("assists", 0)
        return (kills + assists) / max(deaths, 1)
    
    def _fig_to_base64(self, fig) -> str:
        """Convert plotly figure to base64 string."""
        try:
            img_bytes = fig.to_image(format="png", width=800, height=400)
            return base64.b64encode(img_bytes).decode('utf-8')
        except Exception as e:
            print(f"Error converting figure to base64: {e}")
            # Return empty string if conversion fails
            return ""

