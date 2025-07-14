export interface PersonaData {
  username: string;
  profileUrl: string;
  totalPosts: number;
  totalComments: number;
  demographics: {
    age: string;
    gender: string;
    location: string;
    occupation: string;
  };
  interests: Array<{
    category: string;
    description: string;
    sources: string[];
  }>;
  personality: Array<{
    trait: string;
    description: string;
    evidence: string[];
  }>;
  communicationStyle: {
    tone: string;
    formality: string;
    engagement: string;
    commonPhrases: string[];
  };
  values: Array<{
    value: string;
    description: string;
    supportingPosts: string[];
  }>;
  behaviorPatterns: {
    activityLevel: string;
    postingFrequency: string;
    peakTimes: string[];
    preferredSubreddits: string[];
  };
  goals: Array<{
    goal: string;
    description: string;
    indicators: string[];
  }>;
}

export interface RedditPost {
  id: string;
  title: string;
  content: string;
  subreddit: string;
  score: number;
  created: string;
  url: string;
}

export interface RedditComment {
  id: string;
  content: string;
  subreddit: string;
  score: number;
  created: string;
  parentPost: string;
  url: string;
}