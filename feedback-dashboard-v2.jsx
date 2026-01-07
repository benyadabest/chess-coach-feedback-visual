import React, { useState, useMemo } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, LineChart, Line, ComposedChart } from 'recharts';

// Scores data
const scoresData = [
  { timestamp: "2026-01-06", name: "user_feedback", value: 1, userId: "U095XD7U9M0", channel: "C0A4SNLDKHQ" },
  { timestamp: "2026-01-05", name: "user_feedback", value: -1, userId: "U02NA9HP8G7", channel: "C09T1KE0Y9G" },
  { timestamp: "2026-01-05", name: "user_feedback", value: 1, userId: "U09A7KBFQSK", channel: "C0A4SNLDKHQ" },
  { timestamp: "2026-01-05", name: "failure_unhelpful", value: 1, comment: "the only real actionable here is 2: - Analyze games with a focus on space control and endgame techniques.\nbut the actionable on how to do this is vague and unhelpful" },
  { timestamp: "2026-01-05", name: "user_feedback", value: -1, userId: "U01QYGRC0FJ", channel: "C09T1KE0Y9G" },
  { timestamp: "2026-01-02", name: "failure_other", value: 1, comment: "Error when running game review" },
  { timestamp: "2026-01-02", name: "user_feedback", value: -1, userId: "U03V20RB4SV", channel: "C0A4SNLDKHQ" },
  { timestamp: "2025-12-28", name: "user_feedback", value: -1, userId: "U05BWUL4STS", channel: "C0A4SNLDKHQ" },
  { timestamp: "2025-12-26", name: "failure_poor_format", value: 1, comment: "" },
  { timestamp: "2025-12-26", name: "user_feedback", value: -1, userId: "U0VPTBY9F", channel: "C09T1KE0Y9G" },
  { timestamp: "2025-12-26", name: "failure_other", value: 1, comment: "testing" },
  { timestamp: "2025-12-26", name: "user_feedback", value: -1, userId: "U08V8GVK571", channel: "C0A2PGS5C92" },
  { timestamp: "2025-12-26", name: "user_feedback", value: -1, userId: "U0A4VQNLUM9", channel: "C0A3U5GRB16" },
  { timestamp: "2025-12-26", name: "user_feedback", value: 1, userId: "U0A4VQNLUM9", channel: "C0A3U5GRB16" },
  { timestamp: "2025-12-26", name: "user_feedback", value: -1, userId: "U0A4VQNLUM9", channel: "C0A3U5GRB16" },
  { timestamp: "2025-12-26", name: "user_feedback", value: 1, userId: "U060K0B6TNE", channel: "C0ARC3TSB" },
  { timestamp: "2025-12-25", name: "user_feedback", value: 1, userId: "U04RSKLP6QZ", channel: "C0A4SNLDKHQ" },
  { timestamp: "2025-12-25", name: "user_feedback", value: -1, userId: "U09JDLGLH1C", channel: "C0A2PGS5C92" },
  { timestamp: "2025-12-25", name: "user_feedback", value: -1, userId: "U09JDLGLH1C", channel: "C0A2PGS5C92" },
  { timestamp: "2025-12-24", name: "failure_hallucinated", value: 1, comment: "" },
  { timestamp: "2025-12-24", name: "failure_incorrect_chess", value: 1, comment: "" },
  { timestamp: "2025-12-24", name: "user_feedback", value: 1, userId: "U04ML73J2E5", channel: "C0A4SNLDKHQ" },
  { timestamp: "2025-12-24", name: "user_feedback", value: 1, userId: "U09JDLGLH1C", channel: "C0A2PGS5C92" },
  { timestamp: "2025-12-24", name: "user_feedback", value: 1, userId: "U0A4VQNLUM9", channel: "C0A3U5GRB16" },
  { timestamp: "2025-12-24", name: "user_feedback", value: 1, userId: "U0A4VQNLUM9", channel: "C0A3U5GRB16" },
  { timestamp: "2025-12-24", name: "user_feedback", value: 1, userId: "U0A4VQNLUM9", channel: "C0A3U5GRB16" },
  { timestamp: "2025-12-24", name: "user_feedback", value: 1, userId: "U0A4VQNLUM9", channel: "C0A3U5GRB16" },
];

