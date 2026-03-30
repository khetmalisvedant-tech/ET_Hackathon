import { useState, useRef, useEffect } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || "https://et-hackathon-o4iv.onrender.com"

const SUGGESTIONS = [
  '💧 When should I irrigate today?',
  '🌾 Best crop for this season?',
  '🌱 Fertilizer for wheat?',
  '🐛 Pest control tips',
]

const CAPABILITIES = [
  '🌾 Crop decisions',
  '💧 Irrigation planning',
  '🌱 Fertilizer guidance',
  '📊 Smart insights',
]

function parseAiResponse(text) {
  const sections = [
    { key: '🌱 Decision:', label: 'Decision' },
    { key: '⚡ Action:', label: 'Action' },
    { key: '📊 Monitoring:', label: 'Monitoring' },
    { key: '✅ Verification:', label: 'Verification' },
  ]

  const parts = []
  const remaining = text.trim()

  for (let i = 0; i < sections.length; i++) {
    const { key, label } = sections[i]
    const idx = remaining.indexOf(key)
    if (idx === -1) continue

    const nextKeys = sections.slice(i + 1).map(s => s.key)
    let end = remaining.length
    for (const nk of nextKeys) {
      const ni = remaining.indexOf(nk, idx + key.length)
      if (ni !== -1 && ni < end) end = ni
    }

    const content = remaining.slice(idx + key.length, end).trim()
    if (content) parts.push({ label, content })
  }

  return parts.length > 0 ? parts : null
}

