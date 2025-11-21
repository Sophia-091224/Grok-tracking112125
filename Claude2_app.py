import React, { useState, useCallback } from 'react';
import { Upload, FileJson, Eye, Settings, Zap, TrendingUp, AlertCircle, CheckCircle, BarChart3, Network, Sparkles } from 'lucide-react';

const FoodTraceabilityDashboard = () => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [jsonData, setJsonData] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [activeTab, setActiveTab] = useState('upload');
  const [selectedProvider, setSelectedProvider] = useState('OpenAI');
  const [selectedModel, setSelectedModel] = useState('gpt-4o');
  const [maxTokens, setMaxTokens] = useState(2000);
  const [temperature, setTemperature] = useState(0.2);
  const [analyzing, setAnalyzing] = useState(false);

  const modelOptions = {
    'OpenAI': ['gpt-4o', 'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo'],
    'Google Gemini': ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro'],
    'xAI Grok': ['grok-beta', 'grok-vision-beta']
  };

  const handleDragEnter = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      processFile(files[0]);
    }
  }, []);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      processFile(file);
    }
  };

  const processFile = (file) => {
    if (file.type !== 'application/json') {
      alert('Please upload a JSON file');
      return;
    }

    setUploadedFile(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        setJsonData(data);
        setActiveTab('preview');
      } catch (error) {
        alert('Invalid JSON file');
      }
    };
    reader.readAsText(file);
  };

  const handleAnalyze = () => {
    setAnalyzing(true);
    setTimeout(() => {
      setAnalyzing(false);
      setActiveTab('results');
    }, 2000);
  };

  const getDatasetStats = () => {
    if (!jsonData) return null;
    
    const isArray = Array.isArray(jsonData);
    const itemCount = isArray ? jsonData.length : Object.keys(jsonData).length;
    const hasTraceability = JSON.stringify(jsonData).includes('traceability');
    const hasBatches = JSON.stringify(jsonData).includes('batch');
    
    return { isArray, itemCount, hasTraceability, hasBatches };
  };

  const stats = getDatasetStats();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 text-white">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 -left-48 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 -right-48 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1s'}}></div>
      </div>

      {/* Header */}
      <div className="relative z-10 border-b border-purple-500/20 backdrop-blur-xl bg-slate-900/50">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-gradient-to-br from-purple-500 to-blue-500 rounded-2xl shadow-lg shadow-purple-500/50">
                <Sparkles className="w-8 h-8" />
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                  Food Traceability AI
                </h1>
                <p className="text-sm text-slate-400 mt-1">Powered by Multi-LLM Intelligence</p>
              </div>
            </div>
            <div className="flex gap-3">
              <button className="px-4 py-2 rounded-xl bg-slate-800/50 hover:bg-slate-700/50 border border-slate-700/50 transition-all duration-300 flex items-center gap-2">
                <Settings className="w-4 h-4" />
                Settings
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-12 gap-6">
          
          {/* Sidebar - AI Configuration */}
          <div className="col-span-12 lg:col-span-3 space-y-4">
            <div className="backdrop-blur-xl bg-slate-900/50 rounded-2xl border border-purple-500/20 p-6 shadow-2xl">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Zap className="w-5 h-5 text-purple-400" />
                AI Configuration
              </h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-slate-300 mb-2">Provider</label>
                  <select 
                    value={selectedProvider}
                    onChange={(e) => {
                      setSelectedProvider(e.target.value);
                      setSelectedModel(modelOptions[e.target.value][0]);
                    }}
                    className="w-full px-4 py-3 rounded-xl bg-slate-800/50 border border-slate-700/50 focus:border-purple-500/50 focus:outline-none transition-all duration-300"
                  >
                    {Object.keys(modelOptions).map(provider => (
                      <option key={provider} value={provider}>{provider}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm text-slate-300 mb-2">Model</label>
                  <select 
                    value={selectedModel}
                    onChange={(e) => setSelectedModel(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl bg-slate-800/50 border border-slate-700/50 focus:border-purple-500/50 focus:outline-none transition-all duration-300"
                  >
                    {modelOptions[selectedProvider].map(model => (
                      <option key={model} value={model}>{model}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm text-slate-300 mb-2">
                    Max Tokens: <span className="text-purple-400">{maxTokens}</span>
                  </label>
                  <input 
                    type="range" 
                    min="100" 
                    max="8192" 
                    step="100"
                    value={maxTokens}
                    onChange={(e) => setMaxTokens(parseInt(e.target.value))}
                    className="w-full accent-purple-500"
                  />
                </div>

                <div>
                  <label className="block text-sm text-slate-300 mb-2">
                    Temperature: <span className="text-purple-400">{temperature}</span>
                  </label>
                  <input 
                    type="range" 
                    min="0" 
                    max="1" 
                    step="0.1"
                    value={temperature}
                    onChange={(e) => setTemperature(parseFloat(e.target.value))}
                    className="w-full accent-purple-500"
                  />
                </div>
              </div>
            </div>

            {/* Stats Card */}
            {jsonData && (
              <div className="backdrop-blur-xl bg-slate-900/50 rounded-2xl border border-purple-500/20 p-6 shadow-2xl">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <BarChart3 className="w-5 h-5 text-blue-400" />
                  Dataset Stats
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-slate-400">Items</span>
                    <span className="font-semibold text-purple-400">{stats?.itemCount}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-slate-400">Type</span>
                    <span className="font-semibold text-blue-400">{stats?.isArray ? 'Array' : 'Object'}</span>
                  </div>
                  {stats?.hasTraceability && (
                    <div className="flex items-center gap-2 text-sm text-green-400">
                      <CheckCircle className="w-4 h-4" />
                      Traceability Data
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Main Area */}
          <div className="col-span-12 lg:col-span-9">
            
            {/* Tabs */}
            <div className="flex gap-2 mb-6">
              {['upload', 'preview', 'analyze', 'results'].map(tab => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  disabled={tab !== 'upload' && !jsonData}
                  className={`px-6 py-3 rounded-xl font-medium transition-all duration-300 ${
                    activeTab === tab 
                      ? 'bg-gradient-to-r from-purple-500 to-blue-500 shadow-lg shadow-purple-500/50' 
                      : 'bg-slate-800/50 hover:bg-slate-700/50 border border-slate-700/50'
                  } ${tab !== 'upload' && !jsonData ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  {tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>

            {/* Content Area */}
            <div className="backdrop-blur-xl bg-slate-900/50 rounded-2xl border border-purple-500/20 p-8 shadow-2xl min-h-[600px]">
              
              {/* Upload Tab */}
              {activeTab === 'upload' && (
                <div className="h-full flex flex-col items-center justify-center">
                  <div
                    onDragEnter={handleDragEnter}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    className={`w-full max-w-2xl border-2 border-dashed rounded-3xl p-12 text-center transition-all duration-300 ${
                      isDragging 
                        ? 'border-purple-500 bg-purple-500/10 scale-105' 
                        : 'border-slate-700 hover:border-purple-500/50 hover:bg-slate-800/30'
                    }`}
                  >
                    <Upload className={`w-20 h-20 mx-auto mb-6 transition-all duration-300 ${
                      isDragging ? 'text-purple-400 scale-110' : 'text-slate-500'
                    }`} />
                    <h3 className="text-2xl font-bold mb-3">Drop your dataset here</h3>
                    <p className="text-slate-400 mb-6">or click to browse your files</p>
                    <input
                      type="file"
                      accept=".json"
                      onChange={handleFileSelect}
                      className="hidden"
                      id="file-upload"
                    />
                    <label
                      htmlFor="file-upload"
                      className="inline-block px-8 py-4 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl font-semibold cursor-pointer hover:shadow-lg hover:shadow-purple-500/50 transition-all duration-300 hover:scale-105"
                    >
                      Choose JSON File
                    </label>
                    <div className="mt-8 flex items-center justify-center gap-6 text-sm text-slate-500">
                      <div className="flex items-center gap-2">
                        <FileJson className="w-4 h-4" />
                        JSON Format
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4" />
                        Secure Upload
                      </div>
                    </div>
                  </div>
                  
                  {uploadedFile && (
                    <div className="mt-8 p-6 bg-gradient-to-r from-green-500/10 to-blue-500/10 rounded-2xl border border-green-500/20 max-w-2xl w-full">
                      <div className="flex items-center gap-4">
                        <CheckCircle className="w-8 h-8 text-green-400" />
                        <div className="flex-1">
                          <p className="font-semibold text-green-400">File Uploaded Successfully</p>
                          <p className="text-sm text-slate-400 mt-1">{uploadedFile.name}</p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Preview Tab */}
              {activeTab === 'preview' && jsonData && (
                <div className="h-full">
                  <div className="flex items-center gap-3 mb-6">
                    <Eye className="w-6 h-6 text-purple-400" />
                    <h2 className="text-2xl font-bold">Dataset Preview</h2>
                  </div>
                  <div className="bg-slate-950/50 rounded-xl p-6 border border-slate-800 overflow-auto max-h-[500px]">
                    <pre className="text-sm text-slate-300 font-mono">
                      {JSON.stringify(jsonData, null, 2)}
                    </pre>
                  </div>
                </div>
              )}

              {/* Analyze Tab */}
              {activeTab === 'analyze' && jsonData && (
                <div className="h-full flex flex-col items-center justify-center">
                  <Network className="w-24 h-24 text-purple-400 mb-6 animate-pulse" />
                  <h2 className="text-3xl font-bold mb-4">Ready to Analyze</h2>
                  <p className="text-slate-400 mb-8 text-center max-w-md">
                    Your dataset is loaded and configured. Click below to start AI-powered analysis with {selectedProvider} ({selectedModel}).
                  </p>
                  <button
                    onClick={handleAnalyze}
                    disabled={analyzing}
                    className="px-12 py-5 bg-gradient-to-r from-purple-500 to-blue-500 rounded-2xl font-bold text-lg hover:shadow-2xl hover:shadow-purple-500/50 transition-all duration-300 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-3"
                  >
                    {analyzing ? (
                      <>
                        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Zap className="w-6 h-6" />
                        Run AI Analysis
                      </>
                    )}
                  </button>
                </div>
              )}

              {/* Results Tab */}
              {activeTab === 'results' && (
                <div className="h-full">
                  <div className="flex items-center gap-3 mb-6">
                    <TrendingUp className="w-6 h-6 text-green-400" />
                    <h2 className="text-2xl font-bold">Analysis Results</h2>
                  </div>
                  
                  <div className="space-y-6">
                    <div className="bg-gradient-to-br from-green-500/10 to-blue-500/10 rounded-2xl p-6 border border-green-500/20">
                      <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                        <CheckCircle className="w-5 h-5 text-green-400" />
                        Traceability Score: 8.5/10
                      </h3>
                      <p className="text-slate-300">
                        Your supply chain demonstrates strong traceability with comprehensive batch tracking and minimal time delays.
                      </p>
                    </div>

                    <div className="bg-slate-950/50 rounded-2xl p-6 border border-slate-800">
                      <h3 className="text-lg font-semibold mb-4 text-purple-400">Top 3 Risks Identified</h3>
                      <ul className="space-y-3">
                        <li className="flex items-start gap-3">
                          <AlertCircle className="w-5 h-5 text-yellow-400 mt-0.5" />
                          <div>
                            <p className="font-medium">Temperature Variation</p>
                            <p className="text-sm text-slate-400">2 batches showed temperature fluctuations during transport</p>
                          </div>
                        </li>
                        <li className="flex items-start gap-3">
                          <AlertCircle className="w-5 h-5 text-yellow-400 mt-0.5" />
                          <div>
                            <p className="font-medium">Time Delay</p>
                            <p className="text-sm text-slate-400">Average 4.2 hours between laying and collection</p>
                          </div>
                        </li>
                        <li className="flex items-start gap-3">
                          <AlertCircle className="w-5 h-5 text-yellow-400 mt-0.5" />
                          <div>
                            <p className="font-medium">Documentation Gap</p>
                            <p className="text-sm text-slate-400">3 records missing intermediate handler data</p>
                          </div>
                        </li>
                      </ul>
                    </div>

                    <button className="w-full py-4 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl font-semibold hover:shadow-lg hover:shadow-purple-500/50 transition-all duration-300">
                      Download Full Report
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FoodTraceabilityDashboard;
