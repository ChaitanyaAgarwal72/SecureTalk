class SecureTalkClient {
    constructor() {
        this.socket = io();
        this.username = 'Connecting...';
        this.isTyping = false;
        this.typingTimeout = null;
        this.sharedKey = null;
        this.currentRoom = roomCode || 'default';
        this.currentRoomName = roomName || 'General Chat';
        this.hasJoinedRoom = false;
        this.historyLoaded = false;
        
        this.initializeElements();
        this.setupEventListeners();
        this.setupSocketEvents();
        
        console.log(`SecureTalk Client initialized for room: ${this.currentRoom}`);
    }
    
    initializeElements() {
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-button');
        this.chatMessages = document.getElementById('chat-messages');
        this.usernameDisplay = document.getElementById('username');
        this.userCountDisplay = document.getElementById('user-count');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.toastContainer = document.getElementById('toast-container');
        this.smartRepliesContainer = document.getElementById('smart-replies');
    }
    
    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.messageInput.addEventListener('input', () => this.handleTyping());
    this.messageInput.addEventListener('input', () => this.hideSmartReplies());
        this.messageInput.addEventListener('blur', () => this.stopTyping());
        
        this.messageInput.focus();
    }
    
    setupSocketEvents() {
        this.socket.on('connect', () => {
            console.log('Connected to SecureTalk server');
            this.showToast('Connected to SecureTalk', 'success');
            if (!this.hasJoinedRoom) {
                this.joinRoom();
            }
        });
        
        this.socket.on('disconnect', (reason) => {
            console.log('Disconnected from server:', reason);
            this.showToast('Connection lost. Reconnecting...', 'error');
            this.usernameDisplay.textContent = 'Reconnecting...';
            this.hasJoinedRoom = false;
            this.historyLoaded = false;
        });
        
        this.socket.on('reconnect', (attemptNumber) => {
            console.log('Reconnected to server after', attemptNumber, 'attempts');
            this.showToast('Reconnected successfully!', 'success');
        });
        
        this.socket.on('reconnect_attempt', (attemptNumber) => {
            console.log('Attempting to reconnect... attempt', attemptNumber);
            this.usernameDisplay.textContent = `Reconnecting... (${attemptNumber})`;
        });
        
        this.socket.on('user_connected', (data) => {
            this.username = data.username;
            this.usernameDisplay.textContent = data.username;
            this.showToast(data.message, 'info');
        });
        
        this.socket.on('user_joined', (data) => {
            this.addSystemMessage(`${data.username} joined the chat`);
            this.showToast(`${data.username} joined`, 'info');
        });
        
        this.socket.on('user_left', (data) => {
            this.addSystemMessage(`${data.username} left the chat`);
        });
        
        this.socket.on('room_joined', (data) => {
            console.log(`Joined room: ${data.room} (${data.room_name})`);
            this.showToast(`Joined ${data.room_name}`, 'success');
            this.hasJoinedRoom = true;
        });
        
        this.socket.on('room_stats', (data) => {
            const count = data.user_count;
            this.userCountDisplay.textContent = `${count} user${count !== 1 ? 's' : ''} in room`;
        });
        
        this.socket.on('user_count', (data) => {
            const count = data.count;
            this.userCountDisplay.textContent = `${count} user${count !== 1 ? 's' : ''} online`;
        });
        
        this.socket.on('message_history', (data) => {
            console.log('Received message history:', data.messages.length, 'messages');
            this.loadMessageHistory(data.messages);
        });
        
        this.socket.on('receive_message', (data) => {
            this.receiveMessage(data);
            try {
                const sender = data.username || '';
                if (sender && sender !== this.username) {
                    const messageText = data.message || data.encrypted_message || '';
                    if (messageText && messageText.trim()) {
                        this.fetchSmartReplies(messageText);
                    }
                }
            } catch (e) {
            }
        });
        
        this.socket.on('message_sent', (data) => {
            this.addSentMessage(data.message, data.timestamp);
        });
        
        this.socket.on('user_typing', (data) => {
            this.showTypingIndicator(data.username, data.is_typing);
        });
        
        this.socket.on('error', (data) => {
            this.showToast(`Error: ${data.message}`, 'error');
        });
        
        this.socket.on('room_error', (data) => {
            this.showToast(`Room Error: ${data.error}`, 'error');
            console.error('Room error:', data);
            
            setTimeout(() => {
                window.location.href = '/';
            }, 3000);
        });
    }
    
    joinRoom() {
        if (this.hasJoinedRoom) {
            console.log('Already joined room, skipping...');
            return;
        }
        
        this.historyLoaded = false;
        
        this.socket.emit('join_room', {
            room: this.currentRoom,
            room_name: this.currentRoomName
        });
        console.log(`Joining room: ${this.currentRoom} (${this.currentRoomName})`);
    }
    
    loadMessageHistory(messages) {
        if (this.historyLoaded || this.chatMessages.querySelector('.history-indicator')) {
            console.log('History already loaded, skipping...');
            return;
        }
        
        this.historyLoaded = true;
        
        const welcomeMessage = this.chatMessages.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.style.display = 'none';
        }
        
        if (messages.length > 0) {
            const historyIndicator = document.createElement('div');
            historyIndicator.className = 'history-indicator';
            historyIndicator.innerHTML = `
                <div class="history-line"></div>
                <span>Previous messages (${messages.length})</span>
                <div class="history-line"></div>
            `;
            this.chatMessages.appendChild(historyIndicator);
        }
        
        messages.forEach(msgData => {
            if (msgData.username === this.username) {
                this.addSentMessage(msgData.message, msgData.timestamp, true);
            } else {
                this.addReceivedMessage(msgData.username, msgData.message, msgData.timestamp, true);
            }
        });
        
        this.scrollToBottom();
    }
    
    sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        this.messageInput.value = '';
        this.stopTyping();
        
        this.socket.emit('send_message', {
            message: message,
            timestamp: new Date().toLocaleTimeString()
        });
        
        this.sendButton.disabled = true;
        setTimeout(() => {
            this.sendButton.disabled = false;
            this.messageInput.focus();
        }, 500);
    }
    
    receiveMessage(data) {
        try {
            console.log('Received message data:', data);
            
            const message = data.message || data.encrypted_message || '[No message content]';
            this.addReceivedMessage(data.username, message, data.timestamp);
        } catch (error) {
            console.error('Failed to process message:', error);
            this.addReceivedMessage(data.username, '[Message processing failed]', data.timestamp);
        }
    }

    async fetchSmartReplies(message) {
        try {
            const res = await fetch('/api/smart-replies', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            if (!res.ok) return this.hideSmartReplies();
            const data = await res.json();
            const suggestions = data.suggestions || [];
            this.showSmartReplies(suggestions);
        } catch (e) {
            this.hideSmartReplies();
        }
    }

    showSmartReplies(suggestions) {
        if (!this.smartRepliesContainer) return;
        this.smartRepliesContainer.innerHTML = '';
        if (!suggestions || suggestions.length === 0) {
            this.smartRepliesContainer.style.display = 'none';
            return;
        }
        suggestions.forEach(s => {
            const btn = document.createElement('button');
            btn.className = 'smart-reply-btn';
            btn.textContent = s;
            btn.addEventListener('click', () => {
                this.messageInput.value = s;
                this.messageInput.focus();
                this.messageInput.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            });
            this.smartRepliesContainer.appendChild(btn);
        });
        this.smartRepliesContainer.style.display = 'block';
    }

    hideSmartReplies() {
        if (!this.smartRepliesContainer) return;
        this.smartRepliesContainer.innerHTML = '';
        this.smartRepliesContainer.style.display = 'none';
    }
    
    addSentMessage(message, timestamp, isHistory = false) {
        const messageDiv = this.createMessageElement(message, timestamp, true);
        if (isHistory) {
            messageDiv.classList.add('history-message');
        }
        this.chatMessages.appendChild(messageDiv);
        
        if (!isHistory) {
            this.scrollToBottom();
            this.showNetworkActivity('sent', message.length);
        }
    }
    
    addReceivedMessage(username, message, timestamp, isHistory = false) {
        const messageDiv = this.createMessageElement(message, timestamp, false, username);
        if (isHistory) {
            messageDiv.classList.add('history-message');
        }
        this.chatMessages.appendChild(messageDiv);
        
        if (!isHistory) {
            this.scrollToBottom();
            this.showNetworkActivity('received', message.length);
            
            this.playNotificationSound();
        }
    }
    
    addSystemMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'system-message';
        messageDiv.textContent = message;
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    createMessageElement(message, timestamp, isSent, username = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isSent ? 'message-sent' : 'message-received'}`;
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        content.textContent = message;
        
        const info = document.createElement('div');
        info.className = 'message-info';
        
        if (!isSent && username) {
            const usernameSpan = document.createElement('span');
            usernameSpan.className = 'username-tag';
            usernameSpan.textContent = username;
            info.appendChild(usernameSpan);
        }
        
        if (isSent) {
            const statusSpan = document.createElement('span');
            statusSpan.textContent = 'You';
            info.appendChild(statusSpan);
        }
        
        const timestampSpan = document.createElement('span');
        timestampSpan.className = 'timestamp';
        timestampSpan.textContent = timestamp;
        info.appendChild(timestampSpan);
        
        bubble.appendChild(content);
        bubble.appendChild(info);
        messageDiv.appendChild(bubble);
        
        return messageDiv;
    }
    
    handleTyping() {
        if (!this.isTyping) {
            this.isTyping = true;
            this.socket.emit('typing', { is_typing: true });
        }
        
        if (this.typingTimeout) {
            clearTimeout(this.typingTimeout);
        }
        
        this.typingTimeout = setTimeout(() => {
            this.stopTyping();
        }, 2000);
    }
    
    stopTyping() {
        if (this.isTyping) {
            this.isTyping = false;
            this.socket.emit('typing', { is_typing: false });
        }
        
        if (this.typingTimeout) {
            clearTimeout(this.typingTimeout);
            this.typingTimeout = null;
        }
    }
    
    showTypingIndicator(username, isTyping) {
        const typingText = this.typingIndicator.querySelector('.typing-text');
        
        if (isTyping) {
            typingText.textContent = `${username} is typing...`;
            this.typingIndicator.style.display = 'flex';
            this.scrollToBottom();
        } else {
            this.typingIndicator.style.display = 'none';
        }
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        this.toastContainer.appendChild(toast);
        
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    }
    
    playNotificationSound() {
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.frequency.setValueAtTime(600, audioContext.currentTime + 0.1);
            
            gainNode.gain.setValueAtTime(0, audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(0.1, audioContext.currentTime + 0.01);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.2);
        } catch (error) {
        }
    }
    
    showNetworkActivity(direction, messageSize) {
        const indicator = document.createElement('div');
        indicator.className = `network-activity ${direction}`;
        indicator.innerHTML = `
            <i class="fas fa-${direction === 'sent' ? 'arrow-up' : 'arrow-down'}"></i>
            <span>${messageSize}B</span>
        `;
        
        let activityContainer = document.querySelector('.network-activity-container');
        if (!activityContainer) {
            activityContainer = document.createElement('div');
            activityContainer.className = 'network-activity-container';
            document.body.appendChild(activityContainer);
        }
        
        activityContainer.appendChild(indicator);
        
        setTimeout(() => {
            if (indicator.parentNode) {
                indicator.parentNode.removeChild(indicator);
            }
        }, 2000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const welcomeMessage = document.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.style.opacity = '0';
            setTimeout(() => {
                if (welcomeMessage.parentNode) {
                    welcomeMessage.parentNode.removeChild(welcomeMessage);
                }
            }, 500);
        }
    }, 3000);
    
    window.chatClient = new SecureTalkClient();
});