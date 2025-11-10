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
  selector: 'app-zaahen',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="zaahen-container">
      <div class="zaahen-header">
        <div class="zaahen-icon">⚔️</div>
        <h1 class="zaahen-title">ZAAHEN</h1>
        <p class="zaahen-subtitle">AI Coaching Agent</p>
      </div>
      
      <div class="zaahen-content">
        <div class="zaahen-card">
          <h2 class="card-title">PERSONALIZED COACHING</h2>
          <p class="card-description">
            Zaahen analyzes your gameplay patterns, identifies your strengths and weaknesses, 
            and provides personalized coaching insights to help you ascend the ranks.
          </p>
        </div>
        
        <div class="zaahen-card">
          <h2 class="card-title">REAL-TIME ANALYSIS</h2>
          <p class="card-description">
            Get instant feedback on your matches, champion performance, and strategic decisions. 
            Zaahen processes your gameplay data to deliver actionable insights.
          </p>
        </div>
        
        <div class="zaahen-card">
          <h2 class="card-title">STRATEGIC GUIDANCE</h2>
          <p class="card-description">
            Receive tailored recommendations for champion selection, item builds, and gameplay 
            strategies based on your unique playstyle and current meta trends.
          </p>
        </div>
        
        <div class="zaahen-interactive">
          <div class="chat-container">
            <h3 class="chat-title">CONSULT ZAAHEN</h3>
            <div class="chat-messages" #chatMessagesContainer>
              <div *ngIf="messages.length === 0" class="welcome-message">
                <div class="welcome-icon">⚔️</div>
                <p class="welcome-text">Welcome, summoner. I am Zaahen, your AI coaching agent. Ask me anything about your gameplay, strategies, or how to improve your performance on the Rift.</p>
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
                placeholder="Ask Zaahen about your gameplay..."
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
              <span class="hint-text">Press Enter to send, Shift+Enter for new line</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      padding: 40px 20px;
    }
    
    .zaahen-container {
      max-width: 1200px;
      margin: 0 auto;
    }
    
    .zaahen-header {
      text-align: center;
      margin-bottom: 60px;
      padding: 40px 20px;
      background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%);
      border: 2px solid rgba(212, 175, 55, 0.3);
      border-radius: 0;
      box-shadow: 0 0 30px rgba(212, 175, 55, 0.2);
    }
    
    .zaahen-icon {
      font-size: 4em;
      margin-bottom: 20px;
      filter: drop-shadow(0 0 10px rgba(239, 68, 68, 0.5));
    }
    
    .zaahen-title {
      font-size: 3.5em;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: var(--metallic-gold);
      text-shadow: 
        0 0 10px rgba(212, 175, 55, 0.5),
        0 0 20px rgba(212, 175, 55, 0.3),
        0 0 30px rgba(212, 175, 55, 0.2);
      margin-bottom: 10px;
    }
    
    .zaahen-subtitle {
      font-size: 1.2em;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      font-weight: 600;
    }
    
    .zaahen-content {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 24px;
      margin-bottom: 40px;
    }
    
    .zaahen-card {
      background: rgba(15, 15, 20, 0.85);
      border: 2px solid rgba(212, 175, 55, 0.2);
      padding: 30px;
      border-radius: 0;
      transition: all 0.3s ease;
      backdrop-filter: blur(10px);
    }
    
    .zaahen-card:hover {
      border-color: rgba(212, 175, 55, 0.5);
      box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
      transform: translateY(-4px);
    }
    
    .card-title {
      font-size: 1.3em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--metallic-gold);
      margin-bottom: 16px;
      border-bottom: 2px solid rgba(212, 175, 55, 0.3);
      padding-bottom: 12px;
    }
    
    .card-description {
      color: var(--text-secondary);
      line-height: 1.8;
      font-size: 0.95em;
    }
    
    .zaahen-interactive {
      grid-column: 1 / -1;
      margin-top: 20px;
    }
    
    .chat-container {
      background: rgba(15, 15, 20, 0.9);
      border: 2px solid rgba(212, 175, 55, 0.3);
      border-radius: 0;
      padding: 30px;
      backdrop-filter: blur(10px);
      box-shadow: 0 0 30px rgba(212, 175, 55, 0.2);
    }
    
    .chat-title {
      font-size: 1.5em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--metallic-gold);
      margin-bottom: 24px;
      text-align: center;
      border-bottom: 2px solid rgba(212, 175, 55, 0.3);
      padding-bottom: 16px;
    }
    
    .chat-messages {
      min-height: 400px;
      max-height: 600px;
      overflow-y: auto;
      margin-bottom: 24px;
      padding: 20px;
      background: rgba(5, 5, 8, 0.5);
      border: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    
    .welcome-message {
      text-align: center;
      padding: 40px 20px;
      background: rgba(212, 175, 55, 0.05);
      border: 1px solid rgba(212, 175, 55, 0.2);
      border-radius: 0;
    }
    
    .welcome-icon {
      font-size: 3em;
      margin-bottom: 16px;
    }
    
    .welcome-text {
      color: var(--text-secondary);
      line-height: 1.8;
      font-size: 1em;
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
      margin-bottom: 15px;
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
    
    .chat-input-container {
      display: flex;
      gap: 12px;
      align-items: flex-end;
    }
    
    .chat-input {
      flex: 1;
      background: rgba(5, 5, 8, 0.8);
      border: 2px solid rgba(212, 175, 55, 0.3);
      color: var(--text-primary);
      padding: 14px 20px;
      font-size: 1em;
      font-family: inherit;
      border-radius: 0;
      transition: all 0.3s ease;
      resize: none;
      min-height: 50px;
      max-height: 150px;
    }
    
    .chat-input:focus {
      outline: none;
      border-color: rgba(212, 175, 55, 0.6);
      box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
    }
    
    .chat-input:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    
    .chat-input::placeholder {
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    
    .chat-send {
      background: rgba(212, 175, 55, 0.2);
      border: 2px solid rgba(212, 175, 55, 0.5);
      color: var(--metallic-gold);
      padding: 14px 20px;
      font-size: 0.9em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      cursor: pointer;
      transition: all 0.3s ease;
      border-radius: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      min-width: 50px;
      height: 50px;
    }
    
    .chat-send:hover:not(:disabled) {
      background: rgba(212, 175, 55, 0.4);
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
      margin-top: 10px;
      text-align: center;
    }
    
    .hint-text {
      font-size: 0.8em;
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
      border-radius: 0;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
      background: rgba(212, 175, 55, 0.5);
    }
  `]
})
export class ZaahenComponent implements OnInit, AfterViewChecked {
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

  onEnterKey(event: Event): void {
    const keyboardEvent = event as KeyboardEvent;
    if (keyboardEvent.key === 'Enter' && !keyboardEvent.shiftKey) {
      keyboardEvent.preventDefault();
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
      this.error = error.message || 'Failed to get response from Zaahen. Please try again.';
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

