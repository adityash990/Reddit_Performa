# Reddit User Persona Generator

A Python script that analyzes Reddit user profiles to generate detailed, professional user personas with citations from their posts and comments. The output format matches industry-standard persona templates used in UX research and marketing.

## Features

- **Professional Persona Format**: Generates personas matching industry standards with visual personality scales
- **Comprehensive Analysis**: Analyzes demographics, personality traits, motivations, behaviors, frustrations, and goals
- **Citation System**: Links each persona characteristic to specific posts/comments for verification
- **Visual Personality Scales**: Uses bar charts to display personality dimensions (Introvert/Extrovert, etc.)
- **Representative Quotes**: Includes actual quotes from user's posts/comments
- **Command Line Interface**: Easy-to-use CLI with customizable options
- **Error Handling**: Robust error handling for private profiles and API limits

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd reddit-persona-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python reddit_persona_generator.py --help
   ```

## Usage

### Basic Usage

```bash
python reddit_persona_generator.py "https://www.reddit.com/user/username/"
```

### Advanced Usage

```bash
# Specify output filename
python reddit_persona_generator.py "https://www.reddit.com/user/username/" -o custom_report.txt

# Limit number of posts and comments analyzed
python reddit_persona_generator.py "https://www.reddit.com/user/username/" --posts-limit 50 --comments-limit 50
```

### Command Line Options

- `profile_url`: Reddit profile URL (required)
- `-o, --output`: Custom output filename (optional)
- `--posts-limit`: Maximum number of posts to analyze (default: 100)
- `--comments-limit`: Maximum number of comments to analyze (default: 100)

## Sample Usage

### Example 1: kojied
```bash
python reddit_persona_generator.py "https://www.reddit.com/user/kojied/"
```

### Example 2: Hungry-Move-6603
```bash
python reddit_persona_generator.py "https://www.reddit.com/user/Hungry-Move-6603/"
```

## Output Format

The script generates a professional persona report containing:

### 1. **Basic Information**
   - Age estimation
   - Occupation analysis
   - Relationship status
   - Location indicators

### 2. **Personality Traits**
   - Visual personality scales using bar charts:
     - Introvert ████████░░ Extrovert
     - Intuition ██████░░░░ Sensing
     - Feeling ███████░░░ Thinking
     - Perceiving████████░░ Judging
   - Additional characteristics (Helpful, Analytical, etc.)

### 3. **Motivations**
   - Visual motivation scales with percentages:
     - Convenience ████████░░ (80%)
     - Wellness ██████░░░░ (60%)
     - Speed ███████░░░ (70%)

### 4. **Behaviour & Habits**
   - Activity patterns with citations
   - Subreddit preferences
   - Posting frequency analysis

### 5. **Frustrations**
   - Identified pain points
   - Source citations from posts/comments

### 6. **Goals & Needs**
   - Personal and professional goals
   - Supporting evidence from content

### 7. **Representative Quote**
   - Actual quote from user's content
   - Source citation with post/comment ID

## File Structure

```
reddit-persona-generator/
├── reddit_persona_generator.py    # Main script
├── requirements.txt               # Python dependencies
├── README.md                     # This file
├── kojied_persona.txt            # Sample output for kojied
├── Hungry-Move-6603_persona.txt  # Sample output for Hungry-Move-6603
└── .gitignore                    # Git ignore file
```

## Technical Details

### Architecture

The script follows PEP-8 guidelines and is organized into modular classes:

- **RedditScraper**: Handles Reddit API interactions and data fetching
- **PersonaAnalyzer**: Analyzes scraped data using keyword analysis and pattern recognition
- **PersonaReportGenerator**: Formats and saves professional persona reports

### Data Sources

- Reddit public posts and comments via JSON API
- Subreddit activity patterns
- Content analysis for personality traits and motivations
- Temporal activity patterns

### Analysis Methods

The current implementation uses:
- **Keyword-based analysis** for demographic inference
- **Pattern recognition** for personality trait identification
- **Frequency analysis** for motivation scoring
- **Content categorization** for behavior pattern detection

For production use, consider integrating:
- Large Language Models (LLMs) for deeper content analysis
- Natural Language Processing libraries
- Sentiment analysis tools
- Machine learning models for personality prediction

## Persona Format Compliance

This tool generates personas that match professional UX research standards:

- **Visual personality scales** using Unicode bar charts
- **Quantified motivations** with percentage scores
- **Behavioral insights** with specific citations
- **Representative quotes** from actual user content
- **Professional formatting** suitable for stakeholder presentations

## Limitations

1. **Public Data Only**: Can only analyze publicly available posts and comments
2. **Rate Limiting**: Reddit API has rate limits that may affect large-scale analysis
3. **Privacy**: Respects user privacy by only analyzing public content
4. **Accuracy**: Analysis accuracy depends on available content volume and quality

## Error Handling

The script handles common scenarios:

- Invalid URL formats
- Private or deleted profiles
- Network connectivity issues
- Rate limiting from Reddit
- Empty or insufficient data

## Contributing

1. Follow PEP-8 style guidelines
2. Add type hints for new functions
3. Include docstrings for all methods
4. Add error handling for edge cases
5. Update tests for new features

## Legal and Ethical Considerations

- Only analyzes publicly available Reddit data
- Respects Reddit's Terms of Service
- Does not store or redistribute user data
- Intended for educational and research purposes
- Users should obtain appropriate permissions for commercial use

## Future Enhancements

- Integration with OpenAI API for LLM-powered analysis
- Machine learning models for personality prediction
- Web interface for easier usage
- Database storage for historical analysis
- Real-time monitoring capabilities
- Multi-platform social media analysis

## Support

For issues, questions, or contributions:

1. Check existing documentation
2. Review error messages and logs
3. Ensure dependencies are properly installed
4. Verify Reddit profile URLs are public and valid

## License

This project is intended for educational purposes. Please ensure compliance with Reddit's Terms of Service and applicable privacy laws when using this tool.