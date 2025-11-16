// AI Retail Agent Team - UI Application
const APP = {
    sessionId: `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    currentAgent: 'retail_coordinator',
    eventSource: null,
    messages: [],

    elements: {
        messages: document.getElementById('messages'),
        messageInput: document.getElementById('messageInput'),
        sendBtn: document.getElementById('sendBtn'),
        clearBtn: document.getElementById('clearBtn'),
        saveBtn: document.getElementById('saveBtn'),
        historyBtn: document.getElementById('historyBtn'),
        historyPanel: document.getElementById('historyPanel'),
        closeHistoryBtn: document.getElementById('closeHistoryBtn'),
        historySearch: document.getElementById('historySearch'),
        historyList: document.getElementById('historyList'),
        emptyHistory: document.getElementById('emptyHistory'),
        toast: document.getElementById('toast'),
        agentCards: document.querySelectorAll('.agent-card'),
        menuBtn: document.getElementById('menuBtn'),
        sidebar: document.getElementById('sidebar'),
        closeSidebarBtn: document.getElementById('closeSidebarBtn'),
        sidebarOverlay: document.getElementById('sidebarOverlay')
    },

    init() {
        this.setupMarkdown();
        this.setupEventListeners();
        this.connectSSE();
        console.log('✅ App initialized. Session:', this.sessionId);
    },

    setupMarkdown() {
        // Configure marked with custom renderer
        marked.setOptions({
            breaks: true,
            gfm: true,
            highlight: function(code, lang) {
                if (lang && hljs.getLanguage(lang)) {
                    try {
                        return hljs.highlight(code, { language: lang }).value;
                    } catch (e) {
                        console.error('Highlight error:', e);
                    }
                }
                return hljs.highlightAuto(code).value;
            }
        });
    },

    setupEventListeners() {
        // Send message
        this.elements.sendBtn.addEventListener('click', () => this.sendMessage());
        this.elements.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        this.elements.messageInput.addEventListener('input', (e) => {
            e.target.style.height = 'auto';
            e.target.style.height = e.target.scrollHeight + 'px';
        });

        // Clear chat
        this.elements.clearBtn.addEventListener('click', () => {
            if (confirm('Clear all messages?')) {
                this.messages = [];
                this.elements.messages.innerHTML = '';
                this.showToast('Chat cleared');
            }
        });

        // Save conversation
        this.elements.saveBtn.addEventListener('click', () => this.saveConversation());

        // History
        this.elements.historyBtn.addEventListener('click', () => this.toggleHistory());
        this.elements.closeHistoryBtn.addEventListener('click', () => this.toggleHistory());
        this.elements.historySearch.addEventListener('input', (e) => 
            this.filterHistory(e.target.value)
        );

        // Agent selection
        this.elements.agentCards.forEach(card => {
            card.addEventListener('click', () => {
                this.elements.agentCards.forEach(c => c.classList.remove('active'));
                card.classList.add('active');
                this.currentAgent = card.dataset.agent;
                this.showToast(`Switched to ${this.currentAgent}`);
                // Close sidebar on mobile after selection
                this.closeSidebar();
            });
        });
        
        // Mobile menu
        if (this.elements.menuBtn) {
            this.elements.menuBtn.addEventListener('click', () => this.toggleSidebar());
        }
        if (this.elements.closeSidebarBtn) {
            this.elements.closeSidebarBtn.addEventListener('click', () => this.closeSidebar());
        }
        if (this.elements.sidebarOverlay) {
            this.elements.sidebarOverlay.addEventListener('click', () => this.closeSidebar());
        }
    },
    
    toggleSidebar() {
        this.elements.sidebar.classList.toggle('open');
        this.elements.sidebarOverlay.classList.toggle('show');
    },
    
    closeSidebar() {
        this.elements.sidebar.classList.remove('open');
        this.elements.sidebarOverlay.classList.remove('show');
    },

    connectSSE() {
        this.eventSource = new EventSource(`/events/${this.sessionId}`);
        
        this.eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'connected') {
                console.log('✅ Connected to server');
            } else if (data.type === 'chunk') {
                this.appendToLastMessage(data.content);
            } else if (data.type === 'complete') {
                // Message complete
            } else if (data.type === 'error') {
                this.showToast('Error: ' + data.error, 'error');
            }
        };

        this.eventSource.onerror = () => {
            console.error('❌ SSE connection error');
            this.showToast('Connection lost', 'error');
        };
    },

    async sendMessage() {
        const text = this.elements.messageInput.value.trim();
        if (!text) return;

        // Add user message
        this.addMessage(text, true);
        this.messages.push({ role: 'user', content: text });
        this.elements.messageInput.value = '';
        this.elements.messageInput.style.height = 'auto';

        // Add agent message placeholder
        this.addMessage('', false);

        // Send to server
        try {
            await fetch(`/send/${this.sessionId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
        } catch (error) {
            this.showToast('Failed to send message', 'error');
        }
    },

    addMessage(content, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'agent'}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = isUser ? 'U' : 'A';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content markdown-body';

        if (isUser) {
            // User messages - plain text
            contentDiv.textContent = content;
        } else {
            // Agent messages - render as markdown
            if (content) {
                const rendered = marked.parse(content);
                contentDiv.innerHTML = DOMPurify.sanitize(rendered);
                // Highlight code blocks
                contentDiv.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });
            }
        }

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);
        this.elements.messages.appendChild(messageDiv);
        this.scrollToBottom();

        return messageDiv;
    },

    appendToLastMessage(text) {
        const lastMessage = this.elements.messages.lastElementChild;
        if (lastMessage && lastMessage.classList.contains('agent')) {
            const content = lastMessage.querySelector('.message-content');
            // Append text and re-render markdown
            const currentText = content.getAttribute('data-raw-text') || '';
            const newText = currentText + text;
            content.setAttribute('data-raw-text', newText);

            // Render markdown
            const rendered = marked.parse(newText);
            content.innerHTML = DOMPurify.sanitize(rendered);

            // Highlight code blocks
            content.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });

            this.scrollToBottom();
        }
    },

    scrollToBottom() {
        requestAnimationFrame(() => {
            this.elements.messages.scrollTo({
                top: this.elements.messages.scrollHeight,
                behavior: 'smooth'
            });
        });
    },

    saveConversation() {
        if (this.messages.length === 0) {
            this.showToast('No messages to save', 'warning');
            return;
        }

        const conversations = this.getConversations();
        const firstUserMsg = this.messages.find(m => m.role === 'user');
        const title = firstUserMsg 
            ? firstUserMsg.content.substring(0, 50) + (firstUserMsg.content.length > 50 ? '...' : '')
            : 'Untitled';

        const conversation = {
            id: `conv_${Date.now()}`,
            title,
            messages: [...this.messages],
            agent: this.currentAgent,
            timestamp: new Date().toISOString()
        };

        conversations.unshift(conversation);
        if (conversations.length > 50) conversations.splice(50);
        
        localStorage.setItem('conversations', JSON.stringify(conversations));
        this.showToast('Conversation saved!');
        this.renderHistory();
    },

    getConversations() {
        try {
            return JSON.parse(localStorage.getItem('conversations') || '[]');
        } catch {
            return [];
        }
    },

    loadConversation(id) {
        const conversations = this.getConversations();
        const conv = conversations.find(c => c.id === id);
        if (!conv) return;

        this.messages = [...conv.messages];
        this.currentAgent = conv.agent;
        this.elements.messages.innerHTML = '';
        
        conv.messages.forEach(msg => {
            this.addMessage(msg.content, msg.role === 'user');
        });

        this.toggleHistory();
        this.showToast('Conversation loaded');
    },

    deleteConversation(id, event) {
        event.stopPropagation();
        if (!confirm('Delete this conversation?')) return;

        const conversations = this.getConversations();
        const filtered = conversations.filter(c => c.id !== id);
        localStorage.setItem('conversations', JSON.stringify(filtered));
        this.renderHistory();
        this.showToast('Conversation deleted');
    },

    toggleHistory() {
        const isOpen = this.elements.historyPanel.classList.toggle('hidden');
        document.querySelector('.main-layout').classList.toggle('history-open');
        if (!isOpen) {
            this.renderHistory();
        }
    },

    renderHistory(filter = '') {
        const conversations = this.getConversations();
        const filtered = filter
            ? conversations.filter(c => 
                c.title.toLowerCase().includes(filter.toLowerCase())
            )
            : conversations;

        if (filtered.length === 0) {
            this.elements.historyList.innerHTML = '';
            this.elements.emptyHistory.style.display = 'block';
            return;
        }

        this.elements.emptyHistory.style.display = 'none';
        this.elements.historyList.innerHTML = filtered.map(conv => `
            <div class="history-item" onclick="APP.loadConversation('${conv.id}')">
                <div class="history-item-title">${this.escapeHtml(conv.title)}</div>
                <div class="history-item-preview">
                    ${conv.messages[0]?.content ? this.escapeHtml(conv.messages[0].content.substring(0, 100)) : ''}
                </div>
                <div class="history-item-meta">
                    ${new Date(conv.timestamp).toLocaleDateString()} • 
                    ${conv.messages.length} messages •
                    <button onclick="APP.deleteConversation('${conv.id}', event)" 
                            style="background:none;border:none;color:#ea4335;cursor:pointer;padding:0;">
                        Delete
                    </button>
                </div>
            </div>
        `).join('');
    },

    filterHistory(term) {
        this.renderHistory(term);
    },

    showToast(message, type = 'info') {
        this.elements.toast.textContent = message;
        this.elements.toast.className = `toast show ${type}`;
        setTimeout(() => {
            this.elements.toast.classList.remove('show');
        }, 3000);
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => APP.init());
} else {
    APP.init();
}
