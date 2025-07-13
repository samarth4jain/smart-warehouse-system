// Chatbot JavaScript
class ChatbotManager {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.messageCount = 0;
        this.sessionStart = new Date();
        this.isTyping = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateSessionInfo();
        this.updateWelcomeTime();
        this.focusInput();
    }

    setupEventListeners() {
        const chatInput = document.getElementById('chat-input');
        const sendButton = document.getElementById('send-button');

        // Send message on Enter key
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Send button click
        sendButton.addEventListener('click', () => this.sendMessage());

        // Auto-resize input
        chatInput.addEventListener('input', () => {
            this.updateSendButton();
        });

        // Update send button state initially
        this.updateSendButton();
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    updateSessionInfo() {
        document.getElementById('session-id').textContent = this.sessionId.substr(-8);
        document.getElementById('message-count').textContent = this.messageCount;
        document.getElementById('session-start').textContent = this.sessionStart.toLocaleTimeString();
    }

    updateWelcomeTime() {
        const timeElement = document.getElementById('welcome-time');
        if (timeElement) {
            timeElement.textContent = new Date().toLocaleTimeString();
        }
    }

    updateSendButton() {
        const chatInput = document.getElementById('chat-input');
        const sendButton = document.getElementById('send-button');
        const hasText = chatInput.value.trim().length > 0;
        
        sendButton.disabled = !hasText || this.isTyping;
    }

    focusInput() {
        const chatInput = document.getElementById('chat-input');
        if (chatInput) {
            chatInput.focus();
        }
    }

    async sendMessage() {
        const chatInput = document.getElementById('chat-input');
        const message = chatInput.value.trim();

        if (!message || this.isTyping) return;

        // Clear input and disable send button
        chatInput.value = '';
        this.updateSendButton();

        // Add user message to chat
        this.addUserMessage(message);

        // Show typing indicator
        this.showTyping();

        try {
            // Send message to API
            const response = await this.apiCall('/api/chat/message', {
                method: 'POST',
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId,
                    user_id: 'web_user'
                })
            });

            // Hide typing indicator
            this.hideTyping();

            // Add bot response
            this.addBotMessage(response);

            // Update message count
            this.messageCount += 2;
            this.updateSessionInfo();

        } catch (error) {
            this.hideTyping();
            this.addBotMessage({
                message: "Sorry, I'm having trouble connecting right now. Please try again in a moment.",
                intent: "error",
                success: false
            });
            console.error('Chat error:', error);
        }

        // Focus back to input
        this.focusInput();
    }

    addUserMessage(message) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';

        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-user"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    <p>${this.escapeHtml(message)}</p>
                </div>
                <div class="message-time">
                    ${new Date().toLocaleTimeString()}
                </div>
            </div>
        `;

        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    addBotMessage(response) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';

        // Format message content
        let messageContent = this.formatBotMessage(response.message);
        
        // Add action buttons if any
        let actionButtons = '';
        if (response.actions && response.actions.length > 0) {
            actionButtons = `
                <div class="message-actions">
                    ${response.actions.map(action => `
                        <button class="action-btn" onclick="chatbot.handleAction('${action}')">
                            <i class="fas fa-${this.getActionIcon(action)}"></i>
                            ${this.formatActionText(action)}
                        </button>
                    `).join('')}
                </div>
            `;
        }

        // Status indicator
        const statusClass = response.success ? 'success' : 'error';
        const statusIcon = response.success ? 'fa-check' : 'fa-exclamation-triangle';

        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    ${messageContent}
                    ${actionButtons}
                </div>
                <div class="message-time">
                    ${new Date().toLocaleTimeString()}
                    <span class="message-status ${statusClass}">
                        <i class="fas ${statusIcon}"></i>
                    </span>
                </div>
            </div>
        `;

        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatBotMessage(message) {
        // Convert markdown-like formatting to HTML
        return message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
            .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
            .replace(/^• (.+)$/gm, '<li>$1</li>') // List items
            .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>') // Wrap lists
            .replace(/\n/g, '<br>'); // Line breaks
    }

    getActionIcon(action) {
        const icons = {
            'quality_check': 'fa-check-circle',
            'stock_update': 'fa-edit',
            'view_details': 'fa-eye',
            'dispatch': 'fa-shipping-fast'
        };
        return icons[action] || 'fa-arrow-right';
    }

    formatActionText(action) {
        return action.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    showTyping() {
        this.isTyping = true;
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.style.display = 'flex';
        }
        this.updateSendButton();
    }

    hideTyping() {
        this.isTyping = false;
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.style.display = 'none';
        }
        this.updateSendButton();
    }

    scrollToBottom() {
        const messagesContainer = document.getElementById('chat-messages');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // API helper
    async apiCall(endpoint, options = {}) {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`API call failed: ${response.statusText}`);
        }

        return response.json();
    }

    // Quick message helper
    sendQuickMessage(message) {
        const chatInput = document.getElementById('chat-input');
        chatInput.value = message;
        this.sendMessage();
    }

    // Action handler
    handleAction(action) {
        const actionMessages = {
            'quality_check': 'Start quality check process',
            'stock_update': 'Update stock levels',
            'view_details': 'Show detailed information',
            'dispatch': 'Process dispatch'
        };

        const message = actionMessages[action] || `Execute ${action}`;
        this.sendQuickMessage(message);
    }

    // Clear chat
    clearChat() {
        const messagesContainer = document.getElementById('chat-messages');
        
        // Keep only the welcome message
        const welcomeMessage = messagesContainer.querySelector('.message.bot-message');
        messagesContainer.innerHTML = '';
        if (welcomeMessage) {
            messagesContainer.appendChild(welcomeMessage);
        }

        // Reset counters
        this.messageCount = 0;
        this.sessionStart = new Date();
        this.updateSessionInfo();
        this.updateWelcomeTime();

        this.showToast('Chat cleared', 'info');
    }

    // Toggle info panel
    toggleInfoPanel() {
        const infoPanel = document.getElementById('chat-info');
        if (infoPanel) {
            infoPanel.classList.toggle('open');
        }
    }

    // Toast notifications
    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <p>${message}</p>
            </div>
        `;

        container.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    // Help modal
    showHelpModal() {
        const modal = document.getElementById('help-modal');
        if (modal) {
            modal.style.display = 'flex';
        }
    }

    closeHelpModal() {
        const modal = document.getElementById('help-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    // Load chat history (optional)
    async loadChatHistory() {
        try {
            const history = await this.apiCall(`/api/chat/history/${this.sessionId}`);
            
            // Clear current messages except welcome
            const messagesContainer = document.getElementById('chat-messages');
            const welcomeMessage = messagesContainer.querySelector('.message.bot-message');
            messagesContainer.innerHTML = '';
            if (welcomeMessage) {
                messagesContainer.appendChild(welcomeMessage);
            }

            // Add history messages
            history.reverse().forEach(msg => {
                this.addUserMessage(msg.user_message);
                this.addBotMessage({
                    message: msg.bot_response,
                    intent: msg.intent,
                    success: msg.success
                });
            });

            this.messageCount = history.length * 2;
            this.updateSessionInfo();

        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    }
}

// Global functions for HTML onclick handlers
function sendQuickMessage(message) {
    chatbot.sendQuickMessage(message);
}

function clearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        chatbot.clearChat();
    }
}

function showHelpModal() {
    chatbot.showHelpModal();
}

function closeHelpModal() {
    chatbot.closeHelpModal();
}

function toggleInfoPanel() {
    chatbot.toggleInfoPanel();
}

function sendMessage() {
    chatbot.sendMessage();
}

// Initialize chatbot when DOM is loaded
let chatbot;
document.addEventListener('DOMContentLoaded', () => {
    chatbot = new ChatbotManager();
    
    // Close help modal when clicking outside
    document.getElementById('help-modal').addEventListener('click', (e) => {
        if (e.target.id === 'help-modal') {
            closeHelpModal();
        }
    });
});
