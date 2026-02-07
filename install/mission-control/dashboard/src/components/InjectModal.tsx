import { useState, useRef, useEffect } from 'react'
import { sendCommand } from '../api'

interface InjectModalProps {
  sessionId: string
  project: string
  onClose: () => void
}

export function InjectModal({ sessionId, project, onClose }: InjectModalProps) {
  const [prompt, setPrompt] = useState('')
  const [sending, setSending] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    textareaRef.current?.focus()

    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [onClose])

  async function handleSend() {
    if (!prompt.trim() || sending) return

    setSending(true)
    try {
      await sendCommand(sessionId, prompt.trim())
      onClose()
    } catch {
      setSending(false)
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      handleSend()
    }
  }

  return (
    <div className="modal-overlay" onClick={e => { if (e.target === e.currentTarget) onClose() }}>
      <div className="modal-content">
        <div className="modal-header">
          <h3>Inject Prompt</h3>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>
        <div className="modal-target">
          Sending to: <strong>{project}</strong>
        </div>
        <textarea
          ref={textareaRef}
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={'Enter instruction for Claude...\n\nExample: Please pause current work and focus on fixing the failing test in auth.test.ts'}
        />
        <div className="modal-actions">
          <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn" onClick={handleSend} disabled={sending}>
            {sending ? 'Sending...' : 'Send Command'}
          </button>
        </div>
      </div>
    </div>
  )
}
