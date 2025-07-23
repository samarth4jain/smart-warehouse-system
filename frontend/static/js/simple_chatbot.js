// Simplified Chatbot JavaScript
console.log('🤖 Simple Chatbot loaded');

class SimpleChatbot {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8001';
        this.userId = 'user_' + Date.now();
        this.init();
    }
    
    init() {
        console.log('🔧 Initializing chatbot...');
        
        // Wait for DOM
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupEventListeners());
        } else {
            this.setupEventListeners();
        }
    }
    
    setupEventListeners() {
        const chatInput = document.getElementById('chat-input');
        const sendButton = document.getElementById('send-button');
        
        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }
        
        if (sendButton) {
            sendButton.addEventListener('click', () => this.sendMessage());
        }
        
        console.log('✅ Chatbot event listeners set up');
    }
    
    async sendMessage() {
        const chatInput = document.getElementById('chat-input');
        const messagesContainer = document.getElementById('chat-messages');
        
        if (!chatInput || !messagesContainer) {
            console.error('❌ Required chat elements not found');
            return;
        }
        
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        chatInput.value = '';
        
        // Show typing indicator
        this.showTyping();
        
        try {
            console.log('📤 Sending message:', message);
            
            const response = await fetch(`${this.apiBaseUrl}/api/chat/message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    user_id: this.userId
                })
            });
            
            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('📥 Bot response:', data);
            
            // Hide typing and show response
            this.hideTyping();
            this.addMessage(data.message, 'bot');
            
        } catch (error) {
            console.error('❌ Chat error:', error);
            this.hideTyping();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot', 'error');
        }
    }
    
    addMessage(text, sender, type = '') {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message ${type}`;
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${text}</p>
                <span class="message-time">${new Date().toLocaleTimeString()}</span>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    showTyping() {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;
        
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.className = 'message bot-message typing';
        typingDiv.innerHTML = `
            <div class="message-content">
                <p>Assistant is typing...</p>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    hideTyping() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
}

// Initialize chatbot
const chatbot = new SimpleChatbot();

// Global functions
window.chatbot = chatbot;
