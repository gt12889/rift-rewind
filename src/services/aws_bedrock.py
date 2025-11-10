"""
AWS Bedrock integration for generative AI insights.
"""
import json
import boto3
from typing import Dict, List, Optional
from botocore.exceptions import ClientError
from config.settings import settings


class BedrockService:
    """Service for interacting with AWS Bedrock for AI-generated insights."""
    
    def __init__(self):
        self.region = settings.bedrock_region
        self.model_id = settings.bedrock_model_id
        
        # Initialize Bedrock runtime client
        self.client = boto3.client(
            'bedrock-runtime',
            region_name=self.region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key
        )
    
    def _invoke_model(self, prompt: str, max_tokens: int = 4000) -> str:
        """Invoke the Bedrock model with a prompt."""
        try:
            body = json.dumps({
                "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                "max_tokens_to_sample": max_tokens,
                "temperature": 0.7,
                "top_p": 0.9,
                "stop_sequences": ["\n\nHuman:"]
            })
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body,
                contentType="application/json",
                accept="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            return response_body.get('completion', '')
        
        except ClientError as e:
            print(f"Error invoking Bedrock model: {e}")
            raise
    
    def generate_insights(self, match_data: List[Dict], player_stats: Dict) -> Dict:
        """Generate personalized insights from match data."""
        prompt = f"""
Analyze the following League of Legends player statistics and match history to generate personalized insights that help players reflect, learn, and improve.

Player Statistics:
{json.dumps(player_stats, indent=2)}

Recent Match History (last 20 matches):
{json.dumps(match_data[:20], indent=2)}

Please provide:
1. Key strengths (top 3) - highlight what the player does well consistently
2. Areas for improvement (top 3) - identify specific growth opportunities
3. Notable trends or patterns - surface interesting patterns in their gameplay
4. Unexpected insights - reveal surprising or non-obvious insights that spark reflection
5. Personalized recommendations - actionable advice tailored to this player

Look for:
- Hidden patterns in their playstyle
- Surprising correlations (e.g., performance on certain days/times)
- Unique strengths that might not be obvious
- Habits that are helping or hurting their performance
- Opportunities for growth that go beyond basic stats

Format your response as JSON with the following structure:
{{
    "strengths": ["strength1", "strength2", "strength3"],
    "weaknesses": ["weakness1", "weakness2", "weakness3"],
    "trends": "description of trends",
    "unexpected_insights": ["insight1", "insight2", "insight3"],
    "recommendations": ["rec1", "rec2", "rec3"]
}}
"""
        
        response = self._invoke_model(prompt)
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except:
            pass
        
        # Fallback if JSON parsing fails
        return {
            "strengths": ["Strong performance", "Good decision making", "Consistent play"],
            "weaknesses": ["Room for improvement", "Focus on objectives", "Map awareness"],
            "trends": response[:500],
            "unexpected_insights": ["Interesting pattern detected", "Surprising correlation found", "Unique playstyle identified"],
            "recommendations": ["Practice more", "Watch replays", "Focus on fundamentals"]
        }
    
    def generate_year_end_summary(self, year_stats: Dict, highlights: List[Dict]) -> str:
        """Generate a fun, shareable year-end summary."""
        prompt = f"""
Create an engaging, fun, and shareable year-end retrospective for a League of Legends player that they can celebrate, learn from, and share.

Year Statistics:
{json.dumps(year_stats, indent=2)}

Key Highlights:
{json.dumps(highlights, indent=2)}

Write a creative, celebratory retrospective (2-3 paragraphs) that:
- Highlights achievements and milestones worth celebrating
- Surfaces unexpected insights and surprising patterns from their year
- Uses an engaging, friendly, and reflective tone
- Includes specific statistics and fun facts that tell their story
- Identifies growth areas and learning opportunities
- Makes the player want to share it on social media
- Celebrates their journey and growth throughout the year
- Sparks reflection on their gameplay evolution

Be creative, personal, and exciting! This should feel like a personalized year-in-review that goes beyond basic stats.
"""
        
        return self._invoke_model(prompt, max_tokens=2000)
    
    def generate_creative_year_summary(self, year_stats: Dict, highlights: List[Dict], 
                                       persistent_strengths: List[Dict], 
                                       improvements: List[Dict]) -> Dict:
        """Generate a creative, fun year-end summary with multiple formats."""
        prompt = f"""
Create a fun, engaging, and highly shareable year-end summary for a League of Legends player. 
Make it creative, celebratory, and personalized using AWS Bedrock's generative AI capabilities.

Year Statistics:
{json.dumps(year_stats, indent=2)}

Key Highlights:
{json.dumps(highlights, indent=2)}

Persistent Strengths (patterns that appeared consistently):
{json.dumps(persistent_strengths, indent=2)}

Improvements Made:
{json.dumps(improvements, indent=2)}

Generate the following in JSON format:
{{
    "narrative_summary": "A 2-3 paragraph engaging story of their year, written in a celebratory and reflective tone",
    "fun_facts": ["fact1", "fact2", "fact3"],
    "achievement_highlights": ["highlight1", "highlight2", "highlight3"],
    "memorable_moments": ["moment1", "moment2", "moment3"],
    "personalized_title": "A creative, personalized title for their year (e.g., 'The Year of the Carry', 'The Climb Chronicles')",
    "social_media_caption": "A short, shareable caption for social media (1-2 sentences)",
    "year_in_numbers": {{
        "most_played_champion": "champion name",
        "total_games": number,
        "win_rate": percentage,
        "biggest_improvement": "description",
        "longest_streak": number
    }},
    "reflection_questions": ["question1", "question2", "question3"]
}}

Make it fun, personal, and exciting! Use emojis where appropriate. This should be something they want to share with friends.
"""
        
        response = self._invoke_model(prompt, max_tokens=3000)
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except:
            pass
        
        # Fallback
        return {
            "narrative_summary": response[:500],
            "fun_facts": ["Played many games", "Improved over time", "Had fun"],
            "achievement_highlights": highlights[:3],
            "personalized_title": f"My {year_stats.get('year', 2024)} League Journey",
            "social_media_caption": f"Check out my {year_stats.get('year', 2024)} League recap! 🎮"
        }
    
    def generate_playstyle_comparison(self, player1_playstyle: Dict, player2_playstyle: Dict,
                                     comparison_data: Dict) -> str:
        """Generate a creative playstyle comparison narrative."""
        prompt = f"""
Create an engaging, fun comparison between two League of Legends players that highlights how their playstyles complement each other or differ.

Player 1 Playstyle:
{json.dumps(player1_playstyle, indent=2)}

Player 2 Playstyle:
{json.dumps(player2_playstyle, indent=2)}

Comparison Data:
{json.dumps(comparison_data, indent=2)}

Write a 2-3 paragraph comparison that:
- Highlights how their playstyles complement each other (if they do)
- Shows what makes each player unique
- Suggests how they could work together as a duo
- Uses a friendly, engaging tone
- Makes it shareable and fun to read
- Identifies synergy points and complementary strengths

Be creative and focus on the fun aspects of comparing playstyles!
"""
        
        return self._invoke_model(prompt, max_tokens=2000)
    
    def generate_progress_narrative(self, progress_data: Dict) -> str:
        """Generate a narrative about player progress over time."""
        prompt = f"""
Create an engaging narrative about a League of Legends player's progress over time, highlighting their journey, improvements, and persistent patterns.

Progress Data:
{json.dumps(progress_data, indent=2)}

Write a 2-3 paragraph narrative that:
- Tells the story of their progress journey
- Highlights persistent strengths that define their playstyle
- Celebrates improvements and growth
- Identifies areas that need attention
- Uses an encouraging, reflective tone
- Makes them feel proud of their progress
- Sparks motivation for continued improvement

Be personal, encouraging, and celebratory of their growth!
"""
        
        return self._invoke_model(prompt, max_tokens=2000)
    
    def generate_shareable_moment(self, moment_data: Dict, moment_type: str = "achievement") -> Dict:
        """Generate creative shareable content for a specific moment."""
        prompt = f"""
Create fun, engaging, shareable social media content for a League of Legends {moment_type}.

Moment Data:
{json.dumps(moment_data, indent=2)}

Generate the following in JSON format:
{{
    "title": "Creative, catchy title",
    "caption": "Engaging social media caption (1-2 sentences)",
    "hashtags": ["tag1", "tag2", "tag3"],
    "celebration_text": "Short celebration message",
    "fun_fact": "A fun fact about this achievement/moment"
}}

Make it exciting, celebratory, and shareable! Use emojis and make it fun.
"""
        
        response = self._invoke_model(prompt, max_tokens=1000)
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except:
            pass
        
        # Fallback
        return {
            "title": f"🎉 {moment_type.title()}!",
            "caption": f"Just achieved: {moment_data.get('description', '')} 🎮",
            "hashtags": ["#LeagueOfLegends", "#RiftRewind", "#Gaming"]
        }
    
    def generate_match_analysis(self, match: Dict, player_data: Dict) -> str:
        """Generate detailed analysis for a specific match."""
        prompt = f"""
Analyze this League of Legends match and provide insights for the player.

Match Data:
{json.dumps(match, indent=2)}

Player Performance:
{json.dumps(player_data, indent=2)}

Provide:
1. What went well
2. What could be improved
3. Key moments that impacted the game
4. Specific actionable advice

Keep it concise but insightful (3-4 paragraphs).
"""
        
        return self._invoke_model(prompt, max_tokens=1500)
    
    def generate_social_comparison(self, player_stats: Dict, friend_stats: Dict) -> str:
        """Generate a comparison between player and friend."""
        prompt = f"""
Compare two League of Legends players and create an engaging comparison.

Player 1 Stats:
{json.dumps(player_stats, indent=2)}

Player 2 Stats:
{json.dumps(friend_stats, indent=2)}

Create a friendly, engaging comparison that:
- Highlights complementary playstyles
- Shows how they stack up in different areas
- Suggests how they could work together
- Uses a fun, social media-friendly tone

Keep it positive and engaging (2-3 paragraphs).
"""
        
        return self._invoke_model(prompt, max_tokens=1500)
    
    def chat(self, user_message: str, context: Optional[str] = None, conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Chat with the AI agent using Amazon Bedrock.
        
        Args:
            user_message: The user's message/question
            context: Optional context about the user (e.g., player stats, match data)
            conversation_history: Optional list of previous messages in format [{"role": "user|assistant", "content": "..."}]
        
        Returns:
            The AI agent's response
        """
        # Build system prompt for League of Legends coaching agent
        system_prompt = """You are Zaahen, an expert League of Legends coaching agent in the Rift Rewind Hall of Legends. 
Your role is to help players improve their gameplay, understand their statistics, analyze their matches, 
and provide personalized coaching advice. Be friendly, knowledgeable, and encouraging. 
Focus on actionable insights and help players reflect on their gameplay. 
You are a wise and experienced coach who guides summoners to greatness on the Rift."""
        
        # Build conversation context
        conversation_text = ""
        if conversation_history:
            for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                role = "Human" if msg.get("role") == "user" else "Assistant"
                conversation_text += f"\n\n{role}: {msg.get('content', '')}"
        
        # Add optional context about the player
        context_text = ""
        if context:
            context_text = f"\n\nContext about the player:\n{context}"
        
        # Build the full prompt
        prompt = f"""{system_prompt}{context_text}{conversation_text}

Human: {user_message}

Assistant:"""
        
        return self._invoke_model(prompt, max_tokens=4000)

