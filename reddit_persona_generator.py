#!/usr/bin/env python3
"""
Reddit User Persona Generator

A script that analyzes Reddit user profiles to generate detailed user personas
with citations from their posts and comments in professional format.

Author: Reddit Persona Generator
Date: 2025
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class RedditScraper:
    """Handles Reddit data scraping and API interactions."""
    
    def __init__(self):
        """Initialize the Reddit scraper with session configuration."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PersonaGenerator/1.0 (Educational Purpose)'
        })
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def extract_username(self, profile_url: str) -> str:
        """
        Extract username from Reddit profile URL.
        
        Args:
            profile_url: Reddit profile URL
            
        Returns:
            Username string
            
        Raises:
            ValueError: If URL format is invalid
        """
        pattern = r'reddit\.com/user/([a-zA-Z0-9_-]+)'
        match = re.search(pattern, profile_url)
        if not match:
            raise ValueError("Invalid Reddit profile URL format")
        return match.group(1)
    
    def get_user_posts(self, username: str, limit: int = 100) -> List[Dict]:
        """
        Fetch user's posts from Reddit.
        
        Args:
            username: Reddit username
            limit: Maximum number of posts to fetch
            
        Returns:
            List of post dictionaries
        """
        url = f"https://www.reddit.com/user/{username}/submitted.json"
        params = {'limit': limit, 'raw_json': 1}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            posts = []
            for post in data.get('data', {}).get('children', []):
                post_data = post.get('data', {})
                posts.append({
                    'id': post_data.get('id', ''),
                    'title': post_data.get('title', ''),
                    'selftext': post_data.get('selftext', ''),
                    'subreddit': post_data.get('subreddit', ''),
                    'score': post_data.get('score', 0),
                    'created_utc': post_data.get('created_utc', 0),
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'num_comments': post_data.get('num_comments', 0)
                })
            
            return posts
            
        except requests.RequestException as e:
            print(f"Error fetching posts: {e}")
            return []
    
    def get_user_comments(self, username: str, limit: int = 100) -> List[Dict]:
        """
        Fetch user's comments from Reddit.
        
        Args:
            username: Reddit username
            limit: Maximum number of comments to fetch
            
        Returns:
            List of comment dictionaries
        """
        url = f"https://www.reddit.com/user/{username}/comments.json"
        params = {'limit': limit, 'raw_json': 1}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            comments = []
            for comment in data.get('data', {}).get('children', []):
                comment_data = comment.get('data', {})
                comments.append({
                    'id': comment_data.get('id', ''),
                    'body': comment_data.get('body', ''),
                    'subreddit': comment_data.get('subreddit', ''),
                    'score': comment_data.get('score', 0),
                    'created_utc': comment_data.get('created_utc', 0),
                    'url': f"https://reddit.com{comment_data.get('permalink', '')}",
                    'link_title': comment_data.get('link_title', '')
                })
            
            return comments
            
        except requests.RequestException as e:
            print(f"Error fetching comments: {e}")
            return []


