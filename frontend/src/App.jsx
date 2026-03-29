import {useState, useRef, useEffect} from 'react'
import './App.css'

function App() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([
    {
      type: 'ai',
      text: `👋 Hello! I'm AutoFlow AI.

I can help you with:
🌾 Crop decisions
💧 Irrigation planning
🌱 Fertilizer recommendations
📊 Smart agricultural insights

👉 Ask me anything about your farm!`,
    },
  ])
  const [loading, setLoading] = useState(false)

  const [logs, setLogs] = useState([])
  const [weatherInfo, setWeatherInfo] = useState(null)
  const [locationName, setLocationName] = useState("")

  const [wsi, setWsi] = useState(null)
  const [wsiLevel, setWsiLevel] = useState("")

  const [confidence, setConfidence] = useState(null)

  const [location, setLocation] = useState(null)

  const chatEndRef = useRef(null)
  const chatContainerRef = useRef(null)

  const [autoScroll, setAutoScroll] = useState(true)
  const [showScrollBtn, setShowScrollBtn] = useState(false)

  // ✅ ADD THIS (API URL)
  const API_URL =
    import.meta.env.VITE_API_URL ||
    "https://et-hackathon-o4iv.onrender.com"

  // 📍 Get location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        position => {
          setLocation({
            lat: position.coords.latitude,
            lon: position.coords.longitude,
          })
        },
        () => {
          console.log('Location denied')
        }
      )
    }
  }, [])

  // 🔄 Scroll handling
  const handleScroll = () => {
    const container = chatContainerRef.current
    if (!container) return

    const isNearBottom =
      container.scrollHeight - container.scrollTop - container.clientHeight < 100

    setAutoScroll(isNearBottom)
    setShowScrollBtn(!isNearBottom)
  }

  useEffect(() => {
    if (autoScroll) {
      chatEndRef.current?.scrollIntoView({behavior: 'smooth'})
    }
  }, [messages, logs, autoScroll])

  // 🚀 Send message
  const handleSend = async () => {
    if (!input.trim()) return

    const userText = input

    setMessages(prev => [...prev, {type: 'user', text: userText}])
    setInput('')
    setLoading(true)
    setLogs([])
    setConfidence(null)

    try {
      // ✅ ONLY CHANGE HERE
      const res = await fetch(`${API_URL}/execute`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          input: userText,
          location,
        }),
      })

      const data = await res.json()

      setLogs(data.logs || [])
      setWeatherInfo(data.weather)
      setLocationName(data.location)

      setWsi(data.wsi)
      setWsiLevel(data.wsi_level)

      setLoading(false)

      const verificationText = data.response?.verification || ""
      const match = verificationText.match(/Confidence:\s*(\d+)/i)
      if (match) {
        setConfidence(match[1])
      }

      const actionData = data.response?.action

      let formattedAction = "No action available"

      if (actionData && !actionData.error) {
        formattedAction = `
Action Type: ${actionData.action_type}

Priority: ${actionData.priority}

Steps:
${actionData.steps.map(step => `
- Command: ${step.command}
  Duration: ${step.parameters.duration_minutes || "N/A"} minutes
  Zone: ${step.parameters.zone || "N/A"}
`).join('')}
`
      } else if (actionData?.error) {
        formattedAction = "⚠️ Action generation failed"
      }

      const formattedResponse = `
🌱 Decision:
${data.response?.decision || ""}

⚡ Action:
${formattedAction}

📊 Monitoring:
${data.response?.monitor || ""}

✅ Verification:
${data.response?.verification || ""}
`

      setMessages(prev => [...prev, {type: 'ai', text: formattedResponse}])

    } catch (err) {
      console.error(err)
      setLoading(false)
      setLogs([])

      setMessages(prev => [
        ...prev,
        {type: 'ai', text: '❌ Error connecting to backend'},
      ])
    }
  }

  const handleKeyDown = e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="app">
      <h1 className="header">🚀 AutoFlow AI</h1>

      {weatherInfo && (
        <div className="weather-box">
          <p>📍 {locationName}</p>
          <p>⚡ Real-time weather data used</p>
          <p>🌡 Temp: {weatherInfo.temperature}°C</p>
          <p>💧 Humidity: {weatherInfo.humidity}%</p>
          <p>☁ Condition: {weatherInfo.condition}</p>
        </div>
      )}

      {wsi && (
        <div className="wsi-box">
          <p>📊 WSI: {wsi}</p>
          <p>⚠️ Stress Level: {wsiLevel}</p>
        </div>
      )}

      <div className="chat-container" ref={chatContainerRef} onScroll={handleScroll}>
        {loading && logs.length === 0 && (
          <div className="thinking-box">
            <p><b>🧠 Agents Running...</b></p>
            <p>➜ Initializing system...</p>
          </div>
        )}

        {logs.length > 0 && (
          <div className="thinking-box">
            <p><b>🧠 Agent Execution</b></p>
            {logs.map((log, i) => (
              <p key={i}>➜ {log}</p>
            ))}
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className={msg.type === 'user' ? 'user-msg' : 'ai-msg'}>
            {msg.type === 'user' ? (
              <p>{msg.text}</p>
            ) : (
              <div>
                {confidence && (
                  <div className="confidence-badge">
                    ✅ Confidence: {confidence}%
                  </div>
                )}

                <div className="ai-card">
                  {msg.text.split('\n').map((line, i) => (
                    <p key={i}>{line}</p>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}

        <div ref={chatEndRef} />
      </div>

      {showScrollBtn && (
        <button
          className="scroll-btn"
          onClick={() => chatEndRef.current?.scrollIntoView({behavior: 'smooth'})}
        >
          ⬇️
        </button>
      )}

      <div className="input-box">
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  )
}

export default App
