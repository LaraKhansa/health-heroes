// ===================
// STATE MANAGEMENT
// ===================
let currentConversationId = null;
let isLoading = false;

// ===================
// DOM ELEMENTS
// ===================

const conversationsList = document.getElementById('conversationsList');
const chatMessages = document.getElementById('chatMessages');
const chatInputContainer = document.getElementById('chatInputContainer');
const welcomeScreen = document.getElementById('welcomeScreen');
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const newChatBtn = document.getElementById('newChatBtn');
const startChatBtn = document.getElementById('startChatBtn');
const sidebarToggle = document.getElementById('sidebarToggle');
const closeSidebarBtn = document.getElementById('closeSidebarBtn');
const openSidebarBtn = document.getElementById('openSidebarBtn');
const sidebar = document.getElementById('sidebar');

// ===================
// INITIALIZATION
// ===================

document.addEventListener('DOMContentLoaded', function() {
    loadConversations();
    setupEventListeners();
});

// ===================
// EVENT LISTENERS
// ===================

function setupEventListeners() {
    // Form submission
    chatForm.addEventListener('submit', handleSendMessage);
    
    // Enter key to send (Shift+Enter for new line)
    chatInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage(e);
        }
    });
    
    // New chat buttons
    newChatBtn.addEventListener('click', startNewChat);
    startChatBtn.addEventListener('click', startNewChat);
    
    // Auto-resize textarea
    chatInput.addEventListener('input', autoResizeTextarea);
    
    // Mobile sidebar toggle
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }
    
    // Close sidebar button
    if (closeSidebarBtn) {
        closeSidebarBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (sidebar.classList.contains('hidden')) {
                sidebar.classList.remove('hidden');
                openSidebarBtn.classList.remove('visible');
            } else {
                closeSidebar();
            }
        });
    }
    
    // Open sidebar button
    if (openSidebarBtn) {
        openSidebarBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            sidebar.classList.remove('hidden');
            openSidebarBtn.classList.remove('visible');
        });
    }
}

// ===================
// CONVERSATIONS LIST
// ===================

async function loadConversations() {
    try {
        const response = await fetch('/chatbot/api/conversations');
        const data = await response.json();
        
        if (data.success) {
            displayConversations(data.conversations);
        } else {
            showError('Failed to load conversations');
        }
    } catch (error) {
        console.error('Error loading conversations:', error);
        showError('Failed to load conversations');
    }
}

function displayConversations(conversations) {
    conversationsList.innerHTML = '';
    
    if (conversations.length === 0) {
        conversationsList.innerHTML = `
            <div class="empty-message">
                ${LANGUAGE === 'ar' ? 'لا توجد محادثات بعد' : 'No conversations yet'}
            </div>
        `;
        return;
    }
    
    conversations.forEach(conv => {
        const convElement = createConversationElement(conv);
        conversationsList.appendChild(convElement);
    });
}

function createConversationElement(conversation) {
    const div = document.createElement('div');
    div.className = 'conversation-item';
    div.dataset.conversationId = conversation.id;
    
    const date = formatDate(conversation.updated_at);
    
    div.innerHTML = `
        <div class="conversation-content">
            <span class="conversation-title">${conversation.title}</span>
            <span class="conversation-date">${date}</span>
        </div>
        <button class="delete-conversation-btn" data-conversation-id="${conversation.id}" title="${LANGUAGE === 'ar' ? 'حذف' : 'Delete'}">
            🗑️
        </button>
    `;
    
    // Click on conversation to open it
    div.querySelector('.conversation-content').addEventListener('click', () => loadConversation(conversation.id));
    
    // Click on delete button
    div.querySelector('.delete-conversation-btn').addEventListener('click', (e) => {
        e.stopPropagation();  // Don't open the conversation
        deleteConversation(conversation.id);
    });
    
    return div;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
        return LANGUAGE === 'ar' ? 'اليوم' : 'Today';
    } else if (diffDays === 1) {
        return LANGUAGE === 'ar' ? 'أمس' : 'Yesterday';
    } else if (diffDays < 7) {
        return LANGUAGE === 'ar' ? `منذ ${diffDays} أيام` : `${diffDays} days ago`;
    } else {
        return date.toLocaleDateString(LANGUAGE === 'ar' ? 'ar-AE' : 'en-US', {
            month: 'short',
            day: 'numeric'
        });
    }
}

// ===================
// LOAD CONVERSATION
// ===================

async function loadConversation(conversationId) {
    try {
        const response = await fetch(`/chatbot/api/conversation/${conversationId}`);
        const data = await response.json();
        
        if (data.success) {
            currentConversationId = conversationId;
            displayConversation(data.messages);
            highlightActiveConversation(conversationId);
            
            // Hide welcome, show chat
            welcomeScreen.style.display = 'none';
            chatMessages.style.display = 'flex';
            chatInputContainer.style.display = 'block';
            
            // Close sidebar on mobile
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('active');
            }
        } else {
            showError('Failed to load conversation');
        }
    } catch (error) {
        console.error('Error loading conversation:', error);
        showError('Failed to load conversation');
    }
}

function displayConversation(messages) {
    chatMessages.innerHTML = '';
    
    messages.forEach(msg => {
        const messageElement = createMessageElement(msg);
        chatMessages.appendChild(messageElement);
    });
    
    scrollToBottom();
}

function createMessageElement(message) {
    const div = document.createElement('div');
    div.className = `message ${message.role}`;
    
    // Better icons - no zombie robot!
   const avatar = message.role === 'user' ? '👨‍👩‍👦' : '🤖';
    
    // Parse markdown only for assistant messages
    let messageContent = message.message_text;
    if (message.role === 'assistant' && typeof marked !== 'undefined') {
        try {
            // Configure marked for better formatting
            marked.setOptions({
                breaks: true,  // Convert \n to <br>
                gfm: true      // GitHub Flavored Markdown
            });
            messageContent = marked.parse(messageContent);
        } catch (e) {
            console.error('Error parsing markdown:', e);
            messageContent = escapeHtml(messageContent);
        }
    } else {
        messageContent = escapeHtml(messageContent);
    }
    
    div.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-bubble">
            <div class="message-content">${messageContent}</div>
        </div>
    `;
    
    return div;
}

function highlightActiveConversation(conversationId) {
    // Remove active class from all
    document.querySelectorAll('.conversation-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Add active class to selected
    const activeItem = document.querySelector(`[data-conversation-id="${conversationId}"]`);
    if (activeItem) {
        activeItem.classList.add('active');
    }
}

// ===================
// SEND MESSAGE
// ===================

async function handleSendMessage(e) {
    e.preventDefault();
    
    const message = chatInput.value.trim();
    
    if (!message || isLoading) {
        return;
    }
    
    // Disable input
    isLoading = true;
    chatInput.disabled = true;
    sendBtn.disabled = true;
    
    // Clear input
    chatInput.value = '';
    autoResizeTextarea();
    
    // Show user message immediately
    const userMessage = {
        role: 'user',
        message_text: message
    };
    const userMsgElement = createMessageElement(userMessage);
    chatMessages.appendChild(userMsgElement);
    scrollToBottom();
    
    // Show typing indicator
    const typingIndicator = createTypingIndicator();
    chatMessages.appendChild(typingIndicator);
    scrollToBottom();
    
    try {
        const response = await fetch('/chatbot/api/send-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                conversation_id: currentConversationId,
                message: message,
                language: LANGUAGE
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        typingIndicator.remove();
        
        if (data.success) {
            // Update current conversation ID if new
            if (!currentConversationId) {
                currentConversationId = data.conversation_id;
                
                // Show chat area if it was hidden
                welcomeScreen.style.display = 'none';
                chatMessages.style.display = 'flex';
                chatInputContainer.style.display = 'block';
            }
            
            // Show AI response
            const aiMsgElement = createMessageElement(data.ai_message);
            chatMessages.appendChild(aiMsgElement);
            scrollToBottom();
            
            // Reload conversations list
            loadConversations();
        } else {
            showError(LANGUAGE === 'ar' ? 'فشل إرسال الرسالة' : 'Failed to send message');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        typingIndicator.remove();
        showError(LANGUAGE === 'ar' ? 'حدث خطأ أثناء الإرسال' : 'Error sending message');
    } finally {
        // Re-enable input
        isLoading = false;
        chatInput.disabled = false;
        sendBtn.disabled = false;
        chatInput.focus();
    }
}

function createTypingIndicator() {
    const div = document.createElement('div');
    div.className = 'message assistant';
    div.id = 'typingIndicator';
    
    div.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-bubble">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    
    return div;
}

// ===================
// NEW CHAT
// ===================

function startNewChat() {
    currentConversationId = null;
    
    // Clear messages
    chatMessages.innerHTML = '';
    
    // Show chat area with empty messages and input ready
    welcomeScreen.style.display = 'none';
    chatMessages.style.display = 'flex';
    chatInputContainer.style.display = 'block';
    
    // Remove active highlighting
    document.querySelectorAll('.conversation-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Focus on input
    chatInput.focus();
    
    // Close sidebar on mobile
    if (window.innerWidth <= 768) {
        sidebar.classList.remove('active');
    }
}

// ===================
// DELETE CONVERSATION
// ===================

async function deleteConversation(conversationId) {
    const confirmMessage = LANGUAGE === 'ar' 
        ? 'هل أنت متأكد من حذف هذه المحادثة؟'
        : 'Are you sure you want to delete this conversation?';
    
    if (!confirm(confirmMessage)) {
        return;
    }
    
    try {
        const response = await fetch(`/chatbot/api/conversation/${conversationId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            // If we're viewing the deleted conversation, go back to welcome
            if (currentConversationId === conversationId) {
                startNewChat();
            }
            
            // Reload conversations list
            loadConversations();
            
            // Show success message
            const successMsg = LANGUAGE === 'ar' ? 'تم حذف المحادثة' : 'Conversation deleted';
            console.log(successMsg);
        } else {
            showError(LANGUAGE === 'ar' ? 'فشل حذف المحادثة' : 'Failed to delete conversation');
        }
    } catch (error) {
        console.error('Error deleting conversation:', error);
        showError(LANGUAGE === 'ar' ? 'حدث خطأ أثناء الحذف' : 'Error deleting conversation');
    }
}

// ===================
// UTILITIES
// ===================

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function autoResizeTextarea() {
    chatInput.style.height = 'auto';
    chatInput.style.height = chatInput.scrollHeight + 'px';
}

function toggleSidebar() {
    sidebar.classList.toggle('active');
}

function closeSidebar() {
    sidebar.classList.add('hidden');
    sidebar.classList.remove('active');
    if (window.innerWidth > 768) {
        openSidebarBtn.classList.add('visible');
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/\n/g, '<br>');
}

function showError(message) {
    alert(message);
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', function(e) {
    if (window.innerWidth <= 768) {
        if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    }
});