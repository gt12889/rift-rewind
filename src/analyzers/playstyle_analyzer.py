"""
Analyze player playstyles for social comparisons and complement detection.
"""
from typing import Dict, List, Optional
from collections import defaultdict, Counter
import statistics
from src.analyzers.match_analyzer import MatchAnalyzer


class PlaystyleAnalyzer:
    """Analyzes player playstyles for comparison and complement detection."""
    
    def __init__(self):
        self.match_analyzer = MatchAnalyzer()
    
    def analyze_playstyle(self, matches: List[Dict], puuid: str) -> Dict:
        """
        Analyze a player's playstyle characteristics.
        
        Returns:
            Dict with playstyle attributes, preferences, and characteristics
        """
        player_matches = []
        for match in matches:
            player_data = self.match_analyzer._extract_player_data(match, puuid)
            if player_data:
                player_matches.append({
                    "match": match,
                    "player": player_data
                })
        
        if not player_matches:
            return {}
        
        # Analyze playstyle dimensions
        aggression = self._analyze_aggression(player_matches)
        objective_focus = self._analyze_objective_focus(player_matches)
        team_play = self._analyze_team_play(player_matches)
        scaling = self._analyze_scaling_preference(player_matches)
        role_preference = self._analyze_role_preference(player_matches)
        champion_diversity = self._analyze_champion_diversity(player_matches)
        
        # Identify playstyle archetype
        archetype = self._identify_archetype(
            aggression, objective_focus, team_play, scaling
        )
        
        # Calculate playstyle vector (normalized scores)
        playstyle_vector = {
            "aggression": aggression["score"],
            "objective_focus": objective_focus["score"],
            "team_play": team_play["score"],
            "scaling": scaling["score"],
            "consistency": self._calculate_consistency(player_matches)
        }
        
        return {
            "playstyle": {
                "archetype": archetype,
                "vector": playstyle_vector,
                "aggression": aggression,
                "objective_focus": objective_focus,
                "team_play": team_play,
                "scaling": scaling,
                "role_preference": role_preference,
                "champion_diversity": champion_diversity
            },
            "strengths": self._identify_playstyle_strengths(
                aggression, objective_focus, team_play, scaling
            ),
            "complementary_styles": self._identify_complementary_styles(playstyle_vector),
            "preferred_teammates": self._suggest_teammate_types(playstyle_vector)
        }
    
    def _analyze_aggression(self, player_matches: List[Dict]) -> Dict:
        """Analyze player aggression level."""
        kill_participation_rates = []
        early_kills = []
        deaths = []
        
        for match_data in player_matches:
            player = match_data["player"]
            team_id = player.get("teamId", 0)
            
            # Calculate kill participation
            kills = player.get("kills", 0)
            assists = player.get("assists", 0)
            
            # Get team total kills
            team_kills = 0
            participants = match_data["match"].get("info", {}).get("participants", [])
            for p in participants:
                if p.get("teamId") == team_id:
                    team_kills += p.get("kills", 0)
            
            if team_kills > 0:
                kp = ((kills + assists) / team_kills) * 100
                kill_participation_rates.append(kp)
            
            # Early game aggression (first 15 minutes proxy - using first blood)
            first_blood = player.get("firstBloodKill", False) or player.get("firstBloodAssist", False)
            if first_blood:
                early_kills.append(1)
            else:
                early_kills.append(0)
            
            deaths.append(player.get("deaths", 0))
        
        avg_kp = statistics.mean(kill_participation_rates) if kill_participation_rates else 50
        early_aggro = statistics.mean(early_kills) * 100 if early_kills else 0
        avg_deaths = statistics.mean(deaths) if deaths else 5
        
        # Score: 0-100 (higher = more aggressive)
        # High KP, high early aggression, moderate deaths = aggressive
        # Low KP, low early aggression, low deaths = passive
        score = min(100, max(0, (
            (avg_kp - 40) * 1.5 +  # KP contribution
            early_aggro * 0.5 +     # Early game presence
            (avg_deaths - 3) * 10   # Willingness to take risks
        )))
        
        return {
            "score": score,
            "avg_kill_participation": avg_kp,
            "early_aggression_rate": early_aggro,
            "avg_deaths": avg_deaths,
            "level": "aggressive" if score > 60 else "passive" if score < 40 else "balanced"
        }
    
    def _analyze_objective_focus(self, player_matches: List[Dict]) -> Dict:
        """Analyze player's focus on objectives."""
        dragon_kills = []
        baron_kills = []
        turret_damage = []
        
        for match_data in player_matches:
            player = match_data["player"]
            
            dragon_kills.append(player.get("dragonKills", 0))
            baron_kills.append(player.get("baronKills", 0))
            turret_damage.append(player.get("damageDealtToTurrets", 0))
        
        avg_dragons = statistics.mean(dragon_kills) if dragon_kills else 0
        avg_barons = statistics.mean(baron_kills) if baron_kills else 0
        avg_turret_damage = statistics.mean(turret_damage) if turret_damage else 0
        
        # Score: 0-100 (higher = more objective-focused)
        # Normalize: dragons (0-2 avg), barons (0-1 avg), turret damage (0-10000 avg)
        score = min(100, max(0, (
            (avg_dragons / 2.0) * 30 +
            (avg_barons / 1.0) * 40 +
            min(avg_turret_damage / 10000.0, 1.0) * 30
        ) * 100))
        
        return {
            "score": score,
            "avg_dragon_kills": avg_dragons,
            "avg_baron_kills": avg_barons,
            "avg_turret_damage": avg_turret_damage,
            "level": "objective_focused" if score > 60 else "kill_focused" if score < 40 else "balanced"
        }
    
    def _analyze_team_play(self, player_matches: List[Dict]) -> Dict:
        """Analyze player's team play tendency."""
        assists = []
        vision_scores = []
        team_fight_participation = []
        
        for match_data in player_matches:
            player = match_data["player"]
            
            assists.append(player.get("assists", 0))
            vision_scores.append(player.get("visionScore", 0))
            
            # Team fight participation (proxy: high assist games)
            kills = player.get("kills", 0)
            assists_count = player.get("assists", 0)
            if kills + assists_count > 10:
                team_fight_participation.append(1)
            else:
                team_fight_participation.append(0)
        
        avg_assists = statistics.mean(assists) if assists else 5
        avg_vision = statistics.mean(vision_scores) if vision_scores else 20
        team_fight_rate = statistics.mean(team_fight_participation) * 100 if team_fight_participation else 0
        
        # Score: 0-100 (higher = more team-oriented)
        score = min(100, max(0, (
            (avg_assists / 10.0) * 40 +
            (avg_vision / 50.0) * 30 +
            (team_fight_rate / 100.0) * 30
        ) * 100))
        
        return {
            "score": score,
            "avg_assists": avg_assists,
            "avg_vision_score": avg_vision,
            "team_fight_participation_rate": team_fight_rate,
            "level": "team_player" if score > 60 else "solo_carry" if score < 40 else "balanced"
        }
    
    def _analyze_scaling_preference(self, player_matches: List[Dict]) -> Dict:
        """Analyze preference for scaling vs early game champions."""
        # This is a proxy based on game duration and performance
        # Players who perform better in longer games may prefer scaling
        
        game_durations = []
        late_game_performance = []
        
        for match_data in player_matches:
            player = match_data["player"]
            match_info = match_data["match"].get("info", {})
            
            duration_sec = match_info.get("gameDuration", 0)
            duration_min = duration_sec / 60.0
            game_durations.append(duration_min)
            
            # Late game performance (damage in long games)
            if duration_min > 30:
                damage = player.get("totalDamageDealtToChampions", 0)
                late_game_performance.append(damage)
        
        avg_duration = statistics.mean(game_durations) if game_durations else 25
        avg_late_damage = statistics.mean(late_game_performance) if late_game_performance else 0
        
        # Score: 0-100 (higher = prefers scaling)
        # Players with longer games and good late game damage = scaling preference
        duration_score = min(100, (avg_duration / 40.0) * 50)
        late_damage_score = min(50, (avg_late_damage / 40000.0) * 50) if avg_late_damage > 0 else 25
        
        score = duration_score + late_damage_score
        
        return {
            "score": score,
            "avg_game_duration": avg_duration,
            "avg_late_game_damage": avg_late_damage,
            "level": "scaling" if score > 60 else "early_game" if score < 40 else "balanced"
        }
    
    def _analyze_role_preference(self, player_matches: List[Dict]) -> Dict:
        """Analyze preferred roles."""
        role_counts = Counter()
        
        for match_data in player_matches:
            player = match_data["player"]
            role = player.get("teamPosition", "UNKNOWN")
            if role != "UNKNOWN":
                role_counts[role] += 1
        
        total = sum(role_counts.values())
        if total == 0:
            return {"preferred_role": "UNKNOWN", "role_distribution": {}}
        
        role_distribution = {
            role: (count / total) * 100
            for role, count in role_counts.items()
        }
        
        preferred_role = role_counts.most_common(1)[0][0] if role_counts else "UNKNOWN"
        
        return {
            "preferred_role": preferred_role,
            "role_distribution": role_distribution,
            "flexibility": 100 - (role_counts.most_common(1)[0][1] / total * 100) if role_counts else 0
        }
    
    def _analyze_champion_diversity(self, player_matches: List[Dict]) -> Dict:
        """Analyze champion pool diversity."""
        champion_counts = Counter()
        
        for match_data in player_matches:
            player = match_data["player"]
            champion = player.get("championName", "Unknown")
            champion_counts[champion] += 1
        
        total_games = sum(champion_counts.values())
        unique_champions = len(champion_counts)
        
        if total_games == 0:
            return {"diversity_score": 0, "unique_champions": 0, "most_played": []}
        
        # Diversity score: 0-100 (higher = more diverse)
        # Perfect diversity would be playing a different champion every game
        diversity_score = min(100, (unique_champions / total_games) * 100)
        
        most_played = [
            {"champion": champ, "games": count, "percentage": (count / total_games) * 100}
            for champ, count in champion_counts.most_common(5)
        ]
        
        return {
            "diversity_score": diversity_score,
            "unique_champions": unique_champions,
            "total_games": total_games,
            "most_played": most_played,
            "level": "diverse" if diversity_score > 70 else "specialist" if diversity_score < 30 else "balanced"
        }
    
    def _identify_archetype(self, aggression: Dict, objective_focus: Dict,
                           team_play: Dict, scaling: Dict) -> str:
        """Identify playstyle archetype based on dimensions."""
        agg_score = aggression["score"]
        obj_score = objective_focus["score"]
        team_score = team_play["score"]
        scale_score = scaling["score"]
        
        # Determine primary archetype
        if agg_score > 70 and obj_score < 40:
            return "Aggressive Carry"
        elif obj_score > 70 and team_score > 60:
            return "Objective Controller"
        elif team_score > 70 and agg_score < 40:
            return "Supportive Team Player"
        elif scale_score > 70:
            return "Late Game Specialist"
        elif agg_score > 60 and obj_score > 60:
            return "All-Rounder"
        elif team_score > 60 and obj_score > 60:
            return "Strategic Leader"
        else:
            return "Balanced Player"
    
    def _calculate_consistency(self, player_matches: List[Dict]) -> float:
        """Calculate performance consistency."""
        kdas = []
        
        for match_data in player_matches:
            player = match_data["player"]
            kills = player.get("kills", 0)
            deaths = player.get("deaths", 0)
            assists = player.get("assists", 0)
            kda = (kills + assists) / max(deaths, 1)
            kdas.append(kda)
        
        if not kdas:
            return 0
        
        # Consistency = inverse of coefficient of variation
        mean_kda = statistics.mean(kdas)
        if mean_kda == 0:
            return 0
        
        try:
            std_kda = statistics.stdev(kdas)
            cv = std_kda / mean_kda  # Coefficient of variation
            consistency = max(0, min(100, (1 - min(cv, 1)) * 100))
            return consistency
        except:
            return 50  # Default if calculation fails
    
    def _identify_playstyle_strengths(self, aggression: Dict, objective_focus: Dict,
                                     team_play: Dict, scaling: Dict) -> List[str]:
        """Identify strengths based on playstyle."""
        strengths = []
        
        if aggression["score"] > 70:
            strengths.append("Strong early game presence and aggression")
        if objective_focus["score"] > 70:
            strengths.append("Excellent objective control and map awareness")
        if team_play["score"] > 70:
            strengths.append("Great team coordination and support")
        if scaling["score"] > 70:
            strengths.append("Strong late game performance and scaling")
        
        return strengths
    
    def _identify_complementary_styles(self, playstyle_vector: Dict) -> List[str]:
        """Identify playstyles that complement this player."""
        complementary = []
        
        # If aggressive, complement with objective-focused players
        if playstyle_vector["aggression"] > 60:
            complementary.append("Objective-focused players who can secure objectives while you create pressure")
        
        # If objective-focused, complement with aggressive players
        if playstyle_vector["objective_focus"] > 60:
            complementary.append("Aggressive players who can create space for objective control")
        
        # If team-oriented, complement with carries
        if playstyle_vector["team_play"] > 60:
            complementary.append("Carry players who can benefit from your team support")
        
        # If scaling-focused, complement with early game players
        if playstyle_vector["scaling"] > 60:
            complementary.append("Early game players who can hold the game until you scale")
        
        # If solo-focused, complement with team players
        if playstyle_vector["team_play"] < 40:
            complementary.append("Team-oriented players who can support your solo plays")
        
        if not complementary:
            complementary.append("Balanced players who can adapt to your playstyle")
        
        return complementary
    
    def _suggest_teammate_types(self, playstyle_vector: Dict) -> List[Dict]:
        """Suggest types of teammates that would work well."""
        suggestions = []
        
        # High aggression -> needs objective control
        if playstyle_vector["aggression"] > 60:
            suggestions.append({
                "type": "Objective Controller",
                "reason": "Can secure objectives while you create pressure in lanes"
            })
        
        # Low team play -> needs team-oriented support
        if playstyle_vector["team_play"] < 40:
            suggestions.append({
                "type": "Supportive Team Player",
                "reason": "Can provide vision and team coordination to enable your plays"
            })
        
        # High scaling -> needs early game presence
        if playstyle_vector["scaling"] > 60:
            suggestions.append({
                "type": "Early Game Specialist",
                "reason": "Can maintain early game pressure while you scale into late game"
            })
        
        # High objective focus -> needs aggressive pressure
        if playstyle_vector["objective_focus"] > 60:
            suggestions.append({
                "type": "Aggressive Laner",
                "reason": "Can create lane pressure that opens up objective opportunities"
            })
        
        if not suggestions:
            suggestions.append({
                "type": "Flexible Player",
                "reason": "Can adapt to various team compositions and strategies"
            })
        
        return suggestions
    
    def compare_playstyles(self, player1_playstyle: Dict, player2_playstyle: Dict) -> Dict:
        """Compare two players' playstyles."""
        p1_vector = player1_playstyle.get("playstyle", {}).get("vector", {})
        p2_vector = player2_playstyle.get("playstyle", {}).get("vector", {})
        
        # Calculate complementarity score
        complementarity = self._calculate_complementarity(p1_vector, p2_vector)
        
        # Find similarities and differences
        similarities = []
        differences = []
        
        for key in ["aggression", "objective_focus", "team_play", "scaling"]:
            p1_val = p1_vector.get(key, 50)
            p2_val = p2_vector.get(key, 50)
            
            diff = abs(p1_val - p2_val)
            if diff < 20:
                similarities.append({
                    "dimension": key,
                    "player1_score": p1_val,
                    "player2_score": p2_val
                })
            else:
                differences.append({
                    "dimension": key,
                    "player1_score": p1_val,
                    "player2_score": p2_val,
                    "difference": diff
                })
        
        return {
            "complementarity_score": complementarity,
            "complementarity_level": "high" if complementarity > 70 else "moderate" if complementarity > 50 else "low",
            "similarities": similarities,
            "differences": differences,
            "synergy_analysis": self._analyze_synergy(p1_vector, p2_vector),
            "recommendations": self._generate_comparison_recommendations(
                p1_vector, p2_vector, complementarity
            )
        }
    
    def _calculate_complementarity(self, vector1: Dict, vector2: Dict) -> float:
        """Calculate how well two playstyles complement each other."""
        # Complementarity: players who fill each other's gaps
        # High aggression + High objective focus = complementary
        # High team play + Low team play = complementary (one supports, one carries)
        # High scaling + Low scaling = complementary (one early, one late)
        
        complementarity_score = 0
        
        # Aggression + Objective Focus complementarity
        agg1 = vector1.get("aggression", 50)
        obj1 = vector1.get("objective_focus", 50)
        agg2 = vector2.get("aggression", 50)
        obj2 = vector2.get("objective_focus", 50)
        
        # If one is aggressive and other is objective-focused, that's complementary
        if (agg1 > 60 and obj2 > 60) or (agg2 > 60 and obj1 > 60):
            complementarity_score += 25
        
        # Team play complementarity (one supports, one carries)
        team1 = vector1.get("team_play", 50)
        team2 = vector2.get("team_play", 50)
        if abs(team1 - team2) > 30:
            complementarity_score += 25
        
        # Scaling complementarity (one early, one late)
        scale1 = vector1.get("scaling", 50)
        scale2 = vector2.get("scaling", 50)
        if abs(scale1 - scale2) > 30:
            complementarity_score += 25
        
        # Consistency complementarity (one consistent, one variable can work)
        cons1 = vector1.get("consistency", 50)
        cons2 = vector2.get("consistency", 50)
        if abs(cons1 - cons2) < 20:  # Both consistent is good
            complementarity_score += 25
        
        return min(100, complementarity_score)
    
    def _analyze_synergy(self, vector1: Dict, vector2: Dict) -> Dict:
        """Analyze synergy between two playstyles."""
        synergy_points = []
        
        # Check for complementary strengths
        if vector1.get("aggression", 50) > 60 and vector2.get("objective_focus", 50) > 60:
            synergy_points.append("Aggressive pressure creates objective opportunities")
        
        if vector1.get("team_play", 50) > 60 and vector2.get("team_play", 50) < 40:
            synergy_points.append("Team support enables solo carry potential")
        
        if vector1.get("scaling", 50) > 60 and vector2.get("scaling", 50) < 40:
            synergy_points.append("Early game pressure allows late game scaling")
        
        if vector1.get("objective_focus", 50) > 60 and vector2.get("aggression", 50) > 60:
            synergy_points.append("Objective control pairs well with aggressive plays")
        
        return {
            "synergy_level": "high" if len(synergy_points) >= 2 else "moderate" if len(synergy_points) == 1 else "low",
            "synergy_points": synergy_points,
            "recommended_strategy": self._suggest_strategy(vector1, vector2)
        }
    
    def _suggest_strategy(self, vector1: Dict, vector2: Dict) -> str:
        """Suggest team strategy based on playstyles."""
        if vector1.get("aggression", 50) > 60 and vector2.get("objective_focus", 50) > 60:
            return "Early aggression to create pressure, then secure objectives with number advantage"
        elif vector1.get("team_play", 50) > 60 and vector2.get("scaling", 50) > 60:
            return "Protect and scale strategy - support the scaling player to late game"
        elif vector1.get("objective_focus", 50) > 60 and vector2.get("objective_focus", 50) > 60:
            return "Objective-focused strategy - prioritize dragons, barons, and map control"
        else:
            return "Adaptive strategy - play to each player's strengths situationally"
    
    def _generate_comparison_recommendations(self, vector1: Dict, vector2: Dict,
                                            complementarity: float) -> List[str]:
        """Generate recommendations based on playstyle comparison."""
        recommendations = []
        
        if complementarity > 70:
            recommendations.append("These playstyles complement each other very well - great duo potential!")
        
        # Specific recommendations based on differences
        agg_diff = abs(vector1.get("aggression", 50) - vector2.get("aggression", 50))
        if agg_diff > 30:
            recommendations.append("Coordinate aggression levels - one should follow the other's pace")
        
        obj_diff = abs(vector1.get("objective_focus", 50) - vector2.get("objective_focus", 50))
        if obj_diff > 30:
            recommendations.append("Balance kill focus with objective control for optimal results")
        
        team_diff = abs(vector1.get("team_play", 50) - vector2.get("team_play", 50))
        if team_diff > 30:
            recommendations.append("Communicate playstyle preferences - one may need to adjust for team fights")
        
        return recommendations