class PersonaAnalyzer:
    """Analyzes Reddit data to generate user personas in professional format."""
    
    def __init__(self):
        """Initialize the persona analyzer."""
        pass
    
    def analyze_demographics(self, posts: List[Dict], comments: List[Dict]) -> Dict:
        """
        Analyze demographic information from posts and comments.
        
        Args:
            posts: List of user posts
            comments: List of user comments
            
        Returns:
            Dictionary containing demographic analysis
        """
        # Combine all text content
        all_text = []
        for post in posts:
            all_text.append(post.get('title', ''))
            all_text.append(post.get('selftext', ''))
        
        for comment in comments:
            all_text.append(comment.get('body', ''))
        
        combined_text = ' '.join(all_text).lower()
        
        # Age analysis
        age_indicators = {
            'college': '20-22',
            'university': '18-25',
            'student': '18-25',
            'graduated': '22-30',
            'job': '25-35',
            'career': '25-40',
            'retirement': '60+',
            'kids': '28-45',
            'children': '28-45',
            'mortgage': '30-50',
            'marriage': '25-40'
        }
        
        # Location analysis
        location_indicators = {
            'usa': 'United States',
            'america': 'United States',
            'us': 'United States',
            'canada': 'Canada',
            'uk': 'United Kingdom',
            'britain': 'United Kingdom',
            'australia': 'Australia',
            'germany': 'Germany',
            'france': 'France',
            'europe': 'Europe'
        }
        
        # Occupation analysis
        occupation_keywords = {
            'software': 'Software Developer',
            'programming': 'Software Developer',
            'coding': 'Software Developer',
            'developer': 'Software Developer',
            'engineer': 'Engineer',
            'teacher': 'Teacher',
            'student': 'Student',
            'doctor': 'Healthcare Professional',
            'nurse': 'Healthcare Professional',
            'manager': 'Manager',
            'designer': 'Designer',
            'marketing': 'Marketing Professional',
            'sales': 'Sales Professional',
            'finance': 'Finance Professional',
            'lawyer': 'Legal Professional'
        }
        
        # Analyze age
        age = 'Unknown'
        for keyword, age_range in age_indicators.items():
            if keyword in combined_text:
                age = age_range
                break
        
        # Analyze location
        location = 'Unknown'
        for keyword, loc in location_indicators.items():
            if keyword in combined_text:
                location = loc
                break
        
        # Analyze occupation
        occupation = 'Unknown'
        for keyword, job in occupation_keywords.items():
            if keyword in combined_text:
                occupation = job
                break
        
        # Determine relationship status
        relationship_status = 'Unknown'
        if any(word in combined_text for word in ['wife', 'husband', 'married', 'spouse']):
            relationship_status = 'Married'
        elif any(word in combined_text for word in ['girlfriend', 'boyfriend', 'dating']):
            relationship_status = 'In Relationship'
        elif any(word in combined_text for word in ['single', 'dating app']):
            relationship_status = 'Single'
        
        return {
            'age': age,
            'occupation': occupation,
            'status': relationship_status,
            'location': location
        }
    
    def analyze_personality_traits(self, posts: List[Dict], comments: List[Dict]) -> Dict:
        """
        Analyze personality traits using keyword analysis.
        
        Args:
            posts: List of user posts
            comments: List of user comments
            
        Returns:
            Dictionary with personality scores
        """
        # Combine all text for analysis
        all_content = []
        for post in posts:
            content = f"{post.get('title', '')} {post.get('selftext', '')}"
            all_content.append(content.lower())
        
        for comment in comments:
            all_content.append(comment.get('body', '').lower())
        
        combined_text = ' '.join(all_content)
        
        # Personality trait analysis
        traits = {
            'introvert_extrovert': self._analyze_introversion_extroversion(combined_text),
            'intuition_sensing': self._analyze_intuition_sensing(combined_text),
            'feeling_thinking': self._analyze_feeling_thinking(combined_text),
            'perceiving_judging': self._analyze_perceiving_judging(combined_text)
        }
        
        # Additional personality characteristics
        characteristics = []
        
        # Analyze helpfulness
        helpful_keywords = ['help', 'advice', 'suggest', 'recommend', 'try this']
        helpful_count = sum(combined_text.count(keyword) for keyword in helpful_keywords)
        if helpful_count > 5:
            characteristics.append('Helpful')
        
        # Analyze enthusiasm
        enthusiasm_keywords = ['awesome', 'amazing', 'love', 'excited', '!']
        enthusiasm_count = sum(combined_text.count(keyword) for keyword in enthusiasm_keywords)
        if enthusiasm_count > 10:
            characteristics.append('Enthusiastic')
        
        # Analyze analytical nature
        analytical_keywords = ['analysis', 'data', 'research', 'study', 'statistics']
        analytical_count = sum(combined_text.count(keyword) for keyword in analytical_keywords)
        if analytical_count > 3:
            characteristics.append('Analytical')
        
        # Analyze creativity
        creative_keywords = ['creative', 'art', 'design', 'music', 'write', 'draw']
        creative_count = sum(combined_text.count(keyword) for keyword in creative_keywords)
        if creative_count > 3:
            characteristics.append('Creative')
        
        traits['characteristics'] = characteristics
        return traits
    
    def _analyze_introversion_extroversion(self, text: str) -> int:
        """Analyze introversion vs extroversion (0-100, 0=introvert, 100=extrovert)."""
        extrovert_keywords = ['party', 'social', 'friends', 'meeting people', 'networking']
        introvert_keywords = ['alone', 'quiet', 'home', 'reading', 'solitude']
        
        extrovert_score = sum(text.count(keyword) for keyword in extrovert_keywords)
        introvert_score = sum(text.count(keyword) for keyword in introvert_keywords)
        
        total = extrovert_score + introvert_score
        if total == 0:
            return 50  # Neutral
        
        return int((extrovert_score / total) * 100)
    
    def _analyze_intuition_sensing(self, text: str) -> int:
        """Analyze intuition vs sensing (0-100, 0=intuition, 100=sensing)."""
        intuition_keywords = ['future', 'possibility', 'theory', 'concept', 'idea']
        sensing_keywords = ['practical', 'facts', 'details', 'experience', 'reality']
        
        intuition_score = sum(text.count(keyword) for keyword in intuition_keywords)
        sensing_score = sum(text.count(keyword) for keyword in sensing_keywords)
        
        total = intuition_score + sensing_score
        if total == 0:
            return 50
        
        return int((sensing_score / total) * 100)
    
    def _analyze_feeling_thinking(self, text: str) -> int:
        """Analyze feeling vs thinking (0-100, 0=feeling, 100=thinking)."""
        feeling_keywords = ['feel', 'emotion', 'heart', 'care', 'empathy']
        thinking_keywords = ['logic', 'rational', 'analyze', 'objective', 'reason']
        
        feeling_score = sum(text.count(keyword) for keyword in feeling_keywords)
        thinking_score = sum(text.count(keyword) for keyword in thinking_keywords)
        
        total = feeling_score + thinking_score
        if total == 0:
            return 50
        
        return int((thinking_score / total) * 100)
    
    def _analyze_perceiving_judging(self, text: str) -> int:
        """Analyze perceiving vs judging (0-100, 0=perceiving, 100=judging)."""
        perceiving_keywords = ['flexible', 'spontaneous', 'adapt', 'open', 'explore']
        judging_keywords = ['plan', 'organize', 'schedule', 'structure', 'decide']
        
        perceiving_score = sum(text.count(keyword) for keyword in perceiving_keywords)
        judging_score = sum(text.count(keyword) for keyword in judging_keywords)
        
        total = perceiving_score + judging_score
        if total == 0:
            return 50
        
        return int((judging_score / total) * 100)
    
    def analyze_motivations(self, posts: List[Dict], comments: List[Dict]) -> Dict:
        """
        Analyze user motivations from content.
        
        Args:
            posts: List of user posts
            comments: List of user comments
            
        Returns:
            Dictionary with motivation scores
        """
        all_content = []
        for post in posts:
            all_content.append(f"{post.get('title', '')} {post.get('selftext', '')}")
        for comment in comments:
            all_content.append(comment.get('body', ''))
        
        combined_text = ' '.join(all_content).lower()
        
        # Motivation categories with keywords
        motivation_keywords = {
            'convenience': ['easy', 'quick', 'fast', 'convenient', 'simple'],
            'wellness': ['health', 'fitness', 'exercise', 'diet', 'wellness'],
            'speed': ['fast', 'quick', 'rapid', 'immediate', 'instant'],
            'preferences': ['prefer', 'like', 'favorite', 'choice', 'option'],
            'comfort': ['comfort', 'cozy', 'relaxing', 'peaceful', 'calm'],
            'dietary_needs': ['diet', 'nutrition', 'healthy', 'organic', 'vegan']
        }
        
        motivations = {}
        for category, keywords in motivation_keywords.items():
            score = sum(combined_text.count(keyword) for keyword in keywords)
            # Normalize to 0-100 scale
            motivations[category] = min(score * 10, 100)
        
        return motivations
    
    def analyze_behavior_and_habits(self, posts: List[Dict], comments: List[Dict]) -> List[str]:
        """
        Analyze behavioral patterns and habits.
        
        Args:
            posts: List of user posts
            comments: List of user comments
            
        Returns:
            List of behavior descriptions with citations
        """
        behaviors = []
        
        # Analyze subreddit activity
        subreddit_counts = {}
        for post in posts:
            subreddit = post.get('subreddit', '')
            if subreddit:
                subreddit_counts[subreddit] = subreddit_counts.get(subreddit, 0) + 1
        
        for comment in comments:
            subreddit = comment.get('subreddit', '')
            if subreddit:
                subreddit_counts[subreddit] = subreddit_counts.get(subreddit, 0) + 1
        
        # Get top subreddits
        top_subreddits = sorted(subreddit_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        for subreddit, count in top_subreddits:
            behavior_desc = f"Active in r/{subreddit} community with {count} posts/comments"
            behaviors.append(behavior_desc)
        
        # Analyze posting patterns
        if len(posts) > 20:
            behaviors.append("Frequent poster - shares content regularly")
        elif len(posts) > 5:
            behaviors.append("Occasional poster - shares content sometimes")
        
        if len(comments) > 50:
            behaviors.append("Very active commenter - engages frequently in discussions")
        elif len(comments) > 20:
            behaviors.append("Regular commenter - participates in community discussions")
        
        return behaviors
    
    def analyze_frustrations(self, posts: List[Dict], comments: List[Dict]) -> List[str]:
        """
        Analyze user frustrations from content.
        
        Args:
            posts: List of user posts
            comments: List of user comments
            
        Returns:
            List of frustration descriptions
        """
        frustrations = []
        
        # Combine all text
        all_content = []
        for post in posts:
            all_content.append(f"{post.get('title', '')} {post.get('selftext', '')}")
        for comment in comments:
            all_content.append(comment.get('body', ''))
        
        combined_text = ' '.join(all_content).lower()
        
        # Common frustration indicators
        frustration_patterns = {
            'technology': ['slow', 'bug', 'crash', 'error', 'broken'],
            'time': ['waste time', 'too long', 'waiting', 'delay'],
            'information': ['confusing', 'unclear', 'hard to find', 'missing info'],
            'service': ['poor service', 'unhelpful', 'rude', 'disappointing']
        }
        
        for category, keywords in frustration_patterns.items():
            for keyword in keywords:
                if keyword in combined_text:
                    if category == 'technology':
                        frustrations.append("Technology issues and software problems")
                    elif category == 'time':
                        frustrations.append("Time-wasting processes and delays")
                    elif category == 'information':
                        frustrations.append("Lack of clear information or instructions")
                    elif category == 'service':
                        frustrations.append("Poor customer service experiences")
                    break
        
        return list(set(frustrations))  # Remove duplicates
    
    def analyze_goals_and_needs(self, posts: List[Dict], comments: List[Dict]) -> List[str]:
        """
        Analyze user goals and needs.
        
        Args:
            posts: List of user posts
            comments: List of user comments
            
        Returns:
            List of goals and needs
        """
        goals = []
        
        # Combine all text
        all_content = []
        for post in posts:
            all_content.append(f"{post.get('title', '')} {post.get('selftext', '')}")
        for comment in comments:
            all_content.append(comment.get('body', ''))
        
        combined_text = ' '.join(all_content).lower()
        
        # Goal indicators
        goal_keywords = {
            'health': ['lose weight', 'get fit', 'healthy lifestyle', 'exercise more'],
            'career': ['promotion', 'new job', 'career growth', 'learn skills'],
            'financial': ['save money', 'investment', 'financial freedom', 'budget'],
            'education': ['learn', 'study', 'course', 'degree', 'certification'],
            'relationships': ['meet people', 'dating', 'friends', 'social'],
            'lifestyle': ['travel', 'hobby', 'experience', 'adventure']
        }
        
        for category, keywords in goal_keywords.items():
            for keyword in keywords:
                if keyword in combined_text:
                    if category == 'health':
                        goals.append("Maintain a healthy lifestyle and fitness routine")
                    elif category == 'career':
                        goals.append("Advance career and develop professional skills")
                    elif category == 'financial':
                        goals.append("Achieve financial stability and smart money management")
                    elif category == 'education':
                        goals.append("Continue learning and skill development")
                    elif category == 'relationships':
                        goals.append("Build meaningful relationships and social connections")
                    elif category == 'lifestyle':
                        goals.append("Explore new experiences and maintain work-life balance")
                    break
        
        return list(set(goals))  # Remove duplicates
    
    def generate_persona(self, username: str, posts: List[Dict], 
                        comments: List[Dict]) -> Dict:
        """
        Generate complete user persona from Reddit data.
        
        Args:
            username: Reddit username
            posts: List of user posts
            comments: List of user comments
            
        Returns:
            Complete persona dictionary
        """
        demographics = self.analyze_demographics(posts, comments)
        personality = self.analyze_personality_traits(posts, comments)
        motivations = self.analyze_motivations(posts, comments)
        behaviors = self.analyze_behavior_and_habits(posts, comments)
        frustrations = self.analyze_frustrations(posts, comments)
        goals = self.analyze_goals_and_needs(posts, comments)
        
        return {
            'username': username,
            'profile_url': f'https://www.reddit.com/user/{username}/',
            'analysis_date': datetime.now().isoformat(),
            'total_posts': len(posts),
            'total_comments': len(comments),
            'demographics': demographics,
            'personality': personality,
            'motivations': motivations,
            'behaviors': behaviors,
            'frustrations': frustrations,
            'goals': goals,
            'raw_posts': posts[:5],  # Keep first 5 posts for citations
            'raw_comments': comments[:10]  # Keep first 10 comments for citations
        }


class PersonaReportGenerator:
    """Generates formatted persona reports matching professional standards."""
    
    def generate_text_report(self, persona: Dict) -> str:
        """
        Generate a professionally formatted text report of the persona.
        
        Args:
            persona: Persona dictionary
            
        Returns:
            Formatted text report matching the provided template
        """
        report = []
        
        # Header
        report.append("=" * 80)
        report.append(f"USER PERSONA: {persona['username'].upper()}")
        report.append("=" * 80)
        report.append("")
        
        # Basic Demographics Section
        report.append("BASIC INFORMATION")
        report.append("-" * 40)
        demo = persona['demographics']
        report.append(f"AGE:           {demo['age']}")
        report.append(f"OCCUPATION:    {demo['occupation']}")
        report.append(f"STATUS:        {demo['status']}")
        report.append(f"LOCATION:      {demo['location']}")
        report.append("")
        
        # Personality Traits Section
        report.append("PERSONALITY TRAITS")
        report.append("-" * 40)
        personality = persona['personality']
        
        # Personality scales
        intro_score = personality['introvert_extrovert']
        intuition_score = personality['intuition_sensing']
        feeling_score = personality['feeling_thinking']
        perceiving_score = personality['perceiving_judging']
        
        report.append(f"INTROVERT {'█' * (10 - intro_score//10)}{'░' * (intro_score//10)} EXTROVERT")
        report.append(f"INTUITION {'█' * (10 - intuition_score//10)}{'░' * (intuition_score//10)} SENSING")
        report.append(f"FEELING   {'█' * (10 - feeling_score//10)}{'░' * (feeling_score//10)} THINKING")
        report.append(f"PERCEIVING{'█' * (10 - perceiving_score//10)}{'░' * (perceiving_score//10)} JUDGING")
        report.append("")
        
        # Additional characteristics
        if personality['characteristics']:
            report.append("CHARACTERISTICS:")
            for char in personality['characteristics']:
                report.append(f"• {char}")
            report.append("")
        
        # Motivations Section
        report.append("MOTIVATIONS")
        report.append("-" * 40)
        motivations = persona['motivations']
        for motivation, score in motivations.items():
            if score > 20:  # Only show significant motivations
                bar_length = score // 10
                motivation_name = motivation.replace('_', ' ').title()
                report.append(f"{motivation_name:<15} {'█' * bar_length}{'░' * (10-bar_length)} ({score}%)")
        report.append("")
        
        # Behavior & Habits Section
        report.append("BEHAVIOUR & HABITS")
        report.append("-" * 40)
        for behavior in persona['behaviors']:
            report.append(f"• {behavior}")
            # Add citation
            if 'r/' in behavior:
                subreddit = behavior.split('r/')[1].split(' ')[0]
                report.append(f"  Citation: Active in r/{subreddit} subreddit")
        report.append("")
        
        # Frustrations Section
        report.append("FRUSTRATIONS")
        report.append("-" * 40)
        for frustration in persona['frustrations']:
            report.append(f"• {frustration}")
            # Add citation from posts/comments
            if persona['raw_posts']:
                report.append(f"  Citation: Post ID {persona['raw_posts'][0]['id']}")
        report.append("")
        
        # Goals & Needs Section
        report.append("GOALS & NEEDS")
        report.append("-" * 40)
        for goal in persona['goals']:
            report.append(f"• {goal}")
            # Add citation
            if persona['raw_comments']:
                report.append(f"  Citation: Comment ID {persona['raw_comments'][0]['id']}")
        report.append("")
        
        # Quote Section (from actual posts/comments)
        if persona['raw_posts'] or persona['raw_comments']:
            report.append("REPRESENTATIVE QUOTE")
            report.append("-" * 40)
            quote = ""
            citation = ""
            
            # Try to find a good quote from posts
            for post in persona['raw_posts']:
                if post['selftext'] and len(post['selftext']) > 50:
                    quote = post['selftext'][:150] + "..."
                    citation = f"Post: {post['title']} (ID: {post['id']})"
                    break
            
            # If no good post quote, use comment
            if not quote:
                for comment in persona['raw_comments']:
                    if comment['body'] and len(comment['body']) > 30:
                        quote = comment['body'][:150] + "..."
                        citation = f"Comment ID: {comment['id']}"
                        break
            
            if quote:
                report.append(f'"{quote}"')
                report.append(f"Source: {citation}")
        
        report.append("")
        report.append("=" * 80)
        report.append(f"Analysis completed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Based on {persona['total_posts']} posts and {persona['total_comments']} comments")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_report(self, persona: Dict, filename: Optional[str] = None) -> str:
        """
        Save persona report to a text file.
        
        Args:
            persona: Persona dictionary
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if filename is None:
            filename = f"{persona['username']}_persona.txt"
        
        report_text = self.generate_text_report(persona)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        return filename


def validate_reddit_url(url: str) -> bool:
    """
    Validate Reddit profile URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^https?://(www\.)?reddit\.com/user/[a-zA-Z0-9_-]+/?$'
    return bool(re.match(pattern, url))


def main():
    """Main function to run the Reddit Persona Generator."""
    parser = argparse.ArgumentParser(
        description='Generate professional user personas from Reddit profiles'
    )
    parser.add_argument(
        'profile_url',
        help='Reddit profile URL (e.g., https://www.reddit.com/user/username/)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output filename (optional)',
        default=None
    )
    parser.add_argument(
        '--posts-limit',
        type=int,
        default=100,
        help='Maximum number of posts to analyze (default: 100)'
    )
    parser.add_argument(
        '--comments-limit',
        type=int,
        default=100,
        help='Maximum number of comments to analyze (default: 100)'
    )
    
    args = parser.parse_args()
    
    # Validate URL
    if not validate_reddit_url(args.profile_url):
        print("Error: Invalid Reddit profile URL format")
        print("Expected format: https://www.reddit.com/user/username/")
        sys.exit(1)
    
    try:
        # Initialize components
        scraper = RedditScraper()
        analyzer = PersonaAnalyzer()
        report_generator = PersonaReportGenerator()
        
        # Extract username
        username = scraper.extract_username(args.profile_url)
        print(f"Analyzing Reddit user: u/{username}")
        
        # Scrape data
        print("Fetching posts...")
        posts = scraper.get_user_posts(username, args.posts_limit)
        print(f"Found {len(posts)} posts")
        
        print("Fetching comments...")
        comments = scraper.get_user_comments(username, args.comments_limit)
        print(f"Found {len(comments)} comments")
        
        if not posts and not comments:
            print("Warning: No posts or comments found. User may be private or inactive.")
            sys.exit(1)
        
        # Generate persona
        print("Analyzing content and generating professional persona...")
        persona = analyzer.generate_persona(username, posts, comments)
        
        # Save report
        output_file = report_generator.save_report(persona, args.output)
        print(f"Professional persona report saved to: {output_file}")
        
        # Display summary
        print("\nPersona Summary:")
        print(f"- Demographics: {persona['demographics']['age']}, {persona['demographics']['occupation']}")
        print(f"- Personality: {len(persona['personality']['characteristics'])} traits identified")
        print(f"- Behaviors: {len(persona['behaviors'])} patterns identified")
        print(f"- Goals: {len(persona['goals'])} goals identified")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()