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
    
    def generate_phase_performance_heatmap(self, matches: List[Dict], puuid: str) -> str:
        """Generate heatmap of performance by game phase (early/mid/late)."""
        # Categorize games by phase based on duration
        phase_data = {
            "early": {"kda": [], "win_rate": [], "damage": [], "gold": []},
            "mid": {"kda": [], "win_rate": [], "damage": [], "gold": []},
            "late": {"kda": [], "win_rate": [], "damage": [], "gold": []}
        }
        
        for match in matches:
            player_data = self._extract_player_data(match, puuid)
            if not player_data:
                continue
            
            # Get game duration in minutes
            game_duration_sec = match.get("info", {}).get("gameDuration", 0)
            game_duration_min = game_duration_sec / 60
            
            # Determine phase
            if game_duration_min <= 15:
                phase = "early"
            elif game_duration_min <= 30:
                phase = "mid"
            else:
                phase = "late"
            
            # Extract metrics
            kda = self._calculate_kda(player_data)
            win = 1 if player_data.get("win", False) else 0
            damage = player_data.get("totalDamageDealtToChampions", 0)
            gold = player_data.get("goldEarned", 0)
            
            phase_data[phase]["kda"].append(kda)
            phase_data[phase]["win_rate"].append(win)
            phase_data[phase]["damage"].append(damage)
            phase_data[phase]["gold"].append(gold)
        
        # Calculate averages for each phase
        phases = ["early", "mid", "late"]
        metrics = ["KDA", "Win Rate", "Damage", "Gold"]
        
        heatmap_data = []
        for phase in phases:
            if phase_data[phase]["kda"]:
                avg_kda = sum(phase_data[phase]["kda"]) / len(phase_data[phase]["kda"])
                avg_win_rate = (sum(phase_data[phase]["win_rate"]) / len(phase_data[phase]["win_rate"])) * 100
                avg_damage = sum(phase_data[phase]["damage"]) / len(phase_data[phase]["damage"])
                avg_gold = sum(phase_data[phase]["gold"]) / len(phase_data[phase]["gold"])
                
                # Normalize values for heatmap (0-100 scale)
                # For KDA: assume max is 5, normalize to 0-100
                # For win rate: already 0-100
                # For damage: normalize assuming max 50000
                # For gold: normalize assuming max 20000
                normalized_kda = min(avg_kda / 5.0 * 100, 100)
                normalized_damage = min(avg_damage / 50000.0 * 100, 100)
                normalized_gold = min(avg_gold / 20000.0 * 100, 100)
                
                heatmap_data.append([normalized_kda, avg_win_rate, normalized_damage, normalized_gold])
            else:
                heatmap_data.append([0, 0, 0, 0])
        
        if not any(any(row) for row in heatmap_data):
            return None
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=metrics,
            y=["Early Game", "Mid Game", "Late Game"],
            colorscale='RdYlGn',
            text=[[f"{heatmap_data[i][j]:.1f}" for j in range(4)] for i in range(3)],
            texttemplate="%{text}",
            textfont={"size": 10, "color": "white"},
            colorbar=dict(title="Performance Score"),
            hovertemplate='Phase: %{y}<br>Metric: %{x}<br>Score: %{z:.1f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Performance by Game Phase',
            xaxis_title='Metric',
            yaxis_title='Game Phase',
            template='plotly_dark',
            height=400
        )
        
        return self._fig_to_base64(fig)
    
    def generate_win_rate_trend_line(self, matches: List[Dict], puuid: str) -> str:
        """Generate win rate trend line over time."""
        match_data = []
        for match in sorted(matches, key=lambda m: m.get("info", {}).get("gameCreation", 0)):
            player_data = self._extract_player_data(match, puuid)
            if player_data:
                match_data.append({
                    "date": match.get("info", {}).get("gameCreation", 0),
                    "win": 1 if player_data.get("win", False) else 0
                })
        
        if not match_data:
            return None
        
        df = pd.DataFrame(match_data)
        df['date'] = pd.to_datetime(df['date'], unit='ms')
        
        # Calculate cumulative win rate
        df['wins'] = df['win'].cumsum()
        df['games'] = range(1, len(df) + 1)
        df['cumulative_win_rate'] = (df['wins'] / df['games']) * 100
        
        # Calculate rolling win rate (10-game window)
        df['rolling_win_rate'] = df['win'].rolling(window=min(10, len(df)), min_periods=1).mean() * 100
        
        fig = go.Figure()
        
        # Add cumulative win rate line
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['cumulative_win_rate'],
            mode='lines',
            name='Cumulative Win Rate',
            line=dict(color='#4CAF50', width=2, dash='solid')
        ))
        
        # Add rolling win rate line
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['rolling_win_rate'],
            mode='lines',
            name='10-Game Rolling Win Rate',
            line=dict(color='#2196F3', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title='Win Rate Trend Over Time',
            xaxis_title='Date',
            yaxis_title='Win Rate (%)',
            template='plotly_dark',
            height=400,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return self._fig_to_base64(fig)
    
    def generate_champion_radar_chart(self, matches: List[Dict], puuid: str) -> str:
        """Generate radar chart for champion performance."""
        # Group matches by champion
        champion_data = {}
        
        for match in matches:
            player_data = self._extract_player_data(match, puuid)
            if not player_data:
                continue
            
            champion = player_data.get("championName", "Unknown")
            if champion not in champion_data:
                champion_data[champion] = {
                    "kda": [],
                    "win_rate": [],
                    "damage": [],
                    "gold": [],
                    "cs": [],
                    "vision": []
                }
            
            # Extract metrics
            kda = self._calculate_kda(player_data)
            win = 1 if player_data.get("win", False) else 0
            damage = player_data.get("totalDamageDealtToChampions", 0)
            gold = player_data.get("goldEarned", 0)
            cs = player_data.get("totalMinionsKilled", 0) + player_data.get("neutralMinionsKilled", 0)
            vision = player_data.get("visionScore", 0)
            
            champion_data[champion]["kda"].append(kda)
            champion_data[champion]["win_rate"].append(win)
            champion_data[champion]["damage"].append(damage)
            champion_data[champion]["gold"].append(gold)
            champion_data[champion]["cs"].append(cs)
            champion_data[champion]["vision"].append(vision)
        
        # Get top 5 champions by games played
        sorted_champions = sorted(
            champion_data.items(),
            key=lambda x: len(x[1]["kda"]),
            reverse=True
        )[:5]
        
        if not sorted_champions:
            return None
        
        # Create radar chart for each champion
        fig = go.Figure()
        
        categories = ['KDA', 'Win Rate', 'Damage', 'Gold', 'CS', 'Vision']
        
        # Normalize metrics to 0-100 scale for radar chart
        max_values = {
            "kda": 5.0,
            "win_rate": 1.0,
            "damage": 50000.0,
            "gold": 20000.0,
            "cs": 300.0,
            "vision": 100.0
        }
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        
        for idx, (champion, data) in enumerate(sorted_champions):
            if not data["kda"]:
                continue
            
            # Calculate averages
            avg_kda = sum(data["kda"]) / len(data["kda"])
            avg_win_rate = (sum(data["win_rate"]) / len(data["win_rate"])) * 100
            avg_damage = sum(data["damage"]) / len(data["damage"])
            avg_gold = sum(data["gold"]) / len(data["gold"])
            avg_cs = sum(data["cs"]) / len(data["cs"])
            avg_vision = sum(data["vision"]) / len(data["vision"])
            
            # Normalize to 0-100
            normalized_values = [
                min(avg_kda / max_values["kda"] * 100, 100),
                avg_win_rate,  # Already 0-100
                min(avg_damage / max_values["damage"] * 100, 100),
                min(avg_gold / max_values["gold"] * 100, 100),
                min(avg_cs / max_values["cs"] * 100, 100),
                min(avg_vision / max_values["vision"] * 100, 100)
            ]
            
            # Close the radar chart by repeating first value
            normalized_values.append(normalized_values[0])
            radar_categories = categories + [categories[0]]
            
            fig.add_trace(go.Scatterpolar(
                r=normalized_values,
                theta=radar_categories,
                fill='toself',
                name=champion,
                line=dict(color=colors[idx % len(colors)], width=2)
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title='Champion Performance Radar Chart (Top 5)',
            template='plotly_dark',
            height=400
        )
        
        return self._fig_to_base64(fig)
    
    def _fig_to_base64(self, fig) -> str:
        """Convert plotly figure to base64 string."""
        try:
            img_bytes = fig.to_image(format="png", width=800, height=400)
            return base64.b64encode(img_bytes).decode('utf-8')
        except Exception as e:
            print(f"Error converting figure to base64: {e}")
            # Return empty string if conversion fails
            return ""

