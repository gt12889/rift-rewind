"""
Riot Games API integration for fetching League of Legends match data.
"""
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import time
from config.settings import settings


class RiotAPIClient:
    """Client for interacting with Riot Games API."""
    
    def __init__(self):
        self.api_key = settings.riot_api_key
        self.base_url = settings.riot_api_base_url  # Americas routing for match-v5
        self.regional_base_urls = {
            "na1": "https://na1.api.riotgames.com",
            "euw1": "https://euw1.api.riotgames.com",
            "eun1": "https://eun1.api.riotgames.com",
            "kr": "https://kr.api.riotgames.com",
            "br1": "https://br1.api.riotgames.com",
            "la1": "https://la1.api.riotgames.com",
            "la2": "https://la2.api.riotgames.com",
            "oc1": "https://oc1.api.riotgames.com",
            "ru": "https://ru.api.riotgames.com",
            "tr1": "https://tr1.api.riotgames.com",
            "jp1": "https://jp1.api.riotgames.com"
        }
        self.headers = {
            "X-Riot-Token": self.api_key
        }
        self.rate_limit_delay = 1.2  # Respect rate limits (100 requests per 2 minutes)
        self.last_request_time = 0
        self.request_timeout = 30  # 30 second timeout for all requests
        self.max_retries = 3  # Maximum retry attempts
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None, timeout: Optional[int] = None, retries: int = None) -> Dict:
        """Make a rate-limited API request with timeout and retry logic."""
        if timeout is None:
            timeout = self.request_timeout
        if retries is None:
            retries = self.max_retries
        
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=timeout)
                response.raise_for_status()
                self.last_request_time = time.time()
                return response.json()
            except requests.exceptions.Timeout:
                if attempt < retries - 1:
                    wait_time = (attempt + 1) * 2  # Exponential backoff: 2s, 4s, 6s
                    time.sleep(wait_time)
                    continue
                raise Exception(f"Request to Riot API timed out after {timeout} seconds (attempt {attempt + 1}/{retries}). Please check your connection and try again.")
            except requests.exceptions.RequestException as e:
                if attempt < retries - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                    continue
                raise Exception(f"Riot API request failed: {str(e)}")
        
        raise Exception("Failed to complete request after all retry attempts.")
    
    def get_summoner_by_name(self, summoner_name: str, region: str = "na1") -> Dict:
        """Get summoner information by Riot ID (gameName#tagLine)."""
        # Parse Riot ID format (gameName#tagLine)
        if '#' in summoner_name:
            game_name, tag_line = summoner_name.split('#', 1)
        else:
            # If no tag provided, assume NA1
            game_name = summoner_name
            tag_line = "NA1"
        
        # First, get account info using Riot ID
        # Map region to routing value
        routing_map = {
            "na1": "americas",
            "br1": "americas",
            "la1": "americas",
            "la2": "americas",
            "euw1": "europe",
            "eun1": "europe",
            "tr1": "europe",
            "ru": "europe",
            "kr": "asia",
            "jp1": "asia",
            "oc1": "sea"
        }
        routing = routing_map.get(region, "americas")
        routing_base = f"https://{routing}.api.riotgames.com"
        
        # Get account by Riot ID
        account_endpoint = f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        url = f"{routing_base}{account_endpoint}"
        
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        # Retry logic for account lookup
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=self.request_timeout)
                response.raise_for_status()
                self.last_request_time = time.time()
                account = response.json()
                break
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep((attempt + 1) * 2)
                    continue
                raise Exception(f"Request to Riot API timed out (attempt {attempt + 1}/{self.max_retries}). Please check your connection.")
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep((attempt + 1) * 2)
                    continue
                raise Exception(f"Riot API request failed: {str(e)}")
        else:
            raise Exception("Failed to get account info after all retry attempts.")
        
        # Now get summoner info using PUUID
        puuid = account.get("puuid")
        if not puuid:
            raise Exception("PUUID not found in account response")
        
        # Get summoner by PUUID
        regional_url = self.regional_base_urls.get(region, self.regional_base_urls["na1"])
        summoner_endpoint = f"/lol/summoner/v4/summoners/by-puuid/{puuid}"
        summoner_url = f"{regional_url}{summoner_endpoint}"
        
        # Retry logic for summoner lookup
        for attempt in range(self.max_retries):
            try:
                response = requests.get(summoner_url, headers=self.headers, timeout=self.request_timeout)
                response.raise_for_status()
                
                # Merge account and summoner data
                summoner = response.json()
                break
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep((attempt + 1) * 2)
                    continue
                raise Exception(f"Request to Riot API timed out (attempt {attempt + 1}/{self.max_retries}). Please check your connection.")
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep((attempt + 1) * 2)
                    continue
                raise Exception(f"Riot API request failed: {str(e)}")
        else:
            raise Exception("Failed to get summoner info after all retry attempts.")
        summoner["puuid"] = puuid
        summoner["gameName"] = account.get("gameName")
        summoner["tagLine"] = account.get("tagLine")
        
        return summoner
    
    def get_summoner_by_puuid(self, puuid: str) -> Dict:
        """Get summoner information by PUUID."""
        endpoint = f"/riot/account/v1/accounts/by-puuid/{puuid}"
        return self._make_request(endpoint)
    
    def get_match_history(self, puuid: str, start: int = 0, count: int = 100) -> List[str]:
        """Get match history IDs for a player."""
        endpoint = f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {
            "start": start,
            "count": count
        }
        return self._make_request(endpoint, params)
    
    def get_match_details(self, match_id: str) -> Dict:
        """Get detailed match information."""
        endpoint = f"/lol/match/v5/matches/{match_id}"
        return self._make_request(endpoint)
    
    def get_full_year_matches(self, puuid: str, year: int = 2024) -> List[Dict]:
        """Get all matches for a specific year."""
        all_match_ids = []
        start = 0
        batch_size = 100
        
        # Fetch all match IDs
        while True:
            match_ids = self.get_match_history(puuid, start=start, count=batch_size)
            if not match_ids:
                break
            
            all_match_ids.extend(match_ids)
            start += batch_size
            
            # Rate limiting - be conservative
            time.sleep(0.1)
        
        # Filter matches by year
        year_matches = []
        year_start = datetime(year, 1, 1).timestamp() * 1000
        year_end = datetime(year + 1, 1, 1).timestamp() * 1000
        
        for match_id in all_match_ids:
            try:
                match = self.get_match_details(match_id)
                match_timestamp = match.get("info", {}).get("gameCreation", 0)
                
                if year_start <= match_timestamp < year_end:
                    year_matches.append(match)
                
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                print(f"Error fetching match {match_id}: {e}")
                continue
        
        return year_matches
    
    def get_player_match_data(self, match: Dict, puuid: str) -> Optional[Dict]:
        """Extract player-specific data from a match."""
        participants = match.get("info", {}).get("participants", [])
        for participant in participants:
            if participant.get("puuid") == puuid:
                return participant
        return None
    
    def get_league_entries_by_puuid(self, puuid: str, region: str = "na1") -> List[Dict]:
        """Get league entries for a player by PUUID."""
        regional_url = self.regional_base_urls.get(region, self.regional_base_urls["na1"])
        endpoint = f"/lol/league/v4/entries/by-puuid/{puuid}"
        url = f"{regional_url}{endpoint}"
        
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        # Retry logic for league entries
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=self.request_timeout)
                response.raise_for_status()
                self.last_request_time = time.time()
                return response.json()
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep((attempt + 1) * 2)
                    continue
                raise Exception(f"Request to Riot API timed out (attempt {attempt + 1}/{self.max_retries}). Please check your connection.")
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep((attempt + 1) * 2)
                    continue
                raise Exception(f"Riot API request failed: {str(e)}")
        else:
            raise Exception("Failed to get league entries after all retry attempts.")
    
    def get_rank_info(self, puuid: str, region: str = "na1") -> Dict:
        """Get formatted rank information for a player."""
        league_entries = self.get_league_entries_by_puuid(puuid, region)
        
        rank_info = {
            "solo_queue": None,
            "flex_queue": None
        }
        
        for entry in league_entries:
            queue_type = entry.get("queueType")
            rank_data = {
                "tier": entry.get("tier"),
                "rank": entry.get("rank"),
                "league_points": entry.get("leaguePoints"),
                "wins": entry.get("wins"),
                "losses": entry.get("losses"),
                "win_rate": (entry.get("wins", 0) / max(entry.get("wins", 0) + entry.get("losses", 0), 1)) * 100,
                "veteran": entry.get("veteran", False),
                "hot_streak": entry.get("hotStreak", False)
            }
            
            if queue_type == "RANKED_SOLO_5x5":
                rank_info["solo_queue"] = rank_data
            elif queue_type == "RANKED_FLEX_SR":
                rank_info["flex_queue"] = rank_data
        
        return rank_info

