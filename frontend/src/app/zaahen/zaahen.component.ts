import { Component, OnInit, OnDestroy, ViewChild, ElementRef, AfterViewChecked, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../api.service';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

@Component({
  selector: 'app-zaahen',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="zaahen-page">
      <div class="zaahen-page-header">
        <div class="header-content">
          <div class="zaahen-icon-large">⚔️</div>
          <h1 class="zaahen-page-title">ZAAHEN</h1>
          <p class="zaahen-page-subtitle">AI Coaching Agent powered by Amazon Bedrock</p>
          <p class="zaahen-page-description">
            Chat with Zaahen, your AI coaching agent. Get personalized advice on gameplay, strategies, 
            champion selection, and performance improvement. Powered by Amazon Bedrock AI.
          </p>
        </div>
      </div>
      
      <div class="zaahen-chat-wrapper">
        <div class="chat-container-full">
          <div class="chat-header-bar">
            <div class="chat-header-left">
              <span class="chat-status-indicator"></span>
              <span class="chat-status-text">Amazon Bedrock AI Active</span>
            </div>
            <div class="chat-header-right">
              <span class="bedrock-badge">Powered by Amazon Bedrock</span>
            </div>
          </div>
          
          <div class="chat-messages" #chatMessagesContainer>
            <div *ngIf="messages.length === 0" class="welcome-message">
              <div class="welcome-icon">⚔️</div>
              <h3 class="welcome-title">Welcome to Zaahen</h3>
              <p class="welcome-text">
                I'm Zaahen, your AI coaching agent powered by Amazon Bedrock. 
                I'm here to help you improve your League of Legends gameplay.
              </p>
              <div class="welcome-suggestions">
                <p class="suggestions-title">Ask me about:</p>
                <ul class="suggestions-list">
                  <li>Strategy and tactics</li>
                  <li>Champion recommendations</li>
                  <li>Gameplay improvement tips</li>
                  <li>Match analysis</li>
                  <li>Ranked climb strategies</li>
                  <li>Item builds and runes</li>
                </ul>
              </div>
            </div>
            
            <div *ngFor="let message of messages" 
                 [class]="'message message-' + message.role">
              <div class="message-icon" [attr.data-role]="message.role">
                <span *ngIf="message.role === 'user'">👤</span>
                <span *ngIf="message.role === 'assistant'">⚔️</span>
              </div>
              <div class="message-content">
                <div class="message-author" *ngIf="message.role === 'assistant'">ZAAHEN</div>
                <div class="message-author" *ngIf="message.role === 'user'">YOU</div>
                <div class="message-text" [innerHTML]="formatMessage(message.content)"></div>
                <div class="message-time">{{ formatTimestamp(message.timestamp) }}</div>
              </div>
            </div>
            
            <div *ngIf="isLoading" class="message message-assistant">
              <div class="message-icon" data-role="assistant">
                <span>⚔️</span>
              </div>
              <div class="message-content">
                <div class="message-author">ZAAHEN</div>
                <div class="loading-indicator">
                  <span class="dot"></span>
                  <span class="dot"></span>
                  <span class="dot"></span>
                </div>
                <div class="loading-text">Thinking...</div>
              </div>
            </div>
          </div>
          
          <div *ngIf="error" class="error-message">
            <span class="error-icon">⚠️</span>
            <span>{{ error }}</span>
            <button (click)="dismissError()" class="error-dismiss">×</button>
          </div>
          
          <div class="chat-input-container">
            <textarea
              [(ngModel)]="userMessage"
              (keydown)="onEnterKey($event)"
              (input)="adjustTextareaHeight()"
              placeholder="Ask Zaahen about your gameplay, strategies, or anything League of Legends..."
              [disabled]="isLoading"
              class="chat-input"
              rows="1"
              #messageInput
            ></textarea>
            <button class="chat-send" (click)="sendMessage()" [disabled]="!userMessage.trim() || isLoading">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" *ngIf="!isLoading">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
              <span *ngIf="isLoading">SENDING...</span>
            </button>
          </div>
          <div class="input-footer">
            <span class="hint-text">Press Enter to send, Shift+Enter for new line • Powered by Amazon Bedrock AI</span>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      min-height: calc(100vh - 80px);
      background: var(--bg-dark);
    }
    
    .zaahen-page {
      display: flex;
      flex-direction: column;
      min-height: 100%;
      max-width: 1400px;
      margin: 0 auto;
      padding: 0;
    }
    
    .zaahen-page-header {
      background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(192, 192, 192, 0.1) 100%);
      border-bottom: 2px solid rgba(212, 175, 55, 0.3);
      padding: 60px 40px;
      text-align: center;
    }
    
    .header-content {
      max-width: 800px;
      margin: 0 auto;
    }
    
    .zaahen-icon-large {
      font-size: 5em;
      margin-bottom: 20px;
      filter: drop-shadow(0 0 15px rgba(212, 175, 55, 0.6));
      animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
      0%, 100% {
        transform: scale(1);
        opacity: 1;
      }
      50% {
        transform: scale(1.05);
        opacity: 0.9;
      }
    }
    
    .zaahen-page-title {
      font-size: 4em;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: var(--metallic-gold);
      text-shadow: 
        0 0 10px rgba(212, 175, 55, 0.5),
        0 0 20px rgba(212, 175, 55, 0.3),
        0 0 30px rgba(212, 175, 55, 0.2);
      margin-bottom: 15px;
    }
    
    .zaahen-page-subtitle {
      font-size: 1.3em;
      color: var(--metallic-silver);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      font-weight: 700;
      margin-bottom: 20px;
    }
    
    .zaahen-page-description {
      font-size: 1.1em;
      color: var(--text-secondary);
      line-height: 1.8;
      max-width: 600px;
      margin: 0 auto;
    }
    
    .zaahen-chat-wrapper {
      flex: 1;
      padding: 40px;
      display: flex;
      justify-content: center;
      align-items: flex-start;
    }
    
    .chat-container-full {
      width: 100%;
      max-width: 1000px;
      background: rgba(15, 15, 20, 0.95);
      border: 2px solid rgba(212, 175, 55, 0.3);
      border-radius: 8px;
      backdrop-filter: blur(20px);
      box-shadow: 0 0 40px rgba(212, 175, 55, 0.2);
      display: flex;
      flex-direction: column;
      height: calc(100vh - 400px);
      min-height: 600px;
    }
    
    .chat-header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 24px;
      border-bottom: 1px solid rgba(212, 175, 55, 0.2);
      background: rgba(212, 175, 55, 0.05);
    }
    
    .chat-header-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    
    .chat-status-indicator {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #10b981;
      animation: pulse-dot 2s ease-in-out infinite;
    }
    
    @keyframes pulse-dot {
      0%, 100% {
        opacity: 1;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
      }
      50% {
        opacity: 0.8;
        box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
      }
    }
    
    .chat-status-text {
      color: var(--text-secondary);
      font-size: 0.9em;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    
    .bedrock-badge {
      background: linear-gradient(135deg, rgba(255, 153, 0, 0.2) 0%, rgba(255, 153, 0, 0.1) 100%);
      border: 1px solid rgba(255, 153, 0, 0.4);
      color: #ff9900;
      padding: 6px 12px;
      border-radius: 4px;
      font-size: 0.75em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }
    
    .chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 24px;
      background: rgba(5, 5, 8, 0.3);
      display: flex;
      flex-direction: column;
      gap: 20px;
      min-height: 0;
    }
    
    .welcome-message {
      text-align: center;
      padding: 60px 40px;
      background: rgba(212, 175, 55, 0.08);
      border: 2px solid rgba(212, 175, 55, 0.2);
      border-radius: 8px;
      margin: 20px 0;
    }
    
    .welcome-icon {
      font-size: 4em;
      margin-bottom: 20px;
      filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.5));
    }
    
    .welcome-title {
      font-size: 2em;
      font-weight: 700;
      color: var(--metallic-gold);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 16px;
    }
    
    .welcome-text {
      color: var(--text-secondary);
      line-height: 1.8;
      font-size: 1.1em;
      margin-bottom: 30px;
      max-width: 600px;
      margin-left: auto;
      margin-right: auto;
    }
    
    .welcome-suggestions {
      text-align: left;
      max-width: 500px;
      margin: 0 auto;
      padding-top: 20px;
      border-top: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    .suggestions-title {
      color: var(--metallic-gold);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-size: 0.9em;
      margin-bottom: 12px;
    }
    
    .suggestions-list {
      list-style: none;
      padding: 0;
      margin: 0;
    }
    
    .suggestions-list li {
      padding: 8px 0;
      color: var(--text-primary);
      padding-left: 20px;
      position: relative;
    }
    
    .suggestions-list li:before {
      content: "→";
      position: absolute;
      left: 0;
      color: var(--metallic-gold);
      font-weight: bold;
    }
    
    .loading-text {
      color: var(--text-muted);
      font-size: 0.85em;
      margin-top: 8px;
      font-style: italic;
    }
    
    .message {
      display: flex;
      gap: 16px;
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
    
    .message-icon {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5em;
      flex-shrink: 0;
      background: rgba(212, 175, 55, 0.1);
      border: 2px solid rgba(212, 175, 55, 0.3);
    }
    
    .message-icon[data-role="user"] {
      border-color: rgba(192, 192, 192, 0.5);
      background: rgba(192, 192, 192, 0.1);
    }
    
    .message-icon[data-role="assistant"] {
      border-color: rgba(212, 175, 55, 0.5);
      background: rgba(212, 175, 55, 0.1);
    }
    
    .message-content {
      flex: 1;
      max-width: 70%;
    }
    
    .message-user .message-content {
      text-align: right;
    }
    
    .message-author {
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--metallic-gold);
      margin-bottom: 8px;
      font-size: 0.85em;
    }
    
    .message-user .message-author {
      color: var(--metallic-silver);
    }
    
    .message-text {
      color: var(--text-primary);
      line-height: 1.6;
      margin-bottom: 8px;
      padding: 12px 16px;
      background: rgba(255, 255, 255, 0.03);
      border-left: 3px solid rgba(212, 175, 55, 0.5);
      border-radius: 0;
    }
    
    .message-user .message-text {
      background: rgba(192, 192, 192, 0.05);
      border-left: none;
      border-right: 3px solid rgba(192, 192, 192, 0.5);
    }
    
    .message-time {
      font-size: 0.75em;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-top: 4px;
      padding: 0 4px;
    }
    
    .loading-indicator {
      display: flex;
      gap: 5px;
      padding: 12px 16px;
    }
    
    .loading-indicator .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--metallic-gold);
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
    
    .error-message {
      margin: 15px 24px;
      padding: 15px 20px;
      background: rgba(239, 68, 68, 0.1);
      border: 1px solid rgba(239, 68, 68, 0.4);
      border-radius: 4px;
      color: #ff6b6b;
      display: flex;
      align-items: center;
      gap: 10px;
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
    
    .chat-input-container {
      display: flex;
      gap: 12px;
      align-items: flex-end;
      padding: 20px 24px;
      background: rgba(5, 5, 8, 0.5);
      border-top: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    .chat-input {
      flex: 1;
      background: rgba(255, 255, 255, 0.05);
      border: 2px solid rgba(212, 175, 55, 0.3);
      color: var(--text-primary);
      padding: 14px 20px;
      font-size: 1em;
      font-family: inherit;
      border-radius: 4px;
      transition: all 0.3s ease;
      resize: none;
      min-height: 50px;
      max-height: 150px;
    }
    
    .chat-input:focus {
      outline: none;
      border-color: rgba(212, 175, 55, 0.6);
      box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
      background: rgba(255, 255, 255, 0.08);
    }
    
    .chat-input:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    
    .chat-input::placeholder {
      color: var(--text-muted);
    }
    
    .chat-send {
      background: linear-gradient(135deg, rgba(212, 175, 55, 0.3) 0%, rgba(192, 192, 192, 0.2) 100%);
      border: 2px solid rgba(212, 175, 55, 0.5);
      color: var(--metallic-gold);
      padding: 14px 24px;
      font-size: 0.9em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      cursor: pointer;
      transition: all 0.3s ease;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      min-width: 50px;
      height: 50px;
    }
    
    .chat-send:hover:not(:disabled) {
      background: linear-gradient(135deg, rgba(212, 175, 55, 0.4) 0%, rgba(192, 192, 192, 0.3) 100%);
      border-color: rgba(212, 175, 55, 0.8);
      box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
      transform: translateY(-2px);
    }
    
    .chat-send:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }
    
    .input-footer {
      padding: 10px 24px;
      text-align: center;
      background: rgba(5, 5, 8, 0.3);
      border-top: 1px solid rgba(212, 175, 55, 0.1);
    }
    
    .hint-text {
      font-size: 0.75em;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    
    /* Scrollbar styling */
    .chat-messages::-webkit-scrollbar {
      width: 8px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
      background: rgba(5, 5, 8, 0.5);
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
      background: rgba(212, 175, 55, 0.3);
      border-radius: 4px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
      background: rgba(212, 175, 55, 0.5);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
      .zaahen-page-header {
        padding: 40px 20px;
      }
      
      .zaahen-page-title {
        font-size: 2.5em;
      }
      
      .zaahen-page-subtitle {
        font-size: 1em;
      }
      
      .zaahen-chat-wrapper {
        padding: 20px;
      }
      
      .chat-container-full {
        height: calc(100vh - 300px);
        min-height: 500px;
      }
      
      .chat-header-bar {
        flex-direction: column;
        gap: 10px;
        align-items: flex-start;
      }
      
      .bedrock-badge {
        font-size: 0.65em;
        padding: 4px 8px;
      }
    }
  `]
})
export class ZaahenComponent implements OnInit, OnDestroy, AfterViewInit, AfterViewChecked {
  messages: ChatMessage[] = [];
  userMessage: string = '';
  isLoading: boolean = false;
  error: string | null = null;
  @ViewChild('chatMessagesContainer') private chatContainer!: ElementRef;
  @ViewChild('messageInput') private messageInput!: ElementRef<HTMLTextAreaElement>;

  constructor(private apiService: ApiService) {
    console.log('[ZaahenComponent] Constructor called');
    console.log('[ZaahenComponent] ApiService:', apiService ? 'Available' : 'NULL/MISSING');
    if (!apiService) {
      console.error('[ZaahenComponent] ERROR: ApiService is not injected!');
    }
  }

  ngOnInit(): void {
    console.log('[ZaahenComponent] ngOnInit called');
    console.log('[ZaahenComponent] Component initialized');
    console.log('[ZaahenComponent] Initial messages count:', this.messages.length);
  }

  ngAfterViewInit(): void {
    console.log('[ZaahenComponent] ngAfterViewInit called');
    console.log('[ZaahenComponent] View initialized');
    console.log('[ZaahenComponent] chatContainer:', this.chatContainer ? 'Found' : 'Not found');
    console.log('[ZaahenComponent] messageInput:', this.messageInput ? 'Found' : 'Not found');
    
    // Auto-focus the input when component loads
    setTimeout(() => {
      try {
        if (this.messageInput?.nativeElement) {
          this.messageInput.nativeElement.focus();
          console.log('[ZaahenComponent] Input focused successfully');
        } else {
          console.warn('[ZaahenComponent] messageInput or nativeElement not found');
          console.warn('[ZaahenComponent] messageInput:', this.messageInput);
        }
      } catch (error) {
        console.error('[ZaahenComponent] Error focusing input:', error);
      }
    }, 200);
  }

  ngOnDestroy(): void {
    console.log('[ZaahenComponent] ngOnDestroy called - component is being destroyed');
  }

  ngAfterViewChecked(): void {
    // Only log occasionally to avoid spam
    if (Math.random() < 0.01) {
      console.log('[ZaahenComponent] ngAfterViewChecked called');
    }
    this.scrollToBottom();
  }

  scrollToBottom(): void {
    try {
      if (this.chatContainer) {
        this.chatContainer.nativeElement.scrollTop = this.chatContainer.nativeElement.scrollHeight;
      }
    } catch (err) {
      console.error('[ZaahenComponent] Error scrolling to bottom:', err);
    }
  }

  onEnterKey(event: Event): void {
    const keyboardEvent = event as KeyboardEvent;
    if (keyboardEvent.key === 'Enter' && !keyboardEvent.shiftKey) {
      keyboardEvent.preventDefault();
      this.sendMessage();
    }
  }

  async sendMessage(): Promise<void> {
    console.log('[ZaahenComponent] sendMessage called');
    console.log('[ZaahenComponent] userMessage:', this.userMessage);
    console.log('[ZaahenComponent] isLoading:', this.isLoading);
    
    if (!this.userMessage.trim() || this.isLoading) {
      console.log('[ZaahenComponent] Message empty or already loading, returning');
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
    console.log('[ZaahenComponent] User message added to chat. Total messages:', this.messages.length);

    this.isLoading = true;

    try {
      // Prepare conversation history (all messages except the current one we just added)
      const conversationHistory = this.messages
        .slice(0, -1) // Exclude the last message (the current user message)
        .filter(msg => msg.role === 'user' || msg.role === 'assistant')
        .map(msg => ({
          role: msg.role,
          content: msg.content
        }));
      
      console.log('[ZaahenComponent] Conversation history:', conversationHistory);
      console.log('[ZaahenComponent] Calling API service...');

      // Call API
      const response = await this.apiService.chatWithAgent(userMsg, null, conversationHistory);
      console.log('[ZaahenComponent] API response received:', response);

      // Add assistant response to chat
      this.messages.push({
        role: 'assistant',
        content: response.response,
        timestamp: new Date()
      });
      console.log('[ZaahenComponent] Assistant message added. Total messages:', this.messages.length);
    } catch (error: any) {
      console.error('[ZaahenComponent] Error in sendMessage:', error);
      console.error('[ZaahenComponent] Error details:', {
        message: error?.message,
        status: error?.status,
        error: error?.error,
        stack: error?.stack
      });
      this.error = error.message || error?.error?.message || 'Failed to get response from Zaahen. Please try again.';
      console.error('[ZaahenComponent] Error message set:', this.error);
    } finally {
      this.isLoading = false;
      console.log('[ZaahenComponent] Loading complete');
      
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
    try {
      if (this.messageInput) {
        const textarea = this.messageInput.nativeElement;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
      }
    } catch (error) {
      console.error('[ZaahenComponent] Error adjusting textarea height:', error);
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