// Add remaining negative feedback entries
for (let i = 0; i < 53; i++) {
  scoresData.push({ timestamp: "2025-12-24", name: "user_feedback", value: -1, userId: `U_NEG_${i}`, channel: "C0A2PGS5C92" });
}

// Performance data from traces analysis
const perfData = {
  totalTraces: 126,
  latency: { mean: 12.71, median: 9.62, min: 2.04, max: 48.60 },
  tokens: { inputMean: 19231, outputMean: 389, totalMean: 19620, totalSum: 2472140 },
  cost: { mean: 0.0478, median: 0.0372, total: 5.98, min: 0.0142, max: 0.2020 },
  byFeedback: {
    positive: { latency: 12.36, tokens: 15224, cost: 0.0408 },
    negative: { latency: 16.21, tokens: 22828, cost: 0.0572 },
    noFeedback: { latency: 12.54, tokens: 19532, cost: 0.0475 },
    withFailures: { latency: 18.48, tokens: 24672, cost: 0.0633 }
  }
};

const COLORS = {
  positive: '#10b981',
  negative: '#ef4444',
  neutral: '#6b7280',
  warning: '#f59e0b',
  purple: '#8b5cf6',
  pink: '#ec4899',
  cyan: '#06b6d4',
  orange: '#f97316',
};

const CHANNEL_NAMES = {
  'C0A4SNLDKHQ': 'Main Channel',
  'C09T1KE0Y9G': 'Support',
  'C0A2PGS5C92': 'Testing',
  'C0A3U5GRB16': 'Dev',
  'C0ARC3TSB': 'General',
};

export default function FeedbackDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [assumeNoFeedbackGood, setAssumeNoFeedbackGood] = useState(false);
  const [selectedFailure, setSelectedFailure] = useState('all');

  const stats = useMemo(() => {
    const feedback = scoresData.filter(d => d.name === 'user_feedback');
    const failures = scoresData.filter(d => d.name.startsWith('failure_'));
    
    const positive = feedback.filter(d => d.value === 1).length;
    const negative = feedback.filter(d => d.value === -1).length;
    const noFeedbackCount = 57; // 126 total - 69 with feedback
    
    // Adjusted counts based on toggle
    const adjustedPositive = assumeNoFeedbackGood ? positive + noFeedbackCount : positive;
    const adjustedTotal = assumeNoFeedbackGood ? feedback.length + noFeedbackCount : feedback.length;
    const satisfactionRate = (adjustedPositive / adjustedTotal) * 100;
    
    const failureTypes = {};
    const failureComments = [];
    failures.forEach(f => {
      const type = f.name.replace('failure_', '');
      failureTypes[type] = (failureTypes[type] || 0) + 1;
      if (f.comment) {
        failureComments.push({ type, comment: f.comment, timestamp: f.timestamp });
      }
    });

    return {
      totalQueries: 126,
      totalFeedback: feedback.length,
      positive,
      negative,
      noFeedbackCount,
      adjustedPositive,
      adjustedTotal,
      satisfactionRate,
      totalFailures: failures.length,
      failureTypes,
      failureComments,
    };
  }, [assumeNoFeedbackGood]);

  const perfComparisonData = [
    { name: '👍 Positive', latency: perfData.byFeedback.positive.latency, tokens: perfData.byFeedback.positive.tokens / 1000, cost: perfData.byFeedback.positive.cost * 100 },
    { name: '👎 Negative', latency: perfData.byFeedback.negative.latency, tokens: perfData.byFeedback.negative.tokens / 1000, cost: perfData.byFeedback.negative.cost * 100 },
    { name: '❓ No Feedback', latency: perfData.byFeedback.noFeedback.latency, tokens: perfData.byFeedback.noFeedback.tokens / 1000, cost: perfData.byFeedback.noFeedback.cost * 100 },
    { name: '⚠️ Failures', latency: perfData.byFeedback.withFailures.latency, tokens: perfData.byFeedback.withFailures.tokens / 1000, cost: perfData.byFeedback.withFailures.cost * 100 },
  ];

  const failureBarData = Object.entries(stats.failureTypes).map(([type, count]) => ({
    name: type.replace('_', ' '),
    count,
    fill: type === 'other' ? COLORS.purple : type === 'hallucinated' ? COLORS.cyan : type === 'incorrect_chess' ? COLORS.orange : type === 'poor_format' ? COLORS.pink : COLORS.warning,
  }));

  const feedbackPieData = assumeNoFeedbackGood 
    ? [
        { name: 'Positive (explicit)', value: stats.positive, color: COLORS.positive },
        { name: 'Positive (assumed)', value: stats.noFeedbackCount, color: '#34d399' },
        { name: 'Negative', value: stats.negative, color: COLORS.negative },
      ]
    : [
        { name: 'Positive', value: stats.positive, color: COLORS.positive },
        { name: 'Negative', value: stats.negative, color: COLORS.negative },
      ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-white">Feedback & Performance Dashboard</h1>
            <p className="text-slate-400 mt-1">LangFuse analysis · Dec 24 – Jan 6 · 126 queries</p>
          </div>
          
          {/* Toggle */}
          <div className="mt-4 md:mt-0 flex items-center gap-3 bg-slate-900 rounded-lg px-4 py-3 border border-slate-700">
            <span className="text-sm text-slate-300">Assume no feedback = good</span>
            <button
              onClick={() => setAssumeNoFeedbackGood(!assumeNoFeedbackGood)}
              className={`relative w-12 h-6 rounded-full transition-colors ${
                assumeNoFeedbackGood ? 'bg-emerald-600' : 'bg-slate-600'
              }`}
            >
              <span
                className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${
                  assumeNoFeedbackGood ? 'translate-x-7' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
        </div>

        {/* Toggle explanation */}
        {assumeNoFeedbackGood && (
          <div className="mb-6 bg-emerald-900/30 border border-emerald-700/50 rounded-lg px-4 py-3">
            <p className="text-emerald-300 text-sm">
              ✅ <strong>57 queries</strong> without reactions are counted as positive (126 total - 69 with feedback)
            </p>
          </div>
        )}

        {/* Navigation */}
        <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
          {['overview', 'performance', 'failures'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 rounded-lg font-medium transition-all whitespace-nowrap ${
                activeTab === tab 
                  ? 'bg-indigo-600 text-white' 
                  : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
              }`}
            >
              {tab === 'overview' ? '📊 Overview' : tab === 'performance' ? '⚡ Performance' : '🚨 Failures'}
            </button>
          ))}
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* KPI Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
                <p className="text-slate-500 text-sm">Total Queries</p>
                <p className="text-3xl font-bold text-white">{stats.totalQueries}</p>
              </div>
              <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
                <p className="text-slate-500 text-sm">Satisfaction Rate</p>
                <p className={`text-3xl font-bold ${stats.satisfactionRate >= 50 ? 'text-emerald-400' : 'text-red-400'}`}>
                  {stats.satisfactionRate.toFixed(1)}%
                </p>
                {assumeNoFeedbackGood && <p className="text-xs text-emerald-400 mt-1">+57 assumed good</p>}
              </div>
              <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
                <p className="text-slate-500 text-sm">👍 Positive</p>
                <p className="text-3xl font-bold text-emerald-400">{stats.adjustedPositive}</p>
                {assumeNoFeedbackGood && <p className="text-xs text-slate-400 mt-1">{stats.positive} explicit + 57</p>}
              </div>
              <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
                <p className="text-slate-500 text-sm">👎 Negative</p>
                <p className="text-3xl font-bold text-red-400">{stats.negative}</p>
              </div>
            </div>

            {/* Charts Row */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
                <h3 className="text-lg font-semibold mb-4">Feedback Distribution</h3>
                <ResponsiveContainer width="100%" height={220}>
                  <PieChart>
                    <Pie
                      data={feedbackPieData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={90}
                      dataKey="value"
                      label={({ name, percent }) => `${(percent * 100).toFixed(0)}%`}
                    >
                      {feedbackPieData.map((entry, i) => (
                        <Cell key={i} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
                <h3 className="text-lg font-semibold mb-4">Performance Summary</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-400">Avg Latency</span>
                    <span className="text-xl font-bold">{perfData.latency.mean}s</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-400">Avg Tokens</span>
                    <span className="text-xl font-bold">{perfData.tokens.totalMean.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-400">Avg Cost</span>
                    <span className="text-xl font-bold">${perfData.cost.mean.toFixed(4)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-400">Total Cost</span>
                    <span className="text-xl font-bold">${perfData.cost.total.toFixed(2)}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Summary */}
            <div className={`rounded-xl p-5 border ${
              stats.satisfactionRate >= 50 
                ? 'bg-gradient-to-r from-emerald-900/30 to-cyan-900/30 border-emerald-800/50' 
                : 'bg-gradient-to-r from-amber-900/30 to-red-900/30 border-amber-800/50'
            }`}>
              <h3 className={`text-lg font-semibold mb-3 ${stats.satisfactionRate >= 50 ? 'text-emerald-200' : 'text-amber-200'}`}>
                Key Insights
              </h3>
              <ul className="space-y-2 text-slate-300">
                <li>• <strong className="text-white">Satisfaction rate: {stats.satisfactionRate.toFixed(1)}%</strong> — {stats.adjustedPositive} positive vs {stats.negative} negative</li>
                <li>• <strong className="text-white">{stats.totalFailures} documented failures</strong> across {Object.keys(stats.failureTypes).length} categories</li>
                <li>• <strong className="text-white">Negative feedback</strong> correlates with +31% latency and +40% cost</li>
                <li>• <strong className="text-white">Total spend:</strong> ${perfData.cost.total.toFixed(2)} for {perfData.totalTraces} queries (~${perfData.cost.mean.toFixed(3)}/query)</li>
              </ul>
            </div>
          </div>
        )}

        {/* Performance Tab */}
        {activeTab === 'performance' && (
          <div className="space-y-6">
            {/* Performance KPIs */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
                <p className="text-slate-500 text-sm">Avg Latency</p>
                <p className="text-3xl font-bold text-white">{perfData.latency.mean}s</p>
                <p className="text-xs text-slate-400 mt-1">Median: {perfData.latency.median}s</p>
              </div>
              <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
                <p className="text-slate-500 text-sm">Avg Tokens</p>
                <p className="text-3xl font-bold text-white">{(perfData.tokens.totalMean / 1000).toFixed(1)}k</p>
                <p className="text-xs text-slate-400 mt-1">Total: {(perfData.tokens.totalSum / 1000000).toFixed(2)}M</p>
              </div>
              <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
                <p className="text-slate-500 text-sm">Avg Cost</p>
                <p className="text-3xl font-bold text-white">${perfData.cost.mean.toFixed(3)}</p>
                <p className="text-xs text-slate-400 mt-1">Median: ${perfData.cost.median.toFixed(3)}</p>
              </div>
              <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
                <p className="text-slate-500 text-sm">Total Cost</p>
                <p className="text-3xl font-bold text-emerald-400">${perfData.cost.total}</p>
                <p className="text-xs text-slate-400 mt-1">126 queries</p>
              </div>
            </div>

            {/* Performance by Feedback */}
            <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
              <h3 className="text-lg font-semibold mb-4">Performance by Feedback Type</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={perfComparisonData}>
                  <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                  <YAxis yAxisId="left" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                  <YAxis yAxisId="right" orientation="right" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: 8 }}
                    formatter={(value, name) => {
                      if (name === 'latency') return [`${value}s`, 'Latency'];
                      if (name === 'tokens') return [`${(value * 1000).toLocaleString()}`, 'Tokens'];
                      if (name === 'cost') return [`$${(value / 100).toFixed(4)}`, 'Cost'];
                      return [value, name];
                    }}
                  />
                  <Legend />
                  <Bar yAxisId="left" dataKey="latency" fill="#3b82f6" name="Latency (s)" />
                  <Bar yAxisId="left" dataKey="tokens" fill="#8b5cf6" name="Tokens (k)" />
                  <Bar yAxisId="right" dataKey="cost" fill="#10b981" name="Cost (¢)" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Insights */}
            <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-xl p-5 border border-blue-800/50">
              <h3 className="text-lg font-semibold mb-3 text-blue-200">Performance Insights</h3>
              <div className="grid md:grid-cols-2 gap-4 text-slate-300">
                <div>
                  <h4 className="font-semibold text-white mb-2">Negative vs Positive Feedback</h4>
                  <ul className="space-y-1 text-sm">
                    <li>• Latency: <span className="text-red-400">+31%</span> (16.2s vs 12.4s)</li>
                    <li>• Tokens: <span className="text-red-400">+50%</span> (22.8k vs 15.2k)</li>
                    <li>• Cost: <span className="text-red-400">+40%</span> ($0.057 vs $0.041)</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold text-white mb-2">Traces with Failures</h4>
                  <ul className="space-y-1 text-sm">
                    <li>• Latency: <span className="text-orange-400">+49%</span> vs positive (18.5s)</li>
                    <li>• Tokens: <span className="text-orange-400">+62%</span> vs positive (24.7k)</li>
                    <li>• Cost: <span className="text-orange-400">+55%</span> vs positive ($0.063)</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Failures Tab */}
        {activeTab === 'failures' && (
          <div className="space-y-6">
            {/* Failure Filter */}
            <div className="flex items-center gap-3">
              <span className="text-slate-400">Filter:</span>
              <div className="flex gap-2 flex-wrap">
                {['all', ...Object.keys(stats.failureTypes)].map(type => (
                  <button
                    key={type}
                    onClick={() => setSelectedFailure(type)}
                    className={`px-3 py-1.5 rounded-lg text-sm transition-all ${
                      selectedFailure === type
                        ? 'bg-indigo-600 text-white'
                        : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                    }`}
                  >
                    {type === 'all' ? 'All' : type.replace('_', ' ')}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
                <h3 className="text-lg font-semibold mb-4">Failure Distribution ({stats.totalFailures} total)</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={failureBarData} layout="vertical">
                    <XAxis type="number" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                    <YAxis type="category" dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} width={100} />
                    <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: 8 }} />
                    <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                      {failureBarData.map((entry, i) => (
                        <Cell key={i} fill={entry.fill} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
                <h3 className="text-lg font-semibold mb-4">Failure Breakdown</h3>
                <div className="space-y-3">
                  {Object.entries(stats.failureTypes)
                    .filter(([type]) => selectedFailure === 'all' || type === selectedFailure)
                    .map(([type, count]) => (
                    <div 
                      key={type}
                      className="flex items-center justify-between p-3 bg-slate-800 rounded-lg"
                    >
                      <div className="flex items-center gap-3">
                        <div 
                          className="w-3 h-3 rounded-full" 
                          style={{ backgroundColor: type === 'other' ? COLORS.purple : type === 'hallucinated' ? COLORS.cyan : type === 'incorrect_chess' ? COLORS.orange : type === 'poor_format' ? COLORS.pink : COLORS.warning }}
                        />
                        <span className="capitalize">{type.replace('_', ' ')}</span>
                      </div>
                      <span className="text-xl font-bold">{count}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Failure Comments */}
            <div className="bg-slate-900 rounded-xl p-5 border border-slate-800">
              <h3 className="text-lg font-semibold mb-4">Failure Comments</h3>
              {stats.failureComments
                .filter(c => selectedFailure === 'all' || c.type === selectedFailure)
                .length === 0 ? (
                <p className="text-slate-500">No comments for selected filter</p>
              ) : (
                <div className="space-y-3">
                  {stats.failureComments
                    .filter(c => selectedFailure === 'all' || c.type === selectedFailure)
                    .map((f, i) => (
                    <div key={i} className="p-4 bg-slate-800 rounded-lg border-l-4 border-amber-500">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="px-2 py-1 bg-slate-700 rounded text-xs font-medium capitalize">
                          {f.type.replace('_', ' ')}
                        </span>
                        <span className="text-slate-500 text-xs">{f.timestamp}</span>
                      </div>
                      <p className="text-slate-300 whitespace-pre-wrap">{f.comment}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Recommendations */}
            <div className="bg-gradient-to-r from-violet-900/30 to-pink-900/30 rounded-xl p-5 border border-violet-800/50">
              <h3 className="text-lg font-semibold mb-3 text-violet-200">Recommendations</h3>
              <div className="grid md:grid-cols-2 gap-4 text-slate-300">
                <ul className="space-y-2 text-sm">
                  <li>• <strong>Other errors:</strong> Improve error handling for game reviews</li>
                  <li>• <strong>Hallucination:</strong> Add validation and fact-checking</li>
                  <li>• <strong>Incorrect chess:</strong> Implement chess-specific validation</li>
                </ul>
                <ul className="space-y-2 text-sm">
                  <li>• <strong>Poor format:</strong> Standardize output templates</li>
                  <li>• <strong>Unhelpful:</strong> Provide more specific, actionable advice</li>
                  <li>• <strong>General:</strong> Reduce latency for better experience</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
