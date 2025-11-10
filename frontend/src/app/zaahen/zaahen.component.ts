import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

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
            <div class="chat-messages" #chatMessages>
              <div class="message agent" *ngFor="let message of messages">
                <div class="message-icon">⚔️</div>
                <div class="message-content">
                  <div class="message-author">ZAAHEN</div>
                  <div class="message-text">{{ message.text }}</div>
                  <div class="message-time">{{ message.time }}</div>
                </div>
              </div>
            </div>
            
            <div class="chat-input-container">
              <input 
                type="text" 
                class="chat-input"
                [(ngModel)]="userInput"
                placeholder="Ask Zaahen about your gameplay..."
                (keyup.enter)="sendMessage()"
              />
              <button class="chat-send" (click)="sendMessage()" [disabled]="!userInput.trim() || loading">
                {{ loading ? 'SENDING...' : 'SEND' }}
              </button>
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
      min-height: 300px;
      max-height: 500px;
      overflow-y: auto;
      margin-bottom: 24px;
      padding: 20px;
      background: rgba(5, 5, 8, 0.5);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .message {
      display: flex;
      gap: 16px;
      margin-bottom: 20px;
      padding: 16px;
      background: rgba(255, 255, 255, 0.03);
      border-left: 3px solid rgba(212, 175, 55, 0.5);
    }
    
    .message-icon {
      font-size: 1.5em;
      flex-shrink: 0;
    }
    
    .message-content {
      flex: 1;
    }
    
    .message-author {
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--metallic-gold);
      margin-bottom: 8px;
      font-size: 0.9em;
    }
    
    .message-text {
      color: var(--text-primary);
      line-height: 1.6;
      margin-bottom: 8px;
    }
    
    .message-time {
      font-size: 0.75em;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    
    .chat-input-container {
      display: flex;
      gap: 12px;
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
    }
    
    .chat-input:focus {
      outline: none;
      border-color: rgba(212, 175, 55, 0.6);
      box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
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
      padding: 14px 32px;
      font-size: 0.9em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      cursor: pointer;
      transition: all 0.3s ease;
      border-radius: 0;
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
export class ZaahenComponent {
  userInput = '';
  loading = false;
  messages: Array<{ text: string; time: string }> = [
    {
      text: 'Welcome, summoner. I am Zaahen, your AI coaching agent. Ask me anything about your gameplay, strategies, or how to improve your performance on the Rift.',
      time: new Date().toLocaleTimeString()
    }
  ];
  
  sendMessage() {
    if (!this.userInput.trim() || this.loading) return;
    
    const userMessage = this.userInput.trim();
    this.userInput = '';
    this.loading = true;
    
    // Simulate AI response (replace with actual API call later)
    setTimeout(() => {
      const responses = [
        `Based on your gameplay patterns, I recommend focusing on ${this.getRandomAdvice()}. This will help you improve your win rate significantly.`,
        `Your performance shows strength in ${this.getRandomStrength()}, but you should work on ${this.getRandomWeakness()} to reach the next level.`,
        `I've analyzed your recent matches. Consider trying ${this.getRandomStrategy()} to adapt to the current meta and improve your overall performance.`,
        `Your champion pool is solid, but I suggest expanding into ${this.getRandomChampion()} to counter common picks in your elo range.`
      ];
      
      this.messages.push({
        text: responses[Math.floor(Math.random() * responses.length)],
        time: new Date().toLocaleTimeString()
      });
      
      this.loading = false;
    }, 1500);
  }
  
  private getRandomAdvice(): string {
    const advice = [
      'map awareness and vision control',
      'early game aggression and lane dominance',
      'teamfight positioning and target selection',
      'objective control and macro decision-making',
      'itemization and build optimization'
    ];
    return advice[Math.floor(Math.random() * advice.length)];
  }
  
  private getRandomStrength(): string {
    const strengths = [
      'late game scaling',
      'mechanical skill',
      'roaming and map pressure',
      'objective control',
      'team coordination'
    ];
    return strengths[Math.floor(Math.random() * strengths.length)];
  }
  
  private getRandomWeakness(): string {
    const weaknesses = [
      'early game consistency',
      'vision control',
      'positioning in teamfights',
      'resource management',
      'adaptability to different matchups'
    ];
    return weaknesses[Math.floor(Math.random() * weaknesses.length)];
  }
  
  private getRandomStrategy(): string {
    const strategies = [
      'a more aggressive early game approach',
      'focusing on objective control',
      'improving your wave management',
      'better vision placement',
      'adapting your build to match situations'
    ];
    return strategies[Math.floor(Math.random() * strategies.length)];
  }
  
  private getRandomChampion(): string {
    const champions = [
      'tank supports',
      'control mages',
      'split-push champions',
      'engage tanks',
      'utility supports'
    ];
    return champions[Math.floor(Math.random() * champions.length)];
  }
}

