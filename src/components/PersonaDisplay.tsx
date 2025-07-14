import React, { useState } from 'react';
import { ChevronDown, ChevronRight, User, MapPin, Briefcase, Heart, MessageSquare, Target, TrendingUp, Clock, ExternalLink } from 'lucide-react';
import { PersonaData } from '../types/persona';

interface PersonaDisplayProps {
  persona: PersonaData;
}

interface ExpandableSection {
  [key: string]: boolean;
}

const PersonaDisplay: React.FC<PersonaDisplayProps> = ({ persona }) => {
  const [expandedSections, setExpandedSections] = useState<ExpandableSection>({
    demographics: true,
    interests: true,
    personality: false,
    communication: false,
    values: false,
    behavior: false,
    goals: false
  });

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const SectionHeader: React.FC<{ 
    title: string; 
    icon: React.ReactNode; 
    sectionKey: string;
    count?: number;
  }> = ({ title, icon, sectionKey, count }) => (
    <button
      onClick={() => toggleSection(sectionKey)}
      className="w-full flex items-center justify-between p-4 bg-gray-700 hover:bg-gray-650 transition-colors duration-200 rounded-lg mb-4"
    >
      <div className="flex items-center space-x-3">
        {icon}
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        {count && (
          <span className="bg-purple-600 text-white text-xs px-2 py-1 rounded-full">
            {count}
          </span>
        )}
      </div>
      {expandedSections[sectionKey] ? (
        <ChevronDown className="h-5 w-5 text-gray-400" />
      ) : (
        <ChevronRight className="h-5 w-5 text-gray-400" />
      )}
    </button>
  );

  const CitationLink: React.FC<{ source: string }> = ({ source }) => (
    <span className="inline-flex items-center bg-blue-600 text-white text-xs px-2 py-1 rounded-md mr-1 mb-1 hover:bg-blue-700 transition-colors cursor-pointer">
      {source}
      <ExternalLink className="h-3 w-3 ml-1" />
    </span>
  );

  return (
    <div className="p-6 space-y-6">
      {/* Profile Summary */}
      <div className="bg-gradient-to-r from-purple-700 to-blue-700 rounded-lg p-6 text-white">
        <div className="flex items-center space-x-4 mb-4">
          <div className="bg-white bg-opacity-20 rounded-full p-3">
            <User className="h-8 w-8" />
          </div>
          <div>
            <h2 className="text-2xl font-bold">u/{persona.username}</h2>
            <p className="text-purple-200">
              {persona.totalPosts} posts • {persona.totalComments} comments analyzed
            </p>
          </div>
        </div>
      </div>

      {/* Demographics */}
      <div>
        <SectionHeader 
          title="Demographics" 
          icon={<User className="h-5 w-5 text-purple-400" />}
          sectionKey="demographics"
        />
        {expandedSections.demographics && (
          <div className="bg-gray-750 rounded-lg p-6 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center space-x-3">
                <Clock className="h-4 w-4 text-gray-400" />
                <span className="text-gray-300">Age: </span>
                <span className="text-white font-medium">{persona.demographics.age}</span>
              </div>
              <div className="flex items-center space-x-3">
                <User className="h-4 w-4 text-gray-400" />
                <span className="text-gray-300">Gender: </span>
                <span className="text-white font-medium">{persona.demographics.gender}</span>
              </div>
              <div className="flex items-center space-x-3">
                <MapPin className="h-4 w-4 text-gray-400" />
                <span className="text-gray-300">Location: </span>
                <span className="text-white font-medium">{persona.demographics.location}</span>
              </div>
              <div className="flex items-center space-x-3">
                <Briefcase className="h-4 w-4 text-gray-400" />
                <span className="text-gray-300">Occupation: </span>
                <span className="text-white font-medium">{persona.demographics.occupation}</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Interests */}
      <div>
        <SectionHeader 
          title="Interests & Hobbies" 
          icon={<Heart className="h-5 w-5 text-red-400" />}
          sectionKey="interests"
          count={persona.interests.length}
        />
        {expandedSections.interests && (
          <div className="bg-gray-750 rounded-lg p-6 space-y-6">
            {persona.interests.map((interest, index) => (
              <div key={index} className="border-b border-gray-600 last:border-b-0 pb-4 last:pb-0">
                <h4 className="text-lg font-semibold text-white mb-2">{interest.category}</h4>
                <p className="text-gray-300 mb-3">{interest.description}</p>
                <div className="flex flex-wrap">
                  <span className="text-sm text-gray-400 mr-2">Sources:</span>
                  {interest.sources.map((source, idx) => (
                    <CitationLink key={idx} source={source} />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Personality */}
      <div>
        <SectionHeader 
          title="Personality Traits" 
          icon={<TrendingUp className="h-5 w-5 text-green-400" />}
          sectionKey="personality"
          count={persona.personality.length}
        />
        {expandedSections.personality && (
          <div className="bg-gray-750 rounded-lg p-6 space-y-6">
            {persona.personality.map((trait, index) => (
              <div key={index} className="border-b border-gray-600 last:border-b-0 pb-4 last:pb-0">
                <h4 className="text-lg font-semibold text-white mb-2">{trait.trait}</h4>
                <p className="text-gray-300 mb-3">{trait.description}</p>
                <div className="flex flex-wrap">
                  <span className="text-sm text-gray-400 mr-2">Evidence:</span>
                  {trait.evidence.map((evidence, idx) => (
                    <span key={idx} className="bg-green-600 text-white text-xs px-2 py-1 rounded-md mr-1 mb-1">
                      {evidence}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Communication Style */}
      <div>
        <SectionHeader 
          title="Communication Style" 
          icon={<MessageSquare className="h-5 w-5 text-blue-400" />}
          sectionKey="communication"
        />
        {expandedSections.communication && (
          <div className="bg-gray-750 rounded-lg p-6 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span className="text-gray-400 text-sm">Tone:</span>
                <p className="text-white font-medium">{persona.communicationStyle.tone}</p>
              </div>
              <div>
                <span className="text-gray-400 text-sm">Formality:</span>
                <p className="text-white font-medium">{persona.communicationStyle.formality}</p>
              </div>
              <div>
                <span className="text-gray-400 text-sm">Engagement:</span>
                <p className="text-white font-medium">{persona.communicationStyle.engagement}</p>
              </div>
            </div>
            <div>
              <span className="text-gray-400 text-sm">Common Phrases:</span>
              <div className="flex flex-wrap mt-2">
                {persona.communicationStyle.commonPhrases.map((phrase, idx) => (
                  <span key={idx} className="bg-blue-600 text-white text-xs px-2 py-1 rounded-md mr-1 mb-1">
                    "{phrase}"
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Values */}
      <div>
        <SectionHeader 
          title="Values & Beliefs" 
          icon={<Heart className="h-5 w-5 text-pink-400" />}
          sectionKey="values"
          count={persona.values.length}
        />
        {expandedSections.values && (
          <div className="bg-gray-750 rounded-lg p-6 space-y-6">
            {persona.values.map((value, index) => (
              <div key={index} className="border-b border-gray-600 last:border-b-0 pb-4 last:pb-0">
                <h4 className="text-lg font-semibold text-white mb-2">{value.value}</h4>
                <p className="text-gray-300 mb-3">{value.description}</p>
                <div className="flex flex-wrap">
                  <span className="text-sm text-gray-400 mr-2">Supporting Posts:</span>
                  {value.supportingPosts.map((post, idx) => (
                    <CitationLink key={idx} source={post} />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Behavior Patterns */}
      <div>
        <SectionHeader 
          title="Behavioral Patterns" 
          icon={<TrendingUp className="h-5 w-5 text-yellow-400" />}
          sectionKey="behavior"
        />
        {expandedSections.behavior && (
          <div className="bg-gray-750 rounded-lg p-6 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span className="text-gray-400 text-sm">Activity Level:</span>
                <p className="text-white font-medium">{persona.behaviorPatterns.activityLevel}</p>
              </div>
              <div>
                <span className="text-gray-400 text-sm">Posting Frequency:</span>
                <p className="text-white font-medium">{persona.behaviorPatterns.postingFrequency}</p>
              </div>
            </div>
            <div>
              <span className="text-gray-400 text-sm">Peak Activity Times:</span>
              <div className="flex flex-wrap mt-2">
                {persona.behaviorPatterns.peakTimes.map((time, idx) => (
                  <span key={idx} className="bg-yellow-600 text-white text-xs px-2 py-1 rounded-md mr-1 mb-1">
                    {time}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <span className="text-gray-400 text-sm">Preferred Subreddits:</span>
              <div className="flex flex-wrap mt-2">
                {persona.behaviorPatterns.preferredSubreddits.map((subreddit, idx) => (
                  <span key={idx} className="bg-orange-600 text-white text-xs px-2 py-1 rounded-md mr-1 mb-1">
                    r/{subreddit}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Goals */}
      <div>
        <SectionHeader 
          title="Goals & Motivations" 
          icon={<Target className="h-5 w-5 text-green-400" />}
          sectionKey="goals"
          count={persona.goals.length}
        />
        {expandedSections.goals && (
          <div className="bg-gray-750 rounded-lg p-6 space-y-6">
            {persona.goals.map((goal, index) => (
              <div key={index} className="border-b border-gray-600 last:border-b-0 pb-4 last:pb-0">
                <h4 className="text-lg font-semibold text-white mb-2">{goal.goal}</h4>
                <p className="text-gray-300 mb-3">{goal.description}</p>
                <div className="flex flex-wrap">
                  <span className="text-sm text-gray-400 mr-2">Indicators:</span>
                  {goal.indicators.map((indicator, idx) => (
                    <span key={idx} className="bg-green-600 text-white text-xs px-2 py-1 rounded-md mr-1 mb-1">
                      {indicator}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default PersonaDisplay;