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

