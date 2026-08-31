const form = document.querySelector('#chat-form');
const input = document.querySelector('#message-input');
const conversation = document.querySelector('#conversation');
const count = document.querySelector('#character-count');
const clearButton = document.querySelector('#clear-chat');
const sessionKey = 'raven-session-id';

const sessionId = window.localStorage.getItem(sessionKey) || crypto.randomUUID();
window.localStorage.setItem(sessionKey, sessionId);

const timestamp = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

function addMessage(role, text, time = timestamp()) {
  const message = document.createElement('div');
  message.className = `message ${role === 'user' ? 'user-message' : 'raven-message'}`;
  const label = role === 'user' ? 'YOU' : 'RAVEN';
  message.innerHTML = `<div class="message-label">${label} <span>${time}</span></div><div class="message-bubble"></div>`;
  message.querySelector('.message-bubble').textContent = text;
  conversation.appendChild(message);
  conversation.scrollTop = conversation.scrollHeight;
}

function setCount() {
  count.textContent = `${input.value.length} / 1200`;
}

input.addEventListener('input', () => {
  input.style.height = 'auto';
  input.style.height = `${Math.min(input.scrollHeight, 100)}px`;
  setCount();
});

input.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  addMessage('user', message);
  input.value = '';
  input.style.height = 'auto';
  setCount();
  const button = form.querySelector('button');
  button.disabled = true;

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, session_id: sessionId }),
    });
    const data = await response.json();
    if (!response.ok || typeof data.response !== 'string') throw new Error(data.error || 'Raven is unavailable.');
    addMessage('assistant', data.response);
  } catch (error) {
    addMessage('assistant', error.message || 'The signal dropped. Try me again.');
  } finally {
    button.disabled = false;
    input.focus();
  }
});

clearButton.addEventListener('click', () => {
  conversation.innerHTML = '<div class="message raven-message"><div class="message-label">RAVEN <span>01:44</span></div><div class="message-bubble">Fresh slate. I\'m listening.</div></div>';
  input.focus();
});

setCount();
