'use client';

import { useQuery, useMutation } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { useState } from 'react';
import {
  Plus,
  Video,
  Image,
  FileText,
  Play,
  Edit,
  Trash2,
  Save,
  X,
  CheckCircle2,
  AlertCircle,
  Zap,
  Palette,
  Type,
  Mail,
  Phone,
  Globe,
  TrendingUp,
  BarChart3,
  Eye,
  Copy,
  Download,
  ChevronRight,
  ChevronLeft,
  ImageIcon,
  Film,
  Layers,
  Sparkles,
} from 'lucide-react';

interface Campaign {
  name: string;
  assets: Array<{
    id: number;
    title: string;
    type: string;
    platform: string;
    status: string;
  }>;
  asset_count: number;
  platforms: string[];
  status: string;
  created_at: string;
  updated_at: string;
}

interface AdAsset {
  id: number;
  title: string;
  type: string;
  platform: string;
  status: string;
  created_at: string;
}

export default function AdStudioPage() {
  const [activeSection, setActiveSection] = useState<'workspace' | 'copy' | 'video' | 'brand' | 'insights'>('workspace');
  const [showCopyComposer, setShowCopyComposer] = useState(false);
  const [showVideoBuilder, setShowVideoBuilder] = useState(false);
  const [videoStep, setVideoStep] = useState(1);
  
  // Copy composer state
  const [copyObjective, setCopyObjective] = useState('promotion');
  const [copyPlatform, setCopyPlatform] = useState('instagram');
  const [copyHeadline, setCopyHeadline] = useState('');
  const [copyDescription, setCopyDescription] = useState('');
  const [copyCta, setCopyCta] = useState('');
  const [useIntelligence, setUseIntelligence] = useState(false);
  const [campaignName, setCampaignName] = useState('');
  
  // Video builder state
  const [videoObjective, setVideoObjective] = useState('');
  const [videoPlatform, setVideoPlatform] = useState('');
  const [videoTemplate, setVideoTemplate] = useState('');
  const [videoHeadline, setVideoHeadline] = useState('');
  const [videoText, setVideoText] = useState('');
  const [videoCta, setVideoCta] = useState('');

  const { data: campaignsData } = useQuery<{ campaigns: Campaign[] }>({
    queryKey: ['ads-campaigns'],
    queryFn: async () => {
      const response = await api.get('/api/dashboard/ads/campaigns');
      return response.data;
    },
  });

  const { data: templatesData } = useQuery<{ templates: any }>({
    queryKey: ['ads-templates'],
    queryFn: async () => {
      const response = await api.get('/api/dashboard/ads/copy-templates');
      return response.data;
    },
  });

  const { data: intelligenceData } = useQuery<{ top_questions: any[]; high_performing_intents: any[]; frequently_asked: any[] }>({
    queryKey: ['ads-intelligence'],
    queryFn: async () => {
      const response = await api.get('/api/dashboard/ads/conversation-intelligence');
      return response.data;
    },
  });

  const { data: presetsData } = useQuery<{ presets: any }>({
    queryKey: ['ads-presets'],
    queryFn: async () => {
      const response = await api.get('/api/dashboard/ads/platform-presets');
      return response.data;
    },
  });

  const { data: videoTemplatesData } = useQuery<{ templates: any }>({
    queryKey: ['ads-video-templates'],
    queryFn: async () => {
      const response = await api.get('/api/dashboard/ads/video-templates');
      return response.data;
    },
  });

  const { data: brandData } = useQuery<{ logo: any; colors: any; fonts: any; contact: any; legal_disclaimer: string | null }>({
    queryKey: ['ads-brand'],
    queryFn: async () => {
      const response = await api.get('/api/dashboard/ads/brand-assets');
      return response.data;
    },
  });

  const { data: insightsData } = useQuery<{ total_assets: number; assets_by_type: any[]; assets_by_platform: any[]; assets_by_status: any[]; intent_linkage: string[] }>({
    queryKey: ['ads-insights'],
    queryFn: async () => {
      const response = await api.get('/api/dashboard/ads/usage-insights');
      return response.data;
    },
  });

  const generateCopyMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post('/api/dashboard/ads/generate-copy', data);
      return response.data;
    },
    onSuccess: (data) => {
      if (data.template_used) {
        if (copyHeadline === '') {
          setCopyHeadline(data.copy);
        } else if (copyDescription === '') {
          setCopyDescription(data.copy);
        }
      }
    },
  });

  const createAssetMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post('/api/dashboard/ads/assets', data);
      return response.data;
    },
    onSuccess: () => {
      setShowCopyComposer(false);
      setShowVideoBuilder(false);
      setVideoStep(1);
      // Reset form
      setCopyHeadline('');
      setCopyDescription('');
      setCopyCta('');
      setCampaignName('');
    },
  });

  const handleGenerateCopy = (type: 'headline' | 'description' | 'cta') => {
    generateCopyMutation.mutate({
      objective: copyObjective,
      platform: copyPlatform,
      template_type: type,
      use_intelligence: useIntelligence,
    });
  };

  const handleSaveCopy = () => {
    if (!copyHeadline || !campaignName) {
      alert('Please fill in headline and campaign name');
      return;
    }
    
    createAssetMutation.mutate({
      asset_type: 'ad_copy',
      title: copyHeadline.substring(0, 50),
      content: `${copyHeadline}\n\n${copyDescription}\n\n${copyCta}`,
      platform: copyPlatform,
      status: 'draft',
      campaign_name: campaignName,
    });
  };

  const handleSaveVideo = () => {
    if (!videoHeadline || !campaignName) {
      alert('Please complete all video steps');
      return;
    }
    
    createAssetMutation.mutate({
      asset_type: 'video',
      title: videoHeadline.substring(0, 50),
      content: JSON.stringify({
        objective: videoObjective,
        template: videoTemplate,
        headline: videoHeadline,
        text: videoText,
        cta: videoCta,
      }),
      platform: videoPlatform,
      status: 'draft',
      campaign_name: campaignName,
    });
  };

  const nextVideoStep = () => {
    if (videoStep < 6) {
      setVideoStep(videoStep + 1);
    }
  };

  const prevVideoStep = () => {
    if (videoStep > 1) {
      setVideoStep(videoStep - 1);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'published':
        return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      case 'draft':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400';
      case 'archived':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Ad & Video Creation Studio
          </h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Create professional ad copy and video assets with guided workflows
          </p>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => {
              setShowCopyComposer(true);
              setActiveSection('copy');
            }}
            className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
          >
            <FileText className="h-5 w-5 mr-2" />
            Create Ad Copy
          </button>
          <button
            onClick={() => {
              setShowVideoBuilder(true);
              setActiveSection('video');
            }}
            className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
          >
            <Video className="h-5 w-5 mr-2" />
            Create Video
          </button>
        </div>
      </div>

      {/* Section Navigation */}
      <div className="flex space-x-1 bg-gray-100 dark:bg-gray-800 p-1 rounded-lg">
        {[
          { id: 'workspace', label: 'Campaign Workspace', icon: Layers },
          { id: 'copy', label: 'Ad Copy', icon: FileText },
          { id: 'video', label: 'Video Builder', icon: Video },
          { id: 'brand', label: 'Brand Assets', icon: Palette },
          { id: 'insights', label: 'Insights', icon: BarChart3 },
        ].map((section) => (
          <button
            key={section.id}
            onClick={() => setActiveSection(section.id as any)}
            className={`flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeSection === section.id
                ? 'bg-white dark:bg-gray-700 text-primary-600 dark:text-primary-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
            }`}
          >
            <section.icon className="h-4 w-4" />
            <span className="hidden sm:inline">{section.label}</span>
          </button>
        ))}
      </div>

      {/* Campaign Workspace */}
      {activeSection === 'workspace' && (
        <div className="space-y-4">
          <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">
                Campaigns
              </h3>
              {campaignsData && campaignsData.campaigns.length > 0 ? (
                <div className="space-y-4">
                  {campaignsData.campaigns.map((campaign, idx) => (
                    <div
                      key={idx}
                      className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-200 dark:border-gray-600"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <div>
                          <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
                            {campaign.name}
                          </h4>
                          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                            {campaign.asset_count} assets • Created {new Date(campaign.created_at).toLocaleDateString()}
                          </p>
                        </div>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(campaign.status)}`}>
                          {campaign.status}
                        </span>
                      </div>
                      <div className="flex flex-wrap gap-2 mb-3">
                        {campaign.platforms.map((platform, pidx) => (
                          <span
                            key={pidx}
                            className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-primary-100 text-primary-800 dark:bg-primary-900/20 dark:text-primary-400 capitalize"
                          >
                            {platform}
                          </span>
                        ))}
                      </div>
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-gray-500 dark:text-gray-400">Assets:</span>
                          <span className="ml-2 font-medium text-gray-900 dark:text-white">
                            {campaign.asset_count}
                          </span>
                        </div>
                        <div>
                          <span className="text-gray-500 dark:text-gray-400">Last Updated:</span>
                          <span className="ml-2 font-medium text-gray-900 dark:text-white">
                            {new Date(campaign.updated_at).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <Layers className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500 dark:text-gray-400">
                    No campaigns yet. Create your first ad or video to get started.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Ad Copy Composer */}
      {activeSection === 'copy' && (
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">
                Ad Copy Composer
              </h3>
              {showCopyComposer && (
                <button
                  onClick={() => setShowCopyComposer(false)}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <X className="h-5 w-5" />
                </button>
              )}
            </div>

            {!showCopyComposer ? (
              <div className="text-center py-12">
                <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500 dark:text-gray-400 mb-4">
                  Create platform-optimized ad copy using templates and conversation intelligence
                </p>
                <button
                  onClick={() => setShowCopyComposer(true)}
                  className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
                >
                  <Plus className="h-5 w-5 mr-2" />
                  Start Composing
                </button>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Campaign Name */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Campaign Name
                  </label>
                  <input
                    type="text"
                    value={campaignName}
                    onChange={(e) => setCampaignName(e.target.value)}
                    placeholder="e.g., Summer Sale 2024"
                    className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  />
                </div>

                {/* Objective & Platform */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Objective
                    </label>
                    <select
                      value={copyObjective}
                      onChange={(e) => setCopyObjective(e.target.value)}
                      className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    >
                      <option value="promotion">Promotion</option>
                      <option value="announcement">Announcement</option>
                      <option value="offer">Offer</option>
                      <option value="product_highlight">Product Highlight</option>
                      <option value="follow_up">Follow-Up</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Platform
                    </label>
                    <select
                      value={copyPlatform}
                      onChange={(e) => setCopyPlatform(e.target.value)}
                      className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    >
                      <option value="instagram">Instagram</option>
                      <option value="whatsapp_status">WhatsApp Status</option>
                      <option value="facebook">Facebook</option>
                    </select>
                  </div>
                </div>

                {/* Platform Preset Info */}
                {presetsData && presetsData.presets[copyPlatform] && (
                  <div className="p-3 bg-blue-50 dark:bg-blue-900/10 rounded-lg">
                    <p className="text-sm text-gray-700 dark:text-gray-300">
                      <strong>Tone:</strong> {presetsData.presets[copyPlatform].tone} •{' '}
                      <strong>Max Length:</strong> {presetsData.presets[copyPlatform].max_length} characters
                    </p>
                  </div>
                )}

                {/* Conversation Intelligence */}
                <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                  <div className="flex items-center justify-between mb-3">
                    <label className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                      <input
                        type="checkbox"
                        checked={useIntelligence}
                        onChange={(e) => setUseIntelligence(e.target.checked)}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                      Use Conversation Intelligence
                    </label>
                  </div>
                  {useIntelligence && intelligenceData && (
                    <div className="mt-3 space-y-2 text-sm text-gray-600 dark:text-gray-400">
                      {intelligenceData.top_questions.length > 0 && (
                        <div>
                          <strong>Top Question:</strong> {intelligenceData.top_questions[0].question.substring(0, 80)}...
                        </div>
                      )}
                      {intelligenceData.high_performing_intents.length > 0 && (
                        <div>
                          <strong>Top Intent:</strong> {intelligenceData.high_performing_intents[0].intent}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Headline */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      Headline
                    </label>
                    <button
                      onClick={() => handleGenerateCopy('headline')}
                      className="text-xs text-primary-600 hover:text-primary-700 dark:text-primary-400"
                    >
                      Generate from Template
                    </button>
                  </div>
                  <textarea
                    value={copyHeadline}
                    onChange={(e) => setCopyHeadline(e.target.value)}
                    rows={2}
                    placeholder="Enter headline or generate from template..."
                    className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  />
                </div>

                {/* Description */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      Description
                    </label>
                    <button
                      onClick={() => handleGenerateCopy('description')}
                      className="text-xs text-primary-600 hover:text-primary-700 dark:text-primary-400"
                    >
                      Generate from Template
                    </button>
                  </div>
                  <textarea
                    value={copyDescription}
                    onChange={(e) => setCopyDescription(e.target.value)}
                    rows={4}
                    placeholder="Enter description or generate from template..."
                    className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  />
                </div>

                {/* CTA */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      Call-to-Action
                    </label>
                    <button
                      onClick={() => handleGenerateCopy('cta')}
                      className="text-xs text-primary-600 hover:text-primary-700 dark:text-primary-400"
                    >
                      Generate from Template
                    </button>
                  </div>
                  <input
                    type="text"
                    value={copyCta}
                    onChange={(e) => setCopyCta(e.target.value)}
                    placeholder="e.g., Shop Now, Learn More"
                    className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  />
                </div>

                {/* Preview */}
                <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                  <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-2">Preview</h4>
                  <div className="space-y-2 text-sm">
                    <div className="font-semibold text-gray-900 dark:text-white">{copyHeadline || 'Headline...'}</div>
                    <div className="text-gray-600 dark:text-gray-400">{copyDescription || 'Description...'}</div>
                    <div className="text-primary-600 dark:text-primary-400 font-medium">{copyCta || 'CTA...'}</div>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex justify-end gap-2">
                  <button
                    onClick={() => setShowCopyComposer(false)}
                    className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSaveCopy}
                    disabled={createAssetMutation.isPending}
                    className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
                  >
                    <Save className="h-4 w-4 mr-2" />
                    Save as Draft
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Video Asset Builder */}
      {activeSection === 'video' && (
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">
                Video Asset Builder
              </h3>
              {showVideoBuilder && (
                <button
                  onClick={() => {
                    setShowVideoBuilder(false);
                    setVideoStep(1);
                  }}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <X className="h-5 w-5" />
                </button>
              )}
            </div>

            {!showVideoBuilder ? (
              <div className="text-center py-12">
                <Video className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500 dark:text-gray-400 mb-4">
                  Create short promotional videos using guided templates
                </p>
                <button
                  onClick={() => setShowVideoBuilder(true)}
                  className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
                >
                  <Plus className="h-5 w-5 mr-2" />
                  Start Building
                </button>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Progress Indicator */}
                <div className="flex items-center justify-between mb-6">
                  {[1, 2, 3, 4, 5, 6].map((step) => (
                    <div key={step} className="flex items-center flex-1">
                      <div
                        className={`flex items-center justify-center w-8 h-8 rounded-full ${
                          step <= videoStep
                            ? 'bg-primary-600 text-white'
                            : 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
                        }`}
                      >
                        {step}
                      </div>
                      {step < 6 && (
                        <div
                          className={`flex-1 h-1 mx-2 ${
                            step < videoStep ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'
                          }`}
                        />
                      )}
                    </div>
                  ))}
                </div>

                {/* Step 1: Objective */}
                {videoStep === 1 && (
                  <div className="space-y-4">
                    <h4 className="text-md font-medium text-gray-900 dark:text-white">Select Objective</h4>
                    <div className="grid grid-cols-2 gap-4">
                      {['Promotion', 'Announcement', 'Offer', 'Brand Highlight'].map((obj) => (
                        <button
                          key={obj}
                          onClick={() => {
                            setVideoObjective(obj.toLowerCase());
                            nextVideoStep();
                          }}
                          className="p-4 border-2 border-gray-200 dark:border-gray-600 rounded-lg hover:border-primary-500 dark:hover:border-primary-500 text-left"
                        >
                          <div className="font-medium text-gray-900 dark:text-white">{obj}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Step 2: Platform */}
                {videoStep === 2 && (
                  <div className="space-y-4">
                    <h4 className="text-md font-medium text-gray-900 dark:text-white">Select Platform</h4>
                    <div className="grid grid-cols-3 gap-4">
                      {['Instagram', 'WhatsApp Status', 'Facebook'].map((platform) => (
                        <button
                          key={platform}
                          onClick={() => {
                            setVideoPlatform(platform.toLowerCase().replace(' ', '_'));
                            nextVideoStep();
                          }}
                          className="p-4 border-2 border-gray-200 dark:border-gray-600 rounded-lg hover:border-primary-500 dark:hover:border-primary-500 text-center"
                        >
                          <div className="font-medium text-gray-900 dark:text-white">{platform}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Step 3: Template */}
                {videoStep === 3 && videoTemplatesData && (
                  <div className="space-y-4">
                    <h4 className="text-md font-medium text-gray-900 dark:text-white">Choose Template</h4>
                    <div className="space-y-3">
                      {Object.entries(videoTemplatesData.templates).map(([key, template]: [string, any]) => (
                        <button
                          key={key}
                          onClick={() => {
                            setVideoTemplate(key);
                            nextVideoStep();
                          }}
                          className="w-full p-4 border-2 border-gray-200 dark:border-gray-600 rounded-lg hover:border-primary-500 dark:hover:border-primary-500 text-left"
                        >
                          <div className="font-medium text-gray-900 dark:text-white">{template.name}</div>
                          <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                            {template.description} • {template.duration}s
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Step 4: Content */}
                {videoStep === 4 && (
                  <div className="space-y-4">
                    <h4 className="text-md font-medium text-gray-900 dark:text-white">Insert Content</h4>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Campaign Name
                      </label>
                      <input
                        type="text"
                        value={campaignName}
                        onChange={(e) => setCampaignName(e.target.value)}
                        placeholder="e.g., Summer Sale 2024"
                        className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Headline
                      </label>
                      <input
                        type="text"
                        value={videoHeadline}
                        onChange={(e) => setVideoHeadline(e.target.value)}
                        placeholder="Main headline text"
                        className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Supporting Text
                      </label>
                      <textarea
                        value={videoText}
                        onChange={(e) => setVideoText(e.target.value)}
                        rows={3}
                        placeholder="Additional text or description"
                        className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Call-to-Action
                      </label>
                      <input
                        type="text"
                        value={videoCta}
                        onChange={(e) => setVideoCta(e.target.value)}
                        placeholder="e.g., Shop Now"
                        className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500"
                      />
                    </div>
                  </div>
                )}

                {/* Step 5: Visual Assets */}
                {videoStep === 5 && (
                  <div className="space-y-4">
                    <h4 className="text-md font-medium text-gray-900 dark:text-white">Add Visual Assets</h4>
                    <div className="p-8 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg text-center">
                      <ImageIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
                        Upload images or videos for your video asset
                      </p>
                      <button className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700">
                        <Plus className="h-4 w-4 mr-2" />
                        Upload Assets
                      </button>
                    </div>
                    <div className="p-4 bg-blue-50 dark:bg-blue-900/10 rounded-lg">
                      <p className="text-sm text-gray-700 dark:text-gray-300">
                        💡 Tip: Use brand assets from the Brand Manager for consistency
                      </p>
                    </div>
                  </div>
                )}

                {/* Step 6: Preview & Export */}
                {videoStep === 6 && (
                  <div className="space-y-4">
                    <h4 className="text-md font-medium text-gray-900 dark:text-white">Preview & Export</h4>
                    <div className="p-8 bg-gray-50 dark:bg-gray-700/50 rounded-lg border-2 border-dashed border-gray-300 dark:border-gray-600 text-center">
                      <Film className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
                        Video Preview
                      </p>
                      <div className="text-xs text-gray-400 dark:text-gray-500">
                        Template: {videoTemplate} • Platform: {videoPlatform} • Duration: 10s
                      </div>
                    </div>
                    <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                      <h5 className="text-sm font-medium text-gray-900 dark:text-white mb-2">Export Formats</h5>
                      <div className="flex gap-2">
                        <button className="px-3 py-1 text-xs border border-gray-300 dark:border-gray-600 rounded-md">
                          MP4
                        </button>
                        <button className="px-3 py-1 text-xs border border-gray-300 dark:border-gray-600 rounded-md">
                          Square
                        </button>
                        <button className="px-3 py-1 text-xs border border-gray-300 dark:border-gray-600 rounded-md">
                          Vertical
                        </button>
                      </div>
                    </div>
                  </div>
                )}

                {/* Navigation */}
                {showVideoBuilder && (
                  <div className="flex justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
                    <button
                      onClick={prevVideoStep}
                      disabled={videoStep === 1}
                      className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50"
                    >
                      <ChevronLeft className="h-4 w-4 mr-2" />
                      Previous
                    </button>
                    {videoStep < 6 ? (
                      <button
                        onClick={nextVideoStep}
                        className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
                      >
                        Next
                        <ChevronRight className="h-4 w-4 ml-2" />
                      </button>
                    ) : (
                      <button
                        onClick={handleSaveVideo}
                        disabled={createAssetMutation.isPending}
                        className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
                      >
                        <Save className="h-4 w-4 mr-2" />
                        Save as Draft
                      </button>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Brand Asset Manager */}
      {activeSection === 'brand' && (
        <div className="space-y-4">
          <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">
                Brand Assets
              </h3>
              {brandData && (
                <div className="space-y-6">
                  {/* Logo */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3">Logo</h4>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg text-center">
                        <ImageIcon className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                        <p className="text-xs text-gray-500 dark:text-gray-400">Primary Logo</p>
                        <button className="mt-2 text-xs text-primary-600 hover:text-primary-700">
                          Upload
                        </button>
                      </div>
                      <div className="p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg text-center">
                        <ImageIcon className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                        <p className="text-xs text-gray-500 dark:text-gray-400">Secondary Logo</p>
                        <button className="mt-2 text-xs text-primary-600 hover:text-primary-700">
                          Upload
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Colors */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3">Brand Colors</h4>
                    <div className="grid grid-cols-3 gap-4">
                      {Object.entries(brandData.colors).map(([name, color]: [string, any]) => (
                        <div key={name} className="text-center">
                          <div
                            className="w-full h-16 rounded-lg mb-2 border border-gray-200 dark:border-gray-700"
                            style={{ backgroundColor: color }}
                          />
                          <p className="text-xs font-medium text-gray-900 dark:text-white capitalize">{name}</p>
                          <p className="text-xs text-gray-500 dark:text-gray-400">{color}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Fonts */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3">Typography</h4>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                        <span className="text-sm text-gray-700 dark:text-gray-300">Heading Font</span>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                          {brandData.fonts.heading}
                        </span>
                      </div>
                      <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                        <span className="text-sm text-gray-700 dark:text-gray-300">Body Font</span>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                          {brandData.fonts.body}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Contact */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3">Contact Details</h4>
                    <div className="space-y-2">
                      <div className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                        <Phone className="h-4 w-4 text-gray-400" />
                        <input
                          type="text"
                          placeholder="Phone number"
                          className="flex-1 bg-transparent border-none text-sm text-gray-900 dark:text-white"
                        />
                      </div>
                      <div className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                        <Mail className="h-4 w-4 text-gray-400" />
                        <input
                          type="email"
                          placeholder="Email address"
                          className="flex-1 bg-transparent border-none text-sm text-gray-900 dark:text-white"
                        />
                      </div>
                      <div className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                        <Globe className="h-4 w-4 text-gray-400" />
                        <input
                          type="url"
                          placeholder="Website URL"
                          className="flex-1 bg-transparent border-none text-sm text-gray-900 dark:text-white"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Legal Disclaimer */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3">Legal Disclaimer</h4>
                    <textarea
                      rows={3}
                      placeholder="Enter legal disclaimer text..."
                      className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    />
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Performance & Usage Insights */}
      {activeSection === 'insights' && insightsData && (
        <div className="space-y-4">
          <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">
                Usage Insights
              </h3>
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                  <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Total Assets</p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                    {insightsData.total_assets}
                  </p>
                </div>
                <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                  <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Intent Linkage</p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                    {insightsData.intent_linkage.length}
                  </p>
                </div>
              </div>

              {/* Assets by Type */}
              <div className="mb-6">
                <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3">Assets by Type</h4>
                <div className="space-y-2">
                  {insightsData.assets_by_type.map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                      <span className="text-sm text-gray-700 dark:text-gray-300 capitalize">{item.type}</span>
                      <span className="text-sm font-medium text-gray-900 dark:text-white">{item.count}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Assets by Platform */}
              <div className="mb-6">
                <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3">Assets by Platform</h4>
                <div className="space-y-2">
                  {insightsData.assets_by_platform.map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                      <span className="text-sm text-gray-700 dark:text-gray-300 capitalize">{item.platform}</span>
                      <span className="text-sm font-medium text-gray-900 dark:text-white">{item.count}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Assets by Status */}
              <div>
                <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3">Assets by Status</h4>
                <div className="space-y-2">
                  {insightsData.assets_by_status.map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                      <span className="text-sm text-gray-700 dark:text-gray-300 capitalize">{item.status}</span>
                      <span className="text-sm font-medium text-gray-900 dark:text-white">{item.count}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
