"""
Track persistent strengths and weaknesses over time periods.
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
from src.analyzers.match_analyzer import MatchAnalyzer


class ProgressTracker:
    """Tracks player progress and persistent patterns over time."""
    
    def __init__(self):
        self.match_analyzer = MatchAnalyzer()
    
    def track_persistent_patterns(self, matches: List[Dict], puuid: str, time_period: str = "month") -> Dict:
        """
        Track persistent strengths and weaknesses over time periods.
        
        Args:
            matches: List of match data
            puuid: Player UUID
            time_period: "week", "month", or "quarter"
            
        Returns:
            Dict with persistent patterns, trends, and evolution
        """
        # Group matches by time period
        period_matches = self._group_matches_by_period(matches, puuid, time_period)
        
        if not period_matches:
            return {}
        
        # Analyze each period
        period_analyses = {}
        for period, period_match_list in period_matches.items():
            analysis = self.match_analyzer.analyze_player_matches(period_match_list, puuid)
            period_analyses[period] = {
                "analysis": analysis,
                "strengths": analysis.get("strengths", []),
                "weaknesses": analysis.get("weaknesses", []),
                "key_metrics": analysis.get("key_metrics", {}),
                "champion_stats": analysis.get("champion_stats", {}),
                "win_rate": analysis.get("win_rate", {}).get("win_rate", 0)
            }
        
        # Identify persistent strengths (appear in multiple periods)
        persistent_strengths = self._identify_persistent_patterns(
            period_analyses, "strengths"
        )
        
        # Identify persistent weaknesses (appear in multiple periods)
        persistent_weaknesses = self._identify_persistent_patterns(
            period_analyses, "weaknesses"
        )
        
        # Track evolution of metrics over time
        metric_evolution = self._track_metric_evolution(period_analyses)
        
        # Identify improvement areas (weaknesses that became strengths)
        improvements = self._identify_improvements(period_analyses)
        
        # Identify decline areas (strengths that became weaknesses)
        declines = self._identify_declines(period_analyses)
        
        return {
            "time_period": time_period,
            "periods_analyzed": list(period_analyses.keys()),
            "period_count": len(period_analyses),
            "persistent_strengths": persistent_strengths,
            "persistent_weaknesses": persistent_weaknesses,
            "metric_evolution": metric_evolution,
            "improvements": improvements,
            "declines": declines,
            "period_analyses": period_analyses,
            "summary": self._generate_summary(
                persistent_strengths,
                persistent_weaknesses,
                improvements,
                declines,
                metric_evolution
            )
        }
    
    def _group_matches_by_period(self, matches: List[Dict], puuid: str, period: str) -> Dict[str, List[Dict]]:
        """Group matches by time period."""
        period_matches = defaultdict(list)
        
        for match in matches:
            game_creation = match.get("info", {}).get("gameCreation", 0)
            if game_creation == 0:
                continue
            
            # Convert timestamp to datetime
            game_date = datetime.fromtimestamp(game_creation / 1000)
            
            # Determine period key
            if period == "week":
                # Group by week (year-week)
                year, week, _ = game_date.isocalendar()
                period_key = f"{year}-W{week:02d}"
            elif period == "month":
                # Group by month (year-month)
                period_key = f"{game_date.year}-{game_date.month:02d}"
            elif period == "quarter":
                # Group by quarter (year-quarter)
                quarter = (game_date.month - 1) // 3 + 1
                period_key = f"{game_date.year}-Q{quarter}"
            else:
                # Default to month
                period_key = f"{game_date.year}-{game_date.month:02d}"
            
            period_matches[period_key].append(match)
        
        # Sort periods
        sorted_periods = sorted(period_matches.keys())
        return {period: period_matches[period] for period in sorted_periods}
    
    def _identify_persistent_patterns(self, period_analyses: Dict, pattern_type: str) -> List[Dict]:
        """Identify patterns that appear consistently across multiple periods."""
        # Count occurrences of each pattern
        pattern_counts = defaultdict(int)
        pattern_details = defaultdict(list)
        
        for period, analysis_data in period_analyses.items():
            patterns = analysis_data.get(pattern_type, [])
            for pattern in patterns:
                # Normalize pattern text for comparison
                normalized = pattern.lower().strip()
                pattern_counts[normalized] += 1
                pattern_details[normalized].append({
                    "period": period,
                    "original_text": pattern
                })
        
        # Patterns that appear in at least 50% of periods are considered persistent
        min_periods = max(2, len(period_analyses) // 2)
        
        persistent_patterns = []
        for pattern, count in pattern_counts.items():
            if count >= min_periods:
                # Get the most common original text
                original_texts = [p["original_text"] for p in pattern_details[pattern]]
                most_common = max(set(original_texts), key=original_texts.count)
                
                persistent_patterns.append({
                    "pattern": most_common,
                    "frequency": count,
                    "periods_appeared": [p["period"] for p in pattern_details[pattern]],
                    "consistency_score": count / len(period_analyses) * 100
                })
        
        # Sort by consistency score
        persistent_patterns.sort(key=lambda x: x["consistency_score"], reverse=True)
        
        return persistent_patterns
    
    def _track_metric_evolution(self, period_analyses: Dict) -> Dict:
        """Track how key metrics evolve over time."""
        metrics = {
            "win_rate": [],
            "avg_kda": [],
            "avg_damage": [],
            "avg_vision_score": [],
            "avg_cs": []
        }
        
        periods = sorted(period_analyses.keys())
        
        for period in periods:
            analysis = period_analyses[period]
            key_metrics = analysis.get("key_metrics", {})
            
            metrics["win_rate"].append({
                "period": period,
                "value": analysis.get("win_rate", 0)
            })
            metrics["avg_kda"].append({
                "period": period,
                "value": key_metrics.get("avg_kda", 0)
            })
            metrics["avg_damage"].append({
                "period": period,
                "value": key_metrics.get("avg_damage", 0)
            })
            metrics["avg_vision_score"].append({
                "period": period,
                "value": key_metrics.get("avg_vision_score", 0)
            })
            metrics["avg_cs"].append({
                "period": period,
                "value": key_metrics.get("avg_cs", 0)
            })
        
        # Calculate trends for each metric
        trends = {}
        for metric_name, values in metrics.items():
            if len(values) >= 2:
                first_half = values[:len(values)//2]
                second_half = values[len(values)//2:]
                
                first_avg = statistics.mean([v["value"] for v in first_half])
                second_avg = statistics.mean([v["value"] for v in second_half])
                
                change = second_avg - first_avg
                change_percent = (change / first_avg * 100) if first_avg > 0 else 0
                
                trends[metric_name] = {
                    "trend": "improving" if change > 0 else "declining" if change < 0 else "stable",
                    "change": change,
                    "change_percent": change_percent,
                    "first_half_avg": first_avg,
                    "second_half_avg": second_avg,
                    "values": values
                }
            else:
                trends[metric_name] = {
                    "trend": "insufficient_data",
                    "values": values
                }
        
        return trends
    
    def _identify_improvements(self, period_analyses: Dict) -> List[Dict]:
        """Identify weaknesses that improved over time."""
        improvements = []
        periods = sorted(period_analyses.keys())
        
        if len(periods) < 2:
            return improvements
        
        # Compare early periods to recent periods
        early_periods = periods[:len(periods)//2]
        recent_periods = periods[len(periods)//2:]
        
        early_weaknesses = set()
        for period in early_periods:
            weaknesses = period_analyses[period].get("weaknesses", [])
            for weakness in weaknesses:
                early_weaknesses.add(weakness.lower().strip())
        
        recent_strengths = set()
        for period in recent_periods:
            strengths = period_analyses[period].get("strengths", [])
            for strength in strengths:
                recent_strengths.add(strength.lower().strip())
        
        # Find weaknesses that are now strengths
        for weakness in early_weaknesses:
            # Check if similar strength exists
            for strength in recent_strengths:
                if self._are_similar(weakness, strength):
                    improvements.append({
                        "area": weakness,
                        "improvement": "Weakness became a strength",
                        "early_periods": early_periods,
                        "recent_periods": recent_periods
                    })
                    break
        
        return improvements
    
    def _identify_declines(self, period_analyses: Dict) -> List[Dict]:
        """Identify strengths that declined over time."""
        declines = []
        periods = sorted(period_analyses.keys())
        
        if len(periods) < 2:
            return declines
        
        # Compare early periods to recent periods
        early_periods = periods[:len(periods)//2]
        recent_periods = periods[len(periods)//2:]
        
        early_strengths = set()
        for period in early_periods:
            strengths = period_analyses[period].get("strengths", [])
            for strength in strengths:
                early_strengths.add(strength.lower().strip())
        
        recent_weaknesses = set()
        for period in recent_periods:
            weaknesses = period_analyses[period].get("weaknesses", [])
            for weakness in weaknesses:
                recent_weaknesses.add(weakness.lower().strip())
        
        # Find strengths that are now weaknesses
        for strength in early_strengths:
            # Check if similar weakness exists
            for weakness in recent_weaknesses:
                if self._are_similar(strength, weakness):
                    declines.append({
                        "area": strength,
                        "decline": "Strength became a weakness",
                        "early_periods": early_periods,
                        "recent_periods": recent_periods
                    })
                    break
        
        return declines
    
    def _are_similar(self, text1: str, text2: str) -> bool:
        """Check if two text strings are similar (simple keyword matching)."""
        # Simple similarity check based on shared keywords
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        # Check for significant overlap
        common_words = words1.intersection(words2)
        if len(common_words) >= 2:
            return True
        
        # Check if one contains the other
        if len(words1) > 0 and len(words2) > 0:
            if any(word in text2 for word in words1 if len(word) > 4):
                return True
            if any(word in text1 for word in words2 if len(word) > 4):
                return True
        
        return False
    
    def _generate_summary(self, persistent_strengths: List[Dict], persistent_weaknesses: List[Dict],
                         improvements: List[Dict], declines: List[Dict], metric_evolution: Dict) -> Dict:
        """Generate a summary of progress tracking."""
        return {
            "persistent_strength_count": len(persistent_strengths),
            "persistent_weakness_count": len(persistent_weaknesses),
            "improvement_count": len(improvements),
            "decline_count": len(declines),
            "overall_trend": self._determine_overall_trend(metric_evolution),
            "key_insights": self._generate_key_insights(
                persistent_strengths,
                persistent_weaknesses,
                improvements,
                declines,
                metric_evolution
            )
        }
    
    def _determine_overall_trend(self, metric_evolution: Dict) -> str:
        """Determine overall trend based on metric evolution."""
        improving_count = 0
        declining_count = 0
        
        for metric, trend_data in metric_evolution.items():
            trend = trend_data.get("trend", "stable")
            if trend == "improving":
                improving_count += 1
            elif trend == "declining":
                declining_count += 1
        
        if improving_count > declining_count:
            return "improving"
        elif declining_count > improving_count:
            return "declining"
        else:
            return "stable"
    
    def _generate_key_insights(self, persistent_strengths: List[Dict], persistent_weaknesses: List[Dict],
                              improvements: List[Dict], declines: List[Dict], metric_evolution: Dict) -> List[str]:
        """Generate key insights from progress tracking."""
        insights = []
        
        if persistent_strengths:
            top_strength = persistent_strengths[0]
            insights.append(
                f"Most consistent strength: {top_strength['pattern']} "
                f"({top_strength['consistency_score']:.0f}% of periods)"
            )
        
        if persistent_weaknesses:
            top_weakness = persistent_weaknesses[0]
            insights.append(
                f"Most consistent area for improvement: {top_weakness['pattern']} "
                f"({top_weakness['consistency_score']:.0f}% of periods)"
            )
        
        if improvements:
            insights.append(f"Made {len(improvements)} significant improvement(s) - turned weaknesses into strengths!")
        
        if declines:
            insights.append(f"Watch out: {len(declines)} area(s) that were strengths need attention")
        
        # Add metric insights
        best_improving = None
        best_improvement_value = 0
        
        for metric, trend_data in metric_evolution.items():
            if trend_data.get("trend") == "improving":
                change_percent = abs(trend_data.get("change_percent", 0))
                if change_percent > best_improvement_value:
                    best_improvement_value = change_percent
                    best_improving = metric
        
        if best_improving:
            insights.append(
                f"Biggest improvement: {best_improving.replace('_', ' ').title()} "
                f"(+{best_improvement_value:.1f}%)"
            )
        
        return insights