export default function App() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [logs, setLogs] = useState([])
  const [weatherInfo, setWeatherInfo] = useState(null)
  const [locationName, setLocationName] = useState('')
  const [wsi, setWsi] = useState(null)
  const [wsiLevel, setWsiLevel] = useState('')
  const [confidence, setConfidence] = useState(null)
  const [location, setLocation] = useState(null)
  const [autoScroll, setAutoScroll] = useState(true)
  const [showScrollBtn, setShowScrollBtn] = useState(false)

  const chatEndRef = useRef(null)
  const chatContainerRef = useRef(null)
  const textareaRef = useRef(null)

  // 📍 Get geolocation
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        pos => setLocation({ lat: pos.coords.latitude, lon: pos.coords.longitude }),
        () => {}
      )
    }
  }, [])

  // 🔄 Auto-scroll
  useEffect(() => {
    if (autoScroll) {
      chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, logs, autoScroll])

  const handleScroll = () => {
    const c = chatContainerRef.current
    if (!c) return
    const near = c.scrollHeight - c.scrollTop - c.clientHeight < 100
    setAutoScroll(near)
    setShowScrollBtn(!near)
  }

  // 🚀 Send message
  const handleSend = async (text) => {
    const userText = (text || input).trim()
    if (!userText) return

    setMessages(prev => [...prev, { type: 'user', text: userText }])
    setInput('')
    setLoading(true)
    setLogs([])
    setConfidence(null)

    try {
      const res = await fetch(`${API_URL}/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: userText, location }),
      })

      const data = await res.json()

      setLogs(data.logs || [])
      setWeatherInfo(data.weather)
      setLocationName(data.location)
      setWsi(data.wsi)
      setWsiLevel(data.wsi_level)
      setLoading(false)

      const verificationText = data.response?.verification || ''
      const match = verificationText.match(/Confidence:\s*(\d+)/i)
      if (match) setConfidence(match[1])

      const actionData = data.response?.action
      let formattedAction = 'No action available'

      if (actionData && !actionData.error) {
        formattedAction = [
          `Action Type: ${actionData.action_type}`,
          `Priority: ${actionData.priority}`,
          '',
          'Steps:',
          ...actionData.steps.map(s =>
            `• ${s.command} — ${s.parameters.duration_minutes || 'N/A'} min, Zone: ${s.parameters.zone || 'N/A'}`
          ),
        ].join('\n')
      } else if (actionData?.error) {
        formattedAction = '⚠️ Action generation failed'
      }

      const formattedResponse = [
        `🌱 Decision:\n${data.response?.decision || ''}`,
        `⚡ Action:\n${formattedAction}`,
        `📊 Monitoring:\n${data.response?.monitor || ''}`,
        `✅ Verification:\n${data.response?.verification || ''}`,
      ].join('\n\n')

      setMessages(prev => [
        ...prev,
        { type: 'ai', text: formattedResponse, confidence: match ? match[1] : null },
      ])

    } catch (err) {
      console.error(err)
      setLoading(false)
      setLogs([])
      setMessages(prev => [
        ...prev,
        { type: 'ai', text: '❌ Error connecting to backend. Please try again.', confidence: null },
      ])
    }
  }

  const handleKeyDown = e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleTextareaInput = e => {
    e.target.style.height = 'auto'
    e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px'
  }

  const wsiPct = wsi ? Math.min(100, (parseFloat(wsi) / 5) * 100) : 0

  return (
    <div className="layout">

      {/* ── SIDEBAR ── */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="logo">
            <div className="logo-icon">🌿</div>
            <span className="logo-text">AutoFlow AI</span>
          </div>
          <div className="logo-sub">Agricultural Intelligence</div>
        </div>

        <div className="sidebar-scroll">
          {weatherInfo ? (
            <div className="sidebar-section">
              <div className="sidebar-label">Live Conditions</div>
              <div className="weather-card">
                <div className="weather-location">
                  <span>📍</span>
                  {locationName || 'Your Location'}
                </div>
                <div className="weather-grid">
                  <div className="weather-stat">
                    <div className="weather-stat-label">Temp</div>
                    <div className="weather-stat-value">{weatherInfo.temperature}°C</div>
                  </div>
                  <div className="weather-stat">
                    <div className="weather-stat-label">Humidity</div>
                    <div className="weather-stat-value">{weatherInfo.humidity}%</div>
                  </div>
                  <div className="weather-stat full">
                    <div className="weather-stat-label">Condition</div>
                    <div className="weather-stat-value sm">{weatherInfo.condition}</div>
                  </div>
                </div>
              </div>

              {wsi && (
                <div className="wsi-section">
                  <div className="sidebar-label">Water Stress Index</div>
                  <div className="wsi-card">
                    <div className="wsi-row">
                      <div className="wsi-label">WSI Score</div>
                      <div className="wsi-value">{wsi}</div>
                    </div>
                    <div className="wsi-bar-track">
                      <div className="wsi-bar-fill" style={{ width: `${wsiPct}%` }} />
                    </div>
                    <div className="wsi-level">⚠️ {wsiLevel}</div>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="sidebar-section">
              <div className="sidebar-label">Capabilities</div>
              {CAPABILITIES.map(item => (
                <div key={item} className="capability-item">{item}</div>
              ))}
            </div>
          )}
        </div>

        <div className="sidebar-footer">
          <div className="status-dot" />
          <span>Backend connected</span>
        </div>
      </aside>

      {/* ── MAIN ── */}
      <div className="main">
        <div className="main-header">
          <div className="main-title">Farm Assistant</div>
          <div className="chip">AI-Powered</div>
        </div>

        {/* Chat area */}
        <div className="chat-area" ref={chatContainerRef} onScroll={handleScroll}>

          {/* Agent logs */}
          {(loading || logs.length > 0) && (
            <div className="thinking-box">
              <div className="thinking-title">
                {loading && <div className="thinking-spinner" />}
                Agent Execution
              </div>
              {loading && logs.length === 0 && (
                <div className="log-line">
                  <span className="log-arrow">›</span>
                  Initializing agents…
                </div>
              )}
              {logs.map((log, i) => (
                <div key={i} className="log-line">
                  <span className="log-arrow">›</span>
                  {log}
                </div>
              ))}
            </div>
          )}

          {/* Empty state */}
          {messages.length === 0 && !loading && (
            <div className="empty-state">
              <div className="empty-icon">🌿</div>
              <div className="empty-title">What can I help with?</div>
              <div className="empty-sub">
                Ask me anything about your farm — crops, water, weather, or pests.
              </div>
              <div className="pill-grid">
                {SUGGESTIONS.map(s => (
                  <button key={s} className="pill-btn" onClick={() => handleSend(s)}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Messages */}
          {messages.map((msg, i) => {
            if (msg.type === 'user') {
              return (
                <div key={i} className="msg-wrap user">
                  <div className="msg-user">{msg.text}</div>
                </div>
              )
            }

            const sections = parseAiResponse(msg.text)
            return (
              <div key={i} className="msg-wrap ai">
                <div className="msg-ai-wrap">
                  {msg.confidence && (
                    <div className="confidence-badge">
                      ✦ Confidence: {msg.confidence}%
                    </div>
                  )}
                  <div className="ai-card">
                    {sections ? (
                      sections.map((s, j) => (
                        <div key={j}>
                          {j > 0 && <div className="ai-divider" />}
                          <div className="ai-section">
                            <div className="ai-section-title">{s.label}</div>
                            <div className="ai-section-body">{s.content}</div>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="ai-plain">{msg.text}</div>
                    )}
                  </div>
                </div>
              </div>
            )
          })}

          <div ref={chatEndRef} />
        </div>

        {/* Scroll to bottom FAB */}
        {showScrollBtn && (
          <button
            className="scroll-fab"
            onClick={() => chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })}
          >
            ↓
          </button>
        )}

        {/* Input */}
        <div className="input-row">
          <div className="input-wrap">
            <textarea
              ref={textareaRef}
              className="input-textarea"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              onInput={handleTextareaInput}
              placeholder="Ask about your farm…"
              rows={1}
            />
            <button
              className="send-btn"
              onClick={() => handleSend()}
              disabled={loading || !input.trim()}
            >
              <svg className="send-icon" viewBox="0 0 24 24">
                <line x1="22" y1="2" x2="11" y2="13" />
                <polygon points="22 2 15 22 11 13 2 9 22 2" />
              </svg>
            </button>
          </div>
          <div className="hint-text">Enter to send · Shift+Enter for new line</div>
        </div>
      </div>

    </div>
  )
}