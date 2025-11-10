import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../api.service';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

@Component({
  selector: 'app-agent-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="agent-chat-container">
      <div class="chat-header">
        <h2>AI COACHING AGENT</h2>
        <p class="chat-subtitle">Ask me anything about League of Legends strategy, gameplay, or your performance</p>
      </div>
      
      <div class="chat-messages" #chatMessagesContainer>
        <div *ngIf="messages.length === 0" class="welcome-message">
          <div class="welcome-icon">🤖</div>
          <h3>Welcome to the Hall of Legends AI Coach</h3>
          <p>I'm here to help you improve your League of Legends gameplay. Ask me about:</p>
          <ul>
            <li>Strategy and tactics</li>
            <li>Champion recommendations</li>
            <li>Gameplay improvement tips</li>
            <li>Match analysis</li>
            <li>Ranked climb strategies</li>
          </ul>
        </div>
        
        <div *ngFor="let message of messages" 
             [class]="'message message-' + message.role">
          <div class="message-avatar" [attr.data-role]="message.role">
            <span *ngIf="message.role === 'user'">👤</span>
            <span *ngIf="message.role === 'assistant'">🤖</span>
          </div>
          <div class="message-content">
            <div class="message-text" [innerHTML]="formatMessage(message.content)"></div>
            <div class="message-timestamp">{{ formatTimestamp(message.timestamp) }}</div>
          </div>
        </div>
        
        <div *ngIf="isLoading" class="message message-assistant">
          <div class="message-avatar" data-role="assistant">
            <span>🤖</span>
          </div>
          <div class="message-content">
            <div class="loading-indicator">
              <span class="dot"></span>
              <span class="dot"></span>
              <span class="dot"></span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="chat-input-container">
        <div class="input-wrapper">
          <textarea
            [(ngModel)]="userMessage"
            (keydown.enter)="onEnterKey($event)"
            placeholder="Type your message here..."
            [disabled]="isLoading"
            class="chat-input"
            rows="1"
            #messageInput
          ></textarea>
          <button
            (click)="sendMessage()"
            [disabled]="!userMessage.trim() || isLoading"
            class="send-button"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
        <div class="input-footer">
          <span class="hint-text">Press Enter to send, Shift+Enter for new line</span>
        </div>
      </div>
      
      <div *ngIf="error" class="error-message">
        <span class="error-icon">⚠️</span>
        <span>{{ error }}</span>
        <button (click)="dismissError()" class="error-dismiss">×</button>
      </div>
    </div>
  `,
  styles: [`
    .agent-chat-container {
      display: flex;
      flex-direction: column;
      height: 100%;
      max-width: 1200px;
      margin: 0 auto;
      padding: 40px;
      background: var(--bg-dark);
    }
    
    .chat-header {
      text-align: center;
      margin-bottom: 30px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border-color);
    }
    
    .chat-header h2 {
      font-size: 2em;
      font-weight: 700;
      color: var(--metallic-gold);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 10px;
      text-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
    }
    
    .chat-subtitle {
      color: var(--text-secondary);
      font-size: 0.95em;
    }
    
    .chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 20px 0;
      margin-bottom: 20px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    
    .chat-messages::-webkit-scrollbar {
      width: 8px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
      background: var(--bg-darker);
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
      background: var(--border-color);
      border-radius: 4px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
      background: var(--metallic-silver);
    }
    
    .welcome-message {
      text-align: center;
      padding: 60px 40px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 0;
      backdrop-filter: blur(20px);
    }
    
    .welcome-icon {
      font-size: 4em;
      margin-bottom: 20px;
    }
    
    .welcome-message h3 {
      color: var(--metallic-gold);
      font-size: 1.5em;
      margin-bottom: 20px;
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }
    
    .welcome-message p {
      color: var(--text-secondary);
      margin-bottom: 20px;
      font-size: 1.1em;
    }
    
    .welcome-message ul {
      list-style: none;
      padding: 0;
      text-align: left;
      max-width: 400px;
      margin: 0 auto;
    }
    
    .welcome-message li {
      padding: 10px 0;
      color: var(--text-primary);
      border-bottom: 1px solid var(--border-color);
    }
    
    .welcome-message li:before {
      content: "→ ";
      color: var(--metallic-gold);
      font-weight: bold;
      margin-right: 10px;
    }
    
    .message {
      display: flex;
      gap: 15px;
      animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: translateY(10px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    
    .message-user {
      flex-direction: row-reverse;
    }
    
    .message-avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5em;
      flex-shrink: 0;
      background: var(--bg-card);
      border: 2px solid var(--border-color);
    }
    
    .message-avatar[data-role="user"] {
      border-color: var(--metallic-gold);
      background: rgba(212, 175, 55, 0.1);
    }
    
    .message-avatar[data-role="assistant"] {
      border-color: var(--metallic-silver);
      background: rgba(192, 192, 192, 0.1);
    }
    
    .message-content {
      flex: 1;
      max-width: 70%;
    }
    
    .message-user .message-content {
      text-align: right;
    }
    
    .message-text {
      padding: 15px 20px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 0;
      color: var(--text-primary);
      line-height: 1.6;
      backdrop-filter: blur(20px);
      white-space: pre-wrap;
      word-wrap: break-word;
    }
    
    .message-user .message-text {
      background: rgba(212, 175, 55, 0.1);
      border-color: var(--metallic-gold);
    }
    
    .message-assistant .message-text {
      background: rgba(192, 192, 192, 0.05);
      border-color: var(--border-color);
    }
    
    .message-timestamp {
      font-size: 0.75em;
      color: var(--text-muted);
      margin-top: 5px;
      padding: 0 5px;
    }
    
    .loading-indicator {
      display: flex;
      gap: 5px;
      padding: 15px 20px;
    }
    
    .loading-indicator .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--metallic-silver);
      animation: bounce 1.4s infinite ease-in-out both;
    }
    
    .loading-indicator .dot:nth-child(1) {
      animation-delay: -0.32s;
    }
    
    .loading-indicator .dot:nth-child(2) {
      animation-delay: -0.16s;
    }
    
    @keyframes bounce {
      0%, 80%, 100% {
        transform: scale(0);
      }
      40% {
        transform: scale(1);
      }
    }
    
    .chat-input-container {
      border-top: 1px solid var(--border-color);
      padding-top: 20px;
    }
    
    .input-wrapper {
      display: flex;
      gap: 10px;
      align-items: flex-end;
    }
    
    .chat-input {
      flex: 1;
      padding: 14px 16px;
      border: 1px solid var(--border-color);
      border-radius: 0;
      font-size: 16px;
      font-family: inherit;
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-primary);
      resize: none;
      min-height: 50px;
      max-height: 150px;
      backdrop-filter: blur(10px);
      transition: all 0.3s;
    }
    
    .chat-input:focus {
      outline: none;
      border-color: var(--metallic-gold);
      box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
      background: rgba(255, 255, 255, 0.08);
    }
    
    .chat-input:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    
    .chat-input::placeholder {
      color: var(--text-muted);
    }
    
    .send-button {
      padding: 14px 20px;
      background: linear-gradient(135deg, rgba(212, 175, 55, 0.2) 0%, rgba(192, 192, 192, 0.2) 100%);
      border: 1px solid var(--metallic-gold);
      color: var(--text-primary);
      cursor: pointer;
      transition: all 0.3s;
      display: flex;
      align-items: center;
      justify-content: center;
      min-width: 50px;
      height: 50px;
    }
    
    .send-button:hover:not(:disabled) {
      background: linear-gradient(135deg, rgba(212, 175, 55, 0.3) 0%, rgba(192, 192, 192, 0.3) 100%);
      box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
      transform: translateY(-2px);
    }
    
    .send-button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }
    
    .input-footer {
      margin-top: 10px;
      text-align: center;
    }
    
    .hint-text {
      font-size: 0.8em;
      color: var(--text-muted);
    }
    
    .error-message {
      margin-top: 15px;
      padding: 15px 20px;
      background: rgba(239, 68, 68, 0.1);
      border: 1px solid rgba(239, 68, 68, 0.4);
      color: #ff6b6b;
      display: flex;
      align-items: center;
      gap: 10px;
      border-radius: 0;
    }
    
    .error-icon {
      font-size: 1.2em;
    }
    
    .error-dismiss {
      margin-left: auto;
      background: none;
      border: none;
      color: #ff6b6b;
      font-size: 1.5em;
      cursor: pointer;
      padding: 0;
      width: 24px;
      height: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .error-dismiss:hover {
      opacity: 0.7;
    }
    
    @media (max-width: 768px) {
      .agent-chat-container {
        padding: 20px;
        height: calc(100vh - 150px);
      }
      
      .message-content {
        max-width: 85%;
      }
      
      .chat-header h2 {
        font-size: 1.5em;
      }
    }
  `]
})
export class AgentChatComponent implements OnInit, AfterViewChecked {
  messages: ChatMessage[] = [];
  userMessage: string = '';
  isLoading: boolean = false;
  error: string | null = null;
  @ViewChild('chatMessagesContainer') private chatContainer!: ElementRef;
  @ViewChild('messageInput') private messageInput!: ElementRef<HTMLTextAreaElement>;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    // Auto-focus the input when component loads
    setTimeout(() => {
      if (this.messageInput) {
        this.messageInput.nativeElement.focus();
      }
    }, 100);
  }

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  scrollToBottom(): void {
    try {
      if (this.chatContainer) {
        this.chatContainer.nativeElement.scrollTop = this.chatContainer.nativeElement.scrollHeight;
      }
    } catch (err) {
      // Ignore scroll errors
    }
  }

  onEnterKey(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  async sendMessage(): Promise<void> {
    if (!this.userMessage.trim() || this.isLoading) {
      return;
    }

    const userMsg = this.userMessage.trim();
    this.userMessage = '';
    this.error = null;

    // Add user message to chat
    const userMessage: ChatMessage = {
      role: 'user',
      content: userMsg,
      timestamp: new Date()
    };
    this.messages.push(userMessage);

    this.isLoading = true;

    try {
      // Prepare conversation history (all messages except the current one we just added)
      // This way the backend receives history without the current message
      const conversationHistory = this.messages
        .slice(0, -1) // Exclude the last message (the current user message)
        .filter(msg => msg.role === 'user' || msg.role === 'assistant')
        .map(msg => ({
          role: msg.role,
          content: msg.content
        }));

      // Call API
      const response = await this.apiService.chatWithAgent(userMsg, null, conversationHistory);

      // Add assistant response to chat
      this.messages.push({
        role: 'assistant',
        content: response.response,
        timestamp: new Date()
      });
    } catch (error: any) {
      this.error = error.message || 'Failed to get response from agent. Please try again.';
      console.error('Chat error:', error);
    } finally {
      this.isLoading = false;
      // Auto-resize textarea
      this.adjustTextareaHeight();
      // Focus back on input
      setTimeout(() => {
        if (this.messageInput) {
          this.messageInput.nativeElement.focus();
        }
      }, 100);
    }
  }

  adjustTextareaHeight(): void {
    if (this.messageInput) {
      const textarea = this.messageInput.nativeElement;
      textarea.style.height = 'auto';
      textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
    }
  }

  formatMessage(content: string): string {
    // Simple formatting: convert newlines to <br> and escape HTML
    return content
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/\n/g, '<br>');
  }

  formatTimestamp(timestamp: Date): string {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  dismissError(): void {
    this.error = null;
  }
}

