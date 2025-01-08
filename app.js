// Theme switching
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;
let isDarkTheme = true; // Default to dark theme

function toggleTheme() {
    isDarkTheme = !isDarkTheme;
    body.classList.toggle('dark-theme', isDarkTheme);
}

themeToggle.addEventListener('click', toggleTheme);
body.classList.add('dark-theme'); // Initialize dark theme

// Navigation
const navLinks = document.querySelectorAll('.nav-link, .home-link');
const pages = document.querySelectorAll('.page');

function navigateToPage(pageId) {
    const validPages = ['home', 'novel', 'features', 'about', 'chat'];
    
    if (!validPages.includes(pageId)) {
        pageId = 'error';
    }
    
    pages.forEach(page => {
        page.classList.remove('active');
    });
    navLinks.forEach(link => {
        link.classList.remove('active');
    });

    document.getElementById(`${pageId}-section`).classList.add('active');
    if (pageId !== 'error') {
        document.querySelector(`[data-page="${pageId}"]`)?.classList.add('active');
    }

    // Load content based on page
    if (pageId === 'novel') {
        loadNovel();
    } else if (pageId === 'about') {
        loadAbout();
    }
}

navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        navigateToPage(link.dataset.page);
    });
});

// Load markdown files
async function loadNovel() {
    const chapterList = document.querySelector('.chapter-list');
    const chapters = ['chapter1.md', 'chapter2.md', 'chapter3.md', 'chapter4.md', 'chapter5.md'];
    
    // Create chapter list
    chapterList.innerHTML = chapters.map((chapter, index) => `
        <div class="chapter-item" data-chapter="${chapter}">
            Chapter ${index + 1}
        </div>
    `).join('');

    // Add click handlers
    const chapterItems = document.querySelectorAll('.chapter-item');
    chapterItems.forEach(item => {
        item.addEventListener('click', async () => {
            chapterItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            await loadChapter(item.dataset.chapter);
        });
    });

    // Load first chapter by default
    if (chapters.length > 0) {
        chapterItems[0].classList.add('active');
        await loadChapter(chapters[0]);
    }
}

async function loadChapter(chapter) {
    const storyContent = document.querySelector('.story-content');
    try {
        const response = await fetch(`assets/${chapter}`);
        if (!response.ok) {
            throw new Error(`Failed to load ${chapter}`);
        }
        const text = await response.text();
        
        // Configure marked options for better rendering
        marked.setOptions({
            breaks: true,
            gfm: true,
            headerIds: true,
            mangle: false,
            pedantic: false,
            sanitize: false,
            smartLists: true,
            smartypants: true
        });

        // Render the markdown content
        storyContent.innerHTML = marked.parse(text);
        
        // Scroll to top after loading new content
        storyContent.scrollTop = 0;
        
        // Add active class to current chapter
        const chapterItems = document.querySelectorAll('.chapter-item');
        chapterItems.forEach(item => {
            item.classList.toggle('active', item.dataset.chapter === chapter);
        });
    } catch (error) {
        console.error(`Error loading ${chapter}:`, error);
        storyContent.innerHTML = '<p>Error loading chapter. Please try again later.</p>';
    }
}

async function loadAbout() {
    const aboutContent = document.querySelector('.about-content');
    
    try {
        const response = await fetch('/assets/about.md');
        const text = await response.text();
        aboutContent.innerHTML = marked.parse(text);
    } catch (error) {
        console.error('Error loading about:', error);
        aboutContent.innerHTML = '<p>Error loading content. Please try again later.</p>';
    }
}

// Chat functionality
const messageInput = document.querySelector('.message-input');
const sendButton = document.querySelector('.send-button');
const messagesContainer = document.querySelector('.messages-container');

// Add function to adjust messages container height
function adjustMessagesContainerHeight() {
    const chatContainer = document.querySelector('.chat-container');
    const inputContainer = document.querySelector('.input-container');
    if (chatContainer && inputContainer && messagesContainer) {
        const chatHeight = chatContainer.offsetHeight;
        const inputHeight = inputContainer.offsetHeight;
        messagesContainer.style.height = `${chatHeight - inputHeight}px`;
    }
}

// Call the function on window resize
window.addEventListener('resize', adjustMessagesContainerHeight);

let isSending = false;

function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function appendMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;
    
    const messageAuthor = document.createElement('div');
    messageAuthor.className = 'message-author';
    messageAuthor.textContent = isUser ? 'You' : 'VirPrologue';
    
    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(messageAuthor);
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom(); // 滚动到底部
}

async function sendMessage() {
    const messageInput = document.querySelector('.message-input');
    const message = messageInput.value.trim();
    
    if (message) {
        appendMessage(message, true);
        messageInput.value = '';
        
        // Show loading animation
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message assistant loading';
        const loadingImg = document.createElement('img');
        loadingImg.src = 'assets/wait.png';
        loadingImg.alt = 'Loading...';
        loadingDiv.appendChild(loadingImg);
        document.querySelector('.messages-container').appendChild(loadingDiv);
        
        try {
            const result = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            const data = await result.json();
            
            // Remove loading animation
            document.querySelector('.messages-container').removeChild(loadingDiv);
            
            if (!result.ok) {
                throw new Error(data.error || 'Failed to get response');
            }
            
            appendMessage(data.response, false);
            
        } catch (error) {
            console.error('Error:', error);
            // Remove loading animation if it still exists
            const loadingElement = document.querySelector('.loading');
            if (loadingElement) {
                loadingElement.remove();
            }
            appendMessage('Sorry, there was an error processing your message. Please try again.', false);
        }
    }
}

sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    navigateToPage('home');
    messageInput.focus();
    // Initial adjustment of messages container height
    adjustMessagesContainerHeight();
}); 