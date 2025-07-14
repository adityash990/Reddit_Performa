import React, { useState } from 'react';
import { User, FileText, Download, Search, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';
import RedditScraper from './components/RedditScraper';
import PersonaDisplay from './components/PersonaDisplay';
import { PersonaData } from './types/persona';

function App() {
  const [url, setUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [persona, setPersona] = useState<PersonaData | null>(null);
  const [error, setError] = useState('');

  const validateRedditUrl = (url: string): boolean => {
    const redditUserPattern = /^https?:\/\/(www\.)?reddit\.com\/user\/[a-zA-Z0-9_-]+\/?$/;
    return redditUserPattern.test(url);
  };

  const handleAnalyze = async () => {
    if (!url) {
      setError('Please enter a Reddit profile URL');
      return;
    }

    if (!validateRedditUrl(url)) {
      setError('Please enter a valid Reddit user profile URL (e.g., https://www.reddit.com/user/username/)');
      return;
    }

    setError('');
    setIsAnalyzing(true);
    setPersona(null);

    try {
      const scraper = new RedditScraper();
      const personaData = await scraper.generatePersona(url);
      setPersona(personaData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while analyzing the profile');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleDownload = () => {
    if (!persona) return;

    const content = generatePersonaReport(persona);
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${persona.username}_persona.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const generatePersonaReport = (persona: PersonaData): string => {
    let report = `REDDIT USER PERSONA REPORT\n`;
    report += `================================\n\n`;
    report += `Username: ${persona.username}\n`;
    report += `Profile URL: ${persona.profileUrl}\n`;
    report += `Analysis Date: ${new Date().toLocaleDateString()}\n`;
    report += `Posts Analyzed: ${persona.totalPosts}\n`;
    report += `Comments Analyzed: ${persona.totalComments}\n\n`;

    report += `DEMOGRAPHICS\n`;
    report += `============\n`;
    report += `Age: ${persona.demographics.age}\n`;
    report += `Gender: ${persona.demographics.gender}\n`;
    report += `Location: ${persona.demographics.location}\n`;
    report += `Occupation: ${persona.demographics.occupation}\n\n`;

    report += `INTERESTS & HOBBIES\n`;
    report += `==================\n`;
    persona.interests.forEach((interest, index) => {
      report += `${index + 1}. ${interest.category}: ${interest.description}\n`;
      report += `   Sources: ${interest.sources.join(', ')}\n\n`;
    });

    report += `PERSONALITY TRAITS\n`;
    report += `==================\n`;
    persona.personality.forEach((trait, index) => {
      report += `${index + 1}. ${trait.trait}: ${trait.description}\n`;
      report += `   Evidence: ${trait.evidence.join(', ')}\n\n`;
    });

    report += `COMMUNICATION STYLE\n`;
    report += `===================\n`;
    report += `Tone: ${persona.communicationStyle.tone}\n`;
    report += `Formality: ${persona.communicationStyle.formality}\n`;
    report += `Engagement: ${persona.communicationStyle.engagement}\n`;
    report += `Common Phrases: ${persona.communicationStyle.commonPhrases.join(', ')}\n\n`;

    report += `VALUES & BELIEFS\n`;
    report += `================\n`;
    persona.values.forEach((value, index) => {
      report += `${index + 1}. ${value.value}: ${value.description}\n`;
      report += `   Supporting Posts: ${value.supportingPosts.join(', ')}\n\n`;
    });

    report += `BEHAVIORAL PATTERNS\n`;
    report += `===================\n`;
    report += `Activity Level: ${persona.behaviorPatterns.activityLevel}\n`;
    report += `Posting Frequency: ${persona.behaviorPatterns.postingFrequency}\n`;
    report += `Peak Activity Times: ${persona.behaviorPatterns.peakTimes.join(', ')}\n`;
    report += `Preferred Subreddits: ${persona.behaviorPatterns.preferredSubreddits.join(', ')}\n\n`;

    report += `GOALS & MOTIVATIONS\n`;
    report += `==================\n`;
    persona.goals.forEach((goal, index) => {
      report += `${index + 1}. ${goal.goal}: ${goal.description}\n`;
      report += `   Indicators: ${goal.indicators.join(', ')}\n\n`;
    });

    return report;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <User className="h-12 w-12 text-purple-400 mr-3" />
            <h1 className="text-4xl font-bold text-white">Reddit Persona Generator</h1>
          </div>
          <p className="text-gray-300 text-lg max-w-2xl mx-auto">
            Analyze Reddit user profiles to generate detailed personas with AI-powered insights and citations
          </p>
        </div>

        {/* Input Section */}
        <div className="max-w-4xl mx-auto mb-8">
          <div className="bg-gray-800 rounded-xl shadow-2xl p-8 border border-gray-700">
            <div className="flex flex-col space-y-6">
              <div>
                <label htmlFor="reddit-url" className="block text-sm font-medium text-gray-300 mb-2">
                  Reddit Profile URL
                </label>
                <div className="relative">
                  <input
                    id="reddit-url"
                    type="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://www.reddit.com/user/username/"
                    className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                    disabled={isAnalyzing}
                  />
                  <Search className="absolute right-3 top-3 h-5 w-5 text-gray-400" />
                </div>
                {error && (
                  <div className="mt-2 flex items-center text-red-400 text-sm">
                    <AlertCircle className="h-4 w-4 mr-1" />
                    {error}
                  </div>
                )}
              </div>

              <button
                onClick={handleAnalyze}
                disabled={isAnalyzing || !url}
                className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center space-x-2"
              >
                {isAnalyzing ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    <span>Analyzing Profile...</span>
                  </>
                ) : (
                  <>
                    <FileText className="h-5 w-5" />
                    <span>Generate Persona</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Results Section */}
        {persona && (
          <div className="max-w-6xl mx-auto">
            <div className="bg-gray-800 rounded-xl shadow-2xl border border-gray-700 overflow-hidden">
              <div className="p-6 border-b border-gray-700 flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <CheckCircle className="h-6 w-6 text-green-400" />
                  <h2 className="text-2xl font-bold text-white">Persona Analysis Complete</h2>
                </div>
                <button
                  onClick={handleDownload}
                  className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200 flex items-center space-x-2"
                >
                  <Download className="h-4 w-4" />
                  <span>Download Report</span>
                </button>
              </div>
              <PersonaDisplay persona={persona} />
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 text-gray-400">
          <p className="text-sm">
            This tool analyzes publicly available Reddit data to generate user personas.
            <br />
            Please respect user privacy and Reddit's terms of service.
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;