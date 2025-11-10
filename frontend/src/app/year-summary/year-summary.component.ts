import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../api.service';

interface YearSummaryData {
  year: number;
  summary: {
    total_games?: number;
    win_rate?: number;
    best_champion?: string;
    most_played_champions?: Array<{ champion: string; games: number }>;
    key_metrics?: {
      avg_kda?: number;
      avg_damage?: number;
      avg_gold?: number;
    };
    improvement?: number;
  };
  highlights: Array<{ type: string; description: string }>;
  strengths: string[];
  weaknesses: string[];
  growth_areas: string[];
  ai_generated_summary: string;
  shareable_content?: {
    share_text?: string;
    share_image?: string;
  };
}

@Component({
  selector: 'app-year-summary',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="year-summary-container">
      <!-- Input Section -->
      <div class="input-section" *ngIf="!summaryData && !loading">
        <div class="input-card">
          <h2 class="section-title">YOUR 2024 WRAPPED</h2>
          <p class="section-subtitle">🎮 Discover your year in League of Legends 🏆</p>
          <p class="section-note">📌 Access this page by clicking "YEAR SUMMARY" in the navigation bar above</p>
          
          <div class="form-group">
            <label for="summonerName">Riot ID (GameName#Tag)</label>
            <input 
              type="text" 
              id="summonerName" 
              [(ngModel)]="summonerName"
              placeholder="e.g., Faker#KR1"
              (keyup.enter)="fetchYearSummary()"
              class="input-field"
            />
          </div>
          
          <div class="form-group">
            <label for="region">Region</label>
            <select id="region" [(ngModel)]="region" class="input-field">
              <option value="na1">NA (North America)</option>
              <option value="euw1">EUW (Europe West)</option>
              <option value="eun1">EUN (Europe Nordic & East)</option>
              <option value="kr">KR (Korea)</option>
              <option value="br1">BR (Brazil)</option>
              <option value="la1">LAN (Latin America North)</option>
              <option value="la2">LAS (Latin America South)</option>
              <option value="oc1">OCE (Oceania)</option>
              <option value="ru">RU (Russia)</option>
              <option value="tr1">TR (Turkey)</option>
              <option value="jp1">JP (Japan)</option>
            </select>
          </div>
          
          <button 
            class="btn-generate" 
            (click)="fetchYearSummary()"
            [disabled]="loading || !summonerName.trim()"
          >
            {{ loading ? 'GENERATING...' : '🚀 GENERATE MY WRAPPED' }}
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div class="loading-section" *ngIf="loading">
        <div class="loading-spinner"></div>
        <p class="loading-text">🎯 Creating your 2024 Wrapped...</p>
        <p class="loading-subtext">Analyzing your epic plays and... questionable decisions</p>
      </div>

      <!-- Error State -->
      <div class="error-section" *ngIf="error && !loading">
        <div class="error-card">
          <div class="error-icon">⚠️</div>
          <h3 class="error-title">{{ getErrorTitle() }}</h3>
          <p class="error-message">{{ error }}</p>
          <button class="btn-retry" (click)="fetchYearSummary()">TRY AGAIN</button>
        </div>
      </div>

      <!-- Wrapped Cards -->
      <div class="wrapped-cards" *ngIf="summaryData && !loading">
        <!-- Card 1: Welcome -->
        <div class="wrapped-card card-1" [class.active]="currentCard === 0">
          <div class="card-content">
            <div class="card-number">1 / {{ totalCards }}</div>
            <div class="card-emoji">🎮</div>
            <h1 class="card-title">YOUR 2024 WRAPPED</h1>
            <p class="card-subtitle">Ready to see your year in League?</p>
            <div class="player-name">{{ summonerName }}</div>
            <p class="card-witty">*cue dramatic music*</p>
          </div>
        </div>

        <!-- Card 2: Total Games with Witty Joke -->
        <div class="wrapped-card card-2" [class.active]="currentCard === 1">
          <div class="card-content">
            <div class="card-number">2 / {{ totalCards }}</div>
            <p class="card-label">YOU PLAYED</p>
            <h1 class="card-big-number">{{ summaryData?.summary?.total_games || 0 }}</h1>
            <p class="card-description">GAMES IN 2024</p>
            <div class="witty-joke">
              <p class="joke-text">{{ getGamesJoke() }}</p>
            </div>
          </div>
        </div>

        <!-- Card 3: Win Rate with Personality -->
        <div class="wrapped-card card-3" [class.active]="currentCard === 2">
          <div class="card-content">
            <div class="card-number">3 / {{ totalCards }}</div>
            <p class="card-label">YOUR WIN RATE</p>
            <h1 class="card-big-number">{{ (summaryData?.summary?.win_rate || 0).toFixed(1) }}%</h1>
            <p class="card-description">{{ getWinRateDescription() }}</p>
            <div class="witty-joke">
              <p class="joke-text">{{ getWinRateJoke() }}</p>
            </div>
          </div>
        </div>

        <!-- Card 4: Top Champions -->
        <div class="wrapped-card card-4" [class.active]="currentCard === 3">
          <div class="card-content">
            <div class="card-number">4 / {{ totalCards }}</div>
            <p class="card-label">YOUR RIDE OR DIE</p>
            <h1 class="card-champion">{{ summaryData?.summary?.best_champion || 'N/A' }}</h1>
            <p class="card-champion-subtitle">{{ getChampionJoke() }}</p>
            <div class="top-champions" *ngIf="getTopChampions().length > 0">
              <div class="champion-item" *ngFor="let champ of getTopChampions(); let i = index">
                <span class="champion-rank">#{{ i + 1 }}</span>
                <span class="champion-name">{{ champ.champion }}</span>
                <span class="champion-games">{{ champ.games }} {{ champ.games === 1 ? 'game' : 'games' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Card 5: KDA Stats with Humor -->
        <div class="wrapped-card card-5" [class.active]="currentCard === 4">
          <div class="card-content">
            <div class="card-number">5 / {{ totalCards }}</div>
            <p class="card-label">YOUR KDA</p>
            <h1 class="card-big-number">{{ getFormattedKDA() }}</h1>
            <p class="card-description">{{ getKDADescription() }}</p>
            <div class="witty-joke">
              <p class="joke-text">{{ getKDAJoke() }}</p>
            </div>
          </div>
        </div>

        <!-- Card 6: Damage Stats -->
        <div class="wrapped-card card-5b" [class.active]="currentCard === 5">
          <div class="card-content">
            <div class="card-number">6 / {{ totalCards }}</div>
            <p class="card-label">YOUR DAMAGE</p>
            <h1 class="card-big-number">{{ getFormattedDamage() }}</h1>
            <p class="card-description">AVERAGE DAMAGE PER GAME</p>
            <div class="witty-joke">
              <p class="joke-text">{{ getDamageJoke() }}</p>
            </div>
          </div>
        </div>

        <!-- Card 7: Gold Stats -->
        <div class="wrapped-card card-5c" [class.active]="currentCard === 6">
          <div class="card-content">
            <div class="card-number">7 / {{ totalCards }}</div>
            <p class="card-label">YOUR GOLD</p>
            <h1 class="card-big-number">{{ getFormattedGold() }}</h1>
            <p class="card-description">AVERAGE GOLD PER GAME</p>
            <div class="witty-joke">
              <p class="joke-text">{{ getGoldJoke() }}</p>
            </div>
          </div>
        </div>

        <!-- Card 8: Highlights with Emojis -->
        <div class="wrapped-card card-6" [class.active]="currentCard === 7">
          <div class="card-content">
            <div class="card-number">8 / {{ totalCards }}</div>
            <p class="card-label">YOUR HIGHLIGHTS</p>
            <div class="highlights-list">
              <div class="highlight-item" *ngFor="let highlight of summaryData?.highlights || []; let i = index">
                <div class="highlight-icon">{{ getHighlightEmoji(highlight.type) }}</div>
                <div class="highlight-text">{{ highlight.description }}</div>
              </div>
              <div class="highlight-item" *ngIf="(summaryData?.highlights || []).length === 0">
                <div class="highlight-icon">📝</div>
                <div class="highlight-text">Your highlights are loading... or you're just really consistent!</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Card 7: Playstyle Analysis -->
        <div class="wrapped-card card-7" [class.active]="currentCard === 6">
          <div class="card-content">
            <div class="card-number">7 / {{ totalCards }}</div>
            <p class="card-label">YOUR PLAYSTYLE</p>
            <div class="playstyle-analysis">
              <div class="playstyle-item">
                <div class="playstyle-icon">🎯</div>
                <div class="playstyle-text">
                  <strong>{{ getPlaystyleType() }}</strong>
                  <span class="playstyle-subtitle">{{ getPlaystyleDescription() }}</span>
                </div>
              </div>
              <div class="playstyle-stats">
                <div class="stat-item">
                  <span class="stat-label">Aggression</span>
                  <div class="stat-bar">
                    <div class="stat-fill" [style.width.%]="getAggressionLevel()"></div>
                  </div>
                  <span class="stat-value">{{ getAggressionLevel() }}%</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Consistency</span>
                  <div class="stat-bar">
                    <div class="stat-fill" [style.width.%]="getConsistencyLevel()"></div>
                  </div>
                  <span class="stat-value">{{ getConsistencyLevel() }}%</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Team Player</span>
                  <div class="stat-bar">
                    <div class="stat-fill" [style.width.%]="getTeamPlayerLevel()"></div>
                  </div>
                  <span class="stat-value">{{ getTeamPlayerLevel() }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Card 8: Strengths & Weaknesses -->
        <div class="wrapped-card card-8" [class.active]="currentCard === 7">
          <div class="card-content">
            <div class="card-number">8 / {{ totalCards }}</div>
            <p class="card-label">YOUR SUPERPOWERS</p>
            <div class="strengths-list">
              <div class="strength-item" *ngFor="let strength of summaryData?.strengths || []">
                <span class="strength-icon">⚡</span>
                <span class="strength-text">{{ strength }}</span>
              </div>
              <div class="strength-item" *ngIf="(summaryData?.strengths || []).length === 0">
                <span class="strength-icon">🎯</span>
                <span class="strength-text">You're a mystery wrapped in an enigma!</span>
              </div>
            </div>
            <div class="weaknesses-list" *ngIf="(summaryData?.weaknesses || []).length > 0">
              <p class="weaknesses-label">Areas to improve (no judgment! 😅)</p>
              <div class="weakness-item" *ngFor="let weakness of summaryData?.weaknesses">
                <span class="weakness-icon">💡</span>
                <span class="weakness-text">{{ weakness }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Card 9: Fun Facts -->
        <div class="wrapped-card card-9" [class.active]="currentCard === 8">
          <div class="card-content">
            <div class="card-number">9 / {{ totalCards }}</div>
            <p class="card-label">FUN FACTS</p>
            <div class="fun-facts">
              <div class="fun-fact-item">
                <div class="fun-fact-icon">⏱️</div>
                <div class="fun-fact-text">
                  <strong>{{ getEstimatedHours() }}</strong> hours spent in the Rift
                  <span class="fun-fact-subtitle">That's {{ getDaysEquivalent() }} days of pure dedication!</span>
                </div>
              </div>
              <div class="fun-fact-item" *ngIf="getImprovementText()">
                <div class="fun-fact-icon">📈</div>
                <div class="fun-fact-text">
                  <strong>{{ getImprovementText() }}</strong>
                  <span class="fun-fact-subtitle">You're on the up and up!</span>
                </div>
              </div>
              <div class="fun-fact-item">
                <div class="fun-fact-icon">🎲</div>
                <div class="fun-fact-text">
                  <strong>{{ getWinLossBreakdown() }}</strong>
                  <span class="fun-fact-subtitle">{{ getWinLossJoke() }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Card 10: Growth Areas -->
        <div class="wrapped-card card-10" [class.active]="currentCard === 9">
          <div class="card-content">
            <div class="card-number">10 / {{ totalCards }}</div>
            <p class="card-label">YOUR GROWTH</p>
            <div class="growth-areas">
              <div class="growth-item" *ngFor="let area of summaryData?.growth_areas || []">
                <div class="growth-icon">🌱</div>
                <div class="growth-text">{{ area }}</div>
              </div>
              <div class="growth-item" *ngIf="(summaryData?.growth_areas || []).length === 0">
                <div class="growth-icon">✨</div>
                <div class="growth-text">You're already perfect! Just kidding, there's always room to grow! 🚀</div>
              </div>
            </div>
            <div class="witty-joke" style="margin-top: 30px;">
              <p class="joke-text">{{ getGrowthJoke() }}</p>
            </div>
          </div>
        </div>

        <!-- Card 11: Monthly Breakdown -->
        <div class="wrapped-card card-11" [class.active]="currentCard === 10">
          <div class="card-content">
            <div class="card-number">11 / {{ totalCards }}</div>
            <p class="card-label">YOUR YEAR BREAKDOWN</p>
            <div class="year-breakdown">
              <div class="breakdown-item">
                <div class="breakdown-icon">📅</div>
                <div class="breakdown-text">
                  <strong>{{ getGamesPerMonth() }}</strong> games per month on average
                  <span class="breakdown-subtitle">{{ getMonthlyJoke() }}</span>
                </div>
              </div>
              <div class="breakdown-item">
                <div class="breakdown-icon">🔥</div>
                <div class="breakdown-text">
                  <strong>{{ getBestMonth() }}</strong> was your most active month
                  <span class="breakdown-subtitle">{{ getBestMonthJoke() }}</span>
                </div>
              </div>
              <div class="breakdown-item">
                <div class="breakdown-icon">⚡</div>
                <div class="breakdown-text">
                  <strong>{{ getPeakPerformance() }}</strong>
                  <span class="breakdown-subtitle">{{ getPeakJoke() }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Card 12: AI Summary -->
        <div class="wrapped-card card-12" [class.active]="currentCard === 11">
          <div class="card-content">
            <div class="card-number">12 / {{ totalCards }}</div>
            <p class="card-label">YOUR YEAR IN REVIEW</p>
            <p class="card-ai-summary">{{ summaryData?.ai_generated_summary || 'Your year was... eventful! Keep grinding, summoner!' }}</p>
          </div>
        </div>

        <!-- Card 14: Comparison Card -->
        <div class="wrapped-card card-14" [class.active]="currentCard === 13">
          <div class="card-content">
            <div class="card-number">14 / {{ totalCards }}</div>
            <p class="card-label">HOW YOU STACK UP</p>
            <div class="comparison-stats">
              <div class="comparison-item">
                <div class="comparison-icon">🌍</div>
                <div class="comparison-text">
                  <strong>{{ getGlobalRanking() }}</strong>
                  <span class="comparison-subtitle">{{ getRankingJoke() }}</span>
                </div>
              </div>
              <div class="comparison-item">
                <div class="comparison-icon">📊</div>
                <div class="comparison-text">
                  <strong>{{ getPercentile() }}</strong> percentile
                  <span class="comparison-subtitle">{{ getPercentileJoke() }}</span>
                </div>
              </div>
              <div class="comparison-item">
                <div class="comparison-icon">🏅</div>
                <div class="comparison-text">
                  <strong>{{ getAchievementLevel() }}</strong>
                  <span class="comparison-subtitle">{{ getAchievementJoke() }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Card 15: Share -->
        <div class="wrapped-card card-15" [class.active]="currentCard === 14">
          <div class="card-content">
            <div class="card-number">15 / {{ totalCards }}</div>
            <div class="card-emoji">🎉</div>
            <h1 class="card-title">THANKS FOR PLAYING!</h1>
            <p class="card-subtitle">Share your 2024 stats and flex on your friends</p>
            <button class="btn-share" (click)="shareWrapped()">📤 SHARE YOUR WRAPPED</button>
            <p class="card-witty">See you on the Rift in 2025! 🚀</p>
            <p class="card-witty" style="margin-top: 20px; font-size: 0.9em;">Click "YEAR SUMMARY" in the nav to generate another wrapped!</p>
          </div>
        </div>

        <!-- Navigation -->
        <div class="card-navigation" *ngIf="summaryData">
          <button 
            class="nav-btn prev" 
            (click)="previousCard()" 
            [disabled]="currentCard === 0"
            title="Previous"
          >
            ←
          </button>
          <div class="card-dots">
            <span 
              *ngFor="let card of [].constructor(totalCards); let i = index"
              class="dot"
              [class.active]="currentCard === i"
              (click)="goToCard(i)"
              [title]="'Go to card ' + (i + 1)"
            ></span>
          </div>
          <button 
            class="nav-btn next" 
            (click)="nextCard()" 
            [disabled]="currentCard === totalCards - 1"
            title="Next"
          >
            →
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      min-height: 100vh;
      padding: 40px 20px;
      background: linear-gradient(180deg, rgba(5, 5, 8, 0.95) 0%, rgba(10, 10, 15, 0.98) 100%);
    }

    .year-summary-container {
      max-width: 1200px;
      margin: 0 auto;
    }

    /* Input Section */
    .input-section {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 60vh;
    }

    .input-card {
      background: rgba(15, 15, 20, 0.95);
      border: 2px solid rgba(212, 175, 55, 0.3);
      padding: 40px;
      border-radius: 20px;
      max-width: 500px;
      width: 100%;
      backdrop-filter: blur(20px);
      box-shadow: 0 0 40px rgba(212, 175, 55, 0.3);
    }

    .section-title {
      font-size: 2.8em;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      text-align: center;
      margin-bottom: 10px;
      background: linear-gradient(135deg, #f4d03f 0%, #d4af37 50%, #f4d03f 100%);
      background-size: 200% 200%;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      animation: shimmer 3s ease-in-out infinite;
    }

    @keyframes shimmer {
      0%, 100% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
    }

    .section-subtitle {
      text-align: center;
      color: var(--text-secondary);
      margin-bottom: 15px;
      font-size: 1.2em;
    }

    .section-note {
      text-align: center;
      color: var(--text-muted);
      margin-bottom: 30px;
      font-size: 0.9em;
      font-style: italic;
      padding: 10px;
      background: rgba(212, 175, 55, 0.1);
      border-radius: 8px;
      border: 1px solid rgba(212, 175, 55, 0.2);
    }

    .form-group {
      margin-bottom: 24px;
    }

    .form-group label {
      display: block;
      font-size: 0.9em;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-secondary);
      margin-bottom: 8px;
    }

    .input-field {
      width: 100%;
      background: rgba(5, 5, 8, 0.9);
      border: 2px solid rgba(212, 175, 55, 0.3);
      color: var(--text-primary);
      padding: 12px 16px;
      font-size: 1em;
      font-family: inherit;
      border-radius: 10px;
      transition: all 0.3s ease;
    }

    .input-field:focus {
      outline: none;
      border-color: rgba(212, 175, 55, 0.7);
      box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
      transform: translateY(-2px);
    }

    .btn-generate {
      width: 100%;
      background: linear-gradient(135deg, #f4d03f 0%, #d4af37 100%);
      border: none;
      color: var(--bg-dark);
      padding: 18px 32px;
      font-size: 1.2em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      cursor: pointer;
      transition: all 0.3s ease;
      border-radius: 10px;
      box-shadow: 0 6px 25px rgba(244, 208, 63, 0.5);
    }

    .btn-generate:hover:not(:disabled) {
      transform: translateY(-3px);
      box-shadow: 0 8px 35px rgba(244, 208, 63, 0.7);
    }

    .btn-generate:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    /* Loading State */
    .loading-section {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 60vh;
    }

    .loading-spinner {
      width: 70px;
      height: 70px;
      border: 5px solid rgba(212, 175, 55, 0.2);
      border-top: 5px solid var(--metallic-gold);
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin-bottom: 24px;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    .loading-text {
      font-size: 1.3em;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 10px;
    }

    .loading-subtext {
      font-size: 1em;
      color: var(--text-muted);
      font-style: italic;
    }

    /* Error State */
    .error-section {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 60vh;
    }

    .error-card {
      background: rgba(239, 68, 68, 0.1);
      border: 2px solid rgba(239, 68, 68, 0.4);
      padding: 40px;
      border-radius: 20px;
      text-align: center;
      max-width: 500px;
      backdrop-filter: blur(10px);
    }

    .error-icon {
      font-size: 3.5em;
      margin-bottom: 20px;
    }

    .error-title {
      font-size: 1.6em;
      font-weight: 700;
      text-transform: uppercase;
      color: #ff6b6b;
      margin-bottom: 16px;
    }

    .error-message {
      color: var(--text-secondary);
      margin-bottom: 24px;
    }

    .btn-retry {
      background: rgba(212, 175, 55, 0.2);
      border: 2px solid rgba(212, 175, 55, 0.5);
      color: var(--metallic-gold);
      padding: 12px 24px;
      font-weight: 600;
      text-transform: uppercase;
      cursor: pointer;
      border-radius: 10px;
      transition: all 0.3s ease;
    }

    .btn-retry:hover {
      background: rgba(212, 175, 55, 0.4);
      border-color: rgba(212, 175, 55, 0.8);
      transform: translateY(-2px);
    }

    /* Wrapped Cards */
    .wrapped-cards {
      position: relative;
      min-height: 85vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 40px 0;
    }

    .wrapped-card {
      position: absolute;
      width: 100%;
      max-width: 700px;
      min-height: 550px;
      border-radius: 30px;
      padding: 60px 50px;
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      transform: scale(0.85) translateY(60px) rotateY(10deg);
      transition: all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
      pointer-events: none;
      backdrop-filter: blur(30px);
      box-shadow: 0 25px 80px rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .wrapped-card.active {
      opacity: 1;
      transform: scale(1) translateY(0) rotateY(0deg);
      pointer-events: all;
      z-index: 10;
    }

    /* Card Color Themes - More Vibrant */
    .card-1 {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
    }

    .card-2 {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #f093fb 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
    }

    .card-3 {
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #4facfe 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
    }

    .card-4 {
      background: linear-gradient(135deg, #43e97b 0%, #38f9d7 50%, #43e97b 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
    }

    .card-5 {
      background: linear-gradient(135deg, #fa709a 0%, #fee140 50%, #fa709a 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
    }

    .card-6 {
      background: linear-gradient(135deg, #30cfd0 0%, #330867 50%, #30cfd0 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
    }

    .card-7 {
      background: linear-gradient(135deg, #a8edea 0%, #fed6e3 50%, #a8edea 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
      color: var(--bg-dark);
    }

    .card-8 {
      background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #ff9a9e 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
      color: var(--bg-dark);
    }

    .card-9 {
      background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 50%, #a1c4fd 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
      color: var(--bg-dark);
    }

    .card-10 {
      background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 50%, #ffecd2 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
      color: var(--bg-dark);
    }

    .card-5b {
      background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 50%, #ff6b6b 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
    }

    .card-5c {
      background: linear-gradient(135deg, #feca57 0%, #ff9ff3 50%, #feca57 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
    }

    .card-11 {
      background: linear-gradient(135deg, #48c6ef 0%, #6f86d6 50%, #48c6ef 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
    }

    .card-12 {
      background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #ff9a9e 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
      color: var(--bg-dark);
    }

    .card-13 {
      background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 50%, #a1c4fd 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
      color: var(--bg-dark);
    }

    .card-14 {
      background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 50%, #ffecd2 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
      color: var(--bg-dark);
    }

    .card-15 {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%);
      background-size: 200% 200%;
      animation: gradientShift 8s ease infinite;
    }

    @keyframes gradientShift {
      0%, 100% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
    }

    .card-content {
      text-align: center;
      width: 100%;
      position: relative;
      z-index: 2;
    }

    .card-emoji {
      font-size: 4em;
      margin-bottom: 20px;
      animation: bounce 2s ease-in-out infinite;
    }

    @keyframes bounce {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-10px); }
    }

    .card-number {
      font-size: 0.85em;
      font-weight: 600;
      opacity: 0.85;
      margin-bottom: 20px;
      text-transform: uppercase;
      letter-spacing: 0.15em;
    }

    .card-title {
      font-size: 3.2em;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 20px;
      line-height: 1.1;
      text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .card-subtitle {
      font-size: 1.4em;
      opacity: 0.95;
      margin-bottom: 30px;
      font-weight: 500;
    }

    .player-name {
      font-size: 1.6em;
      font-weight: 700;
      margin-top: 20px;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }

    .card-witty {
      font-size: 1em;
      font-style: italic;
      opacity: 0.8;
      margin-top: 20px;
    }

    .card-label {
      font-size: 1.3em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-bottom: 25px;
      opacity: 0.95;
    }

    .card-big-number {
      font-size: 7em;
      font-weight: 900;
      line-height: 1;
      margin: 25px 0;
      text-shadow: 0 5px 30px rgba(0, 0, 0, 0.4);
      letter-spacing: -0.02em;
    }

    .card-description {
      font-size: 1.4em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      opacity: 0.95;
      margin-bottom: 20px;
    }

    .card-champion {
      font-size: 4.5em;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin: 30px 0 15px;
      text-shadow: 0 5px 30px rgba(0, 0, 0, 0.4);
    }

    .card-champion-subtitle {
      font-size: 1.2em;
      font-style: italic;
      opacity: 0.9;
      margin-bottom: 30px;
    }

    /* Witty Jokes */
    .witty-joke {
      margin-top: 30px;
      padding: 20px;
      background: rgba(255, 255, 255, 0.15);
      border-radius: 15px;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .joke-text {
      font-size: 1.15em;
      font-style: italic;
      line-height: 1.6;
      margin: 0;
    }

    /* Top Champions */
    .top-champions {
      margin-top: 35px;
      text-align: left;
      max-width: 450px;
      margin-left: auto;
      margin-right: auto;
    }

    .champion-item {
      display: flex;
      align-items: center;
      gap: 18px;
      padding: 18px;
      margin: 10px 0;
      background: rgba(255, 255, 255, 0.12);
      border-radius: 15px;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      transition: transform 0.3s ease;
    }

    .champion-item:hover {
      transform: translateX(5px);
      background: rgba(255, 255, 255, 0.18);
    }

    .champion-rank {
      font-size: 1.3em;
      font-weight: 800;
      min-width: 45px;
    }

    .champion-name {
      flex: 1;
      font-size: 1.4em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .champion-games {
      font-size: 1.05em;
      opacity: 0.85;
      font-weight: 500;
    }

    /* Highlights */
    .highlights-list {
      margin-top: 30px;
      text-align: left;
      max-width: 550px;
      margin-left: auto;
      margin-right: auto;
    }

    .highlight-item {
      display: flex;
      align-items: flex-start;
      gap: 18px;
      padding: 22px;
      margin: 14px 0;
      background: rgba(255, 255, 255, 0.18);
      border-radius: 15px;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      transition: transform 0.3s ease;
    }

    .highlight-item:hover {
      transform: translateX(5px);
    }

    .highlight-icon {
      font-size: 1.8em;
      flex-shrink: 0;
    }

    .highlight-text {
      font-size: 1.15em;
      line-height: 1.7;
      flex: 1;
      font-weight: 500;
    }

    /* Strengths & Weaknesses */
    .strengths-list {
      margin-top: 25px;
      text-align: left;
      max-width: 550px;
      margin-left: auto;
      margin-right: auto;
    }

    .strength-item {
      display: flex;
      align-items: center;
      gap: 15px;
      padding: 18px;
      margin: 10px 0;
      background: rgba(255, 255, 255, 0.15);
      border-radius: 12px;
      backdrop-filter: blur(10px);
    }

    .strength-icon {
      font-size: 1.5em;
    }

    .strength-text {
      font-size: 1.1em;
      flex: 1;
      font-weight: 500;
    }

    .weaknesses-list {
      margin-top: 30px;
    }

    .weaknesses-label {
      font-size: 1em;
      font-style: italic;
      opacity: 0.8;
      margin-bottom: 15px;
    }

    .weakness-item {
      display: flex;
      align-items: center;
      gap: 15px;
      padding: 16px;
      margin: 8px 0;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      backdrop-filter: blur(10px);
    }

    .weakness-icon {
      font-size: 1.3em;
    }

    .weakness-text {
      font-size: 1.05em;
      flex: 1;
      font-weight: 400;
    }

    /* Fun Facts */
    .fun-facts {
      margin-top: 30px;
      text-align: left;
      max-width: 550px;
      margin-left: auto;
      margin-right: auto;
    }

    .fun-fact-item {
      display: flex;
      align-items: flex-start;
      gap: 20px;
      padding: 25px;
      margin: 15px 0;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 18px;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.25);
    }

    .fun-fact-icon {
      font-size: 2em;
      flex-shrink: 0;
    }

    .fun-fact-text {
      flex: 1;
      font-size: 1.2em;
      line-height: 1.6;
    }

    .fun-fact-text strong {
      display: block;
      font-size: 1.3em;
      margin-bottom: 8px;
    }

    .fun-fact-subtitle {
      display: block;
      font-size: 0.9em;
      opacity: 0.85;
      font-style: italic;
      margin-top: 5px;
    }

    /* Playstyle Analysis */
    .playstyle-analysis {
      margin-top: 30px;
    }

    .playstyle-item {
      display: flex;
      align-items: center;
      gap: 20px;
      padding: 25px;
      margin-bottom: 30px;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 18px;
      backdrop-filter: blur(10px);
    }

    .playstyle-icon {
      font-size: 2.5em;
      flex-shrink: 0;
    }

    .playstyle-text {
      flex: 1;
      font-size: 1.3em;
      line-height: 1.6;
    }

    .playstyle-text strong {
      display: block;
      font-size: 1.4em;
      margin-bottom: 8px;
    }

    .playstyle-subtitle {
      display: block;
      font-size: 0.95em;
      opacity: 0.9;
      font-style: italic;
      margin-top: 5px;
    }

    .playstyle-stats {
      margin-top: 20px;
    }

    .stat-item {
      margin: 20px 0;
    }

    .stat-label {
      display: block;
      font-size: 1.1em;
      font-weight: 600;
      margin-bottom: 10px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .stat-bar {
      width: 100%;
      height: 25px;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 8px;
      position: relative;
    }

    .stat-fill {
      height: 100%;
      background: linear-gradient(90deg, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0.6) 100%);
      border-radius: 12px;
      transition: width 1s ease;
      box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }

    .stat-value {
      font-size: 1.1em;
      font-weight: 700;
      opacity: 0.95;
    }

    /* Growth Areas */
    .growth-areas {
      margin-top: 30px;
      text-align: left;
      max-width: 550px;
      margin-left: auto;
      margin-right: auto;
    }

    .growth-item {
      display: flex;
      align-items: flex-start;
      gap: 18px;
      padding: 22px;
      margin: 14px 0;
      background: rgba(255, 255, 255, 0.18);
      border-radius: 15px;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .growth-icon {
      font-size: 1.8em;
      flex-shrink: 0;
    }

    .growth-text {
      font-size: 1.15em;
      line-height: 1.7;
      flex: 1;
      font-weight: 500;
    }

    /* Year Breakdown */
    .year-breakdown {
      margin-top: 30px;
      text-align: left;
      max-width: 550px;
      margin-left: auto;
      margin-right: auto;
    }

    .breakdown-item {
      display: flex;
      align-items: flex-start;
      gap: 20px;
      padding: 25px;
      margin: 15px 0;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 18px;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.25);
    }

    .breakdown-icon {
      font-size: 2em;
      flex-shrink: 0;
    }

    .breakdown-text {
      flex: 1;
      font-size: 1.2em;
      line-height: 1.6;
    }

    .breakdown-text strong {
      display: block;
      font-size: 1.3em;
      margin-bottom: 8px;
    }

    .breakdown-subtitle {
      display: block;
      font-size: 0.9em;
      opacity: 0.85;
      font-style: italic;
      margin-top: 5px;
    }

    /* Comparison Stats */
    .comparison-stats {
      margin-top: 30px;
      text-align: left;
      max-width: 550px;
      margin-left: auto;
      margin-right: auto;
    }

    .comparison-item {
      display: flex;
      align-items: flex-start;
      gap: 20px;
      padding: 25px;
      margin: 15px 0;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 18px;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.25);
    }

    .comparison-icon {
      font-size: 2em;
      flex-shrink: 0;
    }

    .comparison-text {
      flex: 1;
      font-size: 1.2em;
      line-height: 1.6;
    }

    .comparison-text strong {
      display: block;
      font-size: 1.3em;
      margin-bottom: 8px;
    }

    .comparison-subtitle {
      display: block;
      font-size: 0.9em;
      opacity: 0.85;
      font-style: italic;
      margin-top: 5px;
    }

    /* AI Summary */
    .card-ai-summary {
      font-size: 1.25em;
      line-height: 1.9;
      text-align: left;
      max-width: 580px;
      margin: 35px auto 0;
      padding: 35px;
      background: rgba(255, 255, 255, 0.18);
      border-radius: 20px;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      font-weight: 400;
    }

    .btn-share {
      background: rgba(255, 255, 255, 0.25);
      border: 2px solid rgba(255, 255, 255, 0.5);
      color: var(--bg-dark);
      padding: 18px 50px;
      font-size: 1.3em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      cursor: pointer;
      border-radius: 15px;
      transition: all 0.3s ease;
      margin-top: 30px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }

    .btn-share:hover {
      background: rgba(255, 255, 255, 0.35);
      transform: translateY(-3px);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    /* Navigation */
    .card-navigation {
      position: fixed;
      bottom: 50px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      align-items: center;
      gap: 25px;
      z-index: 100;
      background: rgba(5, 5, 8, 0.9);
      padding: 18px 28px;
      border-radius: 60px;
      backdrop-filter: blur(20px);
      border: 2px solid rgba(212, 175, 55, 0.4);
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    }

    .nav-btn {
      background: rgba(212, 175, 55, 0.25);
      border: 2px solid rgba(212, 175, 55, 0.5);
      color: var(--metallic-gold);
      width: 45px;
      height: 45px;
      border-radius: 50%;
      font-size: 1.6em;
      cursor: pointer;
      transition: all 0.3s ease;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .nav-btn:hover:not(:disabled) {
      background: rgba(212, 175, 55, 0.45);
      border-color: rgba(212, 175, 55, 0.9);
      transform: scale(1.15);
      box-shadow: 0 4px 15px rgba(212, 175, 55, 0.5);
    }

    .nav-btn:disabled {
      opacity: 0.25;
      cursor: not-allowed;
    }

    .card-dots {
      display: flex;
      gap: 10px;
      align-items: center;
    }

    .dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: rgba(212, 175, 55, 0.35);
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .dot.active {
      background: var(--metallic-gold);
      width: 35px;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(212, 175, 55, 0.6);
    }

    .dot:hover {
      background: rgba(212, 175, 55, 0.7);
      transform: scale(1.2);
    }

    @media (max-width: 768px) {
      .wrapped-card {
        padding: 40px 25px;
        min-height: 450px;
        max-width: 95%;
      }

      .card-big-number {
        font-size: 5em;
      }

      .card-title {
        font-size: 2.2em;
      }

      .card-champion {
        font-size: 3em;
      }

      .card-navigation {
        bottom: 25px;
        padding: 14px 20px;
        gap: 15px;
      }

      .nav-btn {
        width: 38px;
        height: 38px;
        font-size: 1.4em;
      }
    }
  `]
})
export class YearSummaryComponent implements OnInit, OnDestroy {
  summonerName = '';
  region = 'na1';
  loading = false;
  error = '';
  errorType: 'network' | 'not_found' | 'bad_request' | 'server_error' | 'rate_limit' | 'unknown' | null = null;
  summaryData: YearSummaryData | null = null;
  currentCard = 0;
  totalCards = 15;
  private autoAdvanceInterval: any;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    // Auto-advance cards every 6 seconds (longer for reading)
    this.autoAdvanceInterval = setInterval(() => {
      if (this.summaryData && this.currentCard < this.totalCards - 1) {
        this.nextCard();
      }
    }, 6000);
  }

  ngOnDestroy() {
    if (this.autoAdvanceInterval) {
      clearInterval(this.autoAdvanceInterval);
    }
  }

  async fetchYearSummary() {
    let summonerName = this.summonerName.trim().replace(/\s*#\s*/g, '#');
    
    if (!summonerName) {
      this.error = 'Please enter a summoner name in format: GameName#Tag';
      this.errorType = 'bad_request';
      return;
    }
    
    this.loading = true;
    this.error = '';
    this.errorType = null;
    this.summaryData = null;
    this.currentCard = 0;
    
    try {
      this.summaryData = await this.apiService.getYearSummary(summonerName, 2024, this.region);
      this.summonerName = summonerName;
    } catch (error: any) {
      this.handleError(error);
    } finally {
      this.loading = false;
    }
  }

  handleError(error: any) {
    console.error('Error:', error);
    
    if (error && typeof error === 'object') {
      this.error = error.message || 'An error occurred while fetching year summary';
      this.errorType = error.type || 'unknown';
    } else if (error && typeof error === 'string') {
      this.error = error;
      this.errorType = 'unknown';
    } else {
      this.error = 'An unexpected error occurred. Please try again.';
      this.errorType = 'unknown';
    }
  }

  getErrorTitle(): string {
    switch (this.errorType) {
      case 'network':
        return 'Connection Error';
      case 'not_found':
        return 'Summoner Not Found';
      case 'bad_request':
        return 'Invalid Request';
      case 'server_error':
        return 'Server Error';
      case 'rate_limit':
        return 'Rate Limit Exceeded';
      default:
        return 'Error';
    }
  }

  getTopChampions(): Array<{ champion: string; games: number }> {
    return this.summaryData?.summary?.most_played_champions || [];
  }

  // Witty Jokes Based on Stats
  getGamesJoke(): string {
    const games = this.summaryData?.summary?.total_games || 0;
    if (games === 0) return "You're a free agent! Time to get in the game! 🎮";
    if (games < 50) return "Casual gamer alert! 🎯 You've been taking it easy this year.";
    if (games < 200) return "Solid grind! 💪 You've been putting in the work!";
    if (games < 500) return "Dedication level: LEGENDARY! 🏆 That's a lot of games, summoner!";
    if (games < 1000) return "Are you sure you're not a pro player? 🤔 That's some serious commitment!";
    return "Wait... did you even sleep this year? 😴 You're a machine!";
  }

  getWinRateDescription(): string {
    const winRate = this.summaryData?.summary?.win_rate || 0;
    if (winRate >= 60) return "DOMINANT";
    if (winRate >= 55) return "STRONG";
    if (winRate >= 50) return "BALANCED";
    if (winRate >= 45) return "FIGHTING";
    return "GRINDING";
  }

  getWinRateJoke(): string {
    const winRate = this.summaryData?.summary?.win_rate || 0;
    if (winRate >= 60) return "You're basically Faker at this point! 🔥";
    if (winRate >= 55) return "You're carrying games like it's your job! 💼";
    if (winRate >= 50) return "Perfectly balanced, as all things should be! ⚖️";
    if (winRate >= 45) return "You're a fighter! Every game is a comeback story! 💪";
    return "The Rift is your training ground! Keep grinding! 🎯";
  }

  getChampionJoke(): string {
    const champ = this.summaryData?.summary?.best_champion || '';
    const topChamps = this.getTopChampions();
    if (topChamps.length > 0 && topChamps[0].games > 100) {
      return `You really love ${champ}, don't you? 😏`;
    }
    if (topChamps.length > 0 && topChamps[0].games > 50) {
      return `${champ} is clearly your comfort pick! 🎯`;
    }
    return `${champ} has been good to you this year! ✨`;
  }

  getFormattedKDA(): string {
    const kda = this.summaryData?.summary?.key_metrics?.avg_kda || 0;
    return kda.toFixed(2);
  }

  getKDADescription(): string {
    const kda = this.summaryData?.summary?.key_metrics?.avg_kda || 0;
    if (kda >= 3.0) return "ELITE";
    if (kda >= 2.5) return "STRONG";
    if (kda >= 2.0) return "SOLID";
    if (kda >= 1.5) return "STEADY";
    return "GROWING";
  }

  getKDAJoke(): string {
    const kda = this.summaryData?.summary?.key_metrics?.avg_kda || 0;
    if (kda >= 3.0) return "You're a KDA machine! Death is not in your vocabulary! 💀";
    if (kda >= 2.5) return "You know how to stay alive and get kills! 🎯";
    if (kda >= 2.0) return "Solid performance! You're holding your own! 👍";
    if (kda >= 1.5) return "You're learning! Every death is a lesson! 📚";
    return "You're improving! The Rift is your teacher! 🎓";
  }

  getHighlightEmoji(type: string): string {
    const emojiMap: { [key: string]: string } = {
      'Best Performance': '⭐',
      'Win Streak': '🔥',
      'Perfect Game': '💯',
      'Comeback': '📈',
      'Pentakill': '👑',
      'Ace': '🎯',
      'MVP': '🏆',
      'Clutch': '⚡',
    };
    return emojiMap[type] || '✨';
  }

  getEstimatedHours(): string {
    const games = this.summaryData?.summary?.total_games || 0;
    const avgGameTime = 30; // minutes
    const hours = Math.round((games * avgGameTime) / 60);
    return hours.toLocaleString();
  }

  getDaysEquivalent(): string {
    const games = this.summaryData?.summary?.total_games || 0;
    const avgGameTime = 30; // minutes
    const hours = (games * avgGameTime) / 60;
    const days = Math.round(hours / 24);
    return days.toLocaleString();
  }

  getImprovementText(): string {
    const improvement = this.summaryData?.summary?.improvement || 0;
    if (improvement > 0) {
      return `+${improvement.toFixed(1)}% improvement`;
    }
    return '';
  }

  getWinLossBreakdown(): string {
    const games = this.summaryData?.summary?.total_games || 0;
    const winRate = this.summaryData?.summary?.win_rate || 0;
    const wins = Math.round(games * (winRate / 100));
    const losses = games - wins;
    return `${wins} wins, ${losses} losses`;
  }

  getWinLossJoke(): string {
    const games = this.summaryData?.summary?.total_games || 0;
    const winRate = this.summaryData?.summary?.win_rate || 0;
    const wins = Math.round(games * (winRate / 100));
    const losses = games - wins;
    
    if (wins > losses * 1.5) return "You're winning more than you're losing! That's the way! 🎉";
    if (losses > wins * 1.5) return "Every loss is a lesson! You'll bounce back! 💪";
    return "You're keeping it balanced! That's respectable! ⚖️";
  }

  getFormattedDamage(): string {
    const damage = this.summaryData?.summary?.key_metrics?.avg_damage || 0;
    if (damage >= 1000000) return (damage / 1000000).toFixed(1) + 'M';
    if (damage >= 1000) return (damage / 1000).toFixed(1) + 'K';
    return Math.round(damage).toLocaleString();
  }

  getDamageJoke(): string {
    const damage = this.summaryData?.summary?.key_metrics?.avg_damage || 0;
    if (damage >= 30000) return "You're a damage dealer! The enemy team fears you! 💥";
    if (damage >= 20000) return "You're putting in work! Keep dealing that damage! 🔥";
    if (damage >= 15000) return "Solid damage output! You're contributing! ⚡";
    return "Every bit of damage counts! Keep improving! 📈";
  }

  getFormattedGold(): string {
    const gold = this.summaryData?.summary?.key_metrics?.avg_gold || 0;
    if (gold >= 1000000) return (gold / 1000000).toFixed(1) + 'M';
    if (gold >= 1000) return (gold / 1000).toFixed(1) + 'K';
    return Math.round(gold).toLocaleString();
  }

  getGoldJoke(): string {
    const gold = this.summaryData?.summary?.key_metrics?.avg_gold || 0;
    if (gold >= 15000) return "You're rich! The economy is your friend! 💰";
    if (gold >= 12000) return "Good gold income! You're farming well! 🌾";
    if (gold >= 10000) return "Decent gold! Keep working on that CS! 📊";
    return "Gold is power! Work on your farming! 💪";
  }

  getPlaystyleType(): string {
    const kda = this.summaryData?.summary?.key_metrics?.avg_kda || 0;
    const damage = this.summaryData?.summary?.key_metrics?.avg_damage || 0;
    if (kda >= 3.0 && damage >= 25000) return "AGGRESSIVE CARRY";
    if (kda >= 2.5 && damage >= 20000) return "BALANCED PLAYER";
    if (kda >= 2.0) return "SUPPORTIVE PLAYER";
    return "GROWING PLAYER";
  }

  getPlaystyleDescription(): string {
    const type = this.getPlaystyleType();
    if (type === "AGGRESSIVE CARRY") return "You're not afraid to take risks and carry games!";
    if (type === "BALANCED PLAYER") return "You know when to be aggressive and when to play safe!";
    if (type === "SUPPORTIVE PLAYER") return "You play for the team and make smart decisions!";
    return "You're learning and improving every game!";
  }

  getAggressionLevel(): number {
    const kda = this.summaryData?.summary?.key_metrics?.avg_kda || 0;
    const damage = this.summaryData?.summary?.key_metrics?.avg_damage || 0;
    const base = 50;
    const kdaBonus = Math.min((kda - 1.5) * 10, 30);
    const damageBonus = Math.min((damage - 10000) / 500, 20);
    return Math.max(0, Math.min(100, base + kdaBonus + damageBonus));
  }

  getConsistencyLevel(): number {
    const winRate = this.summaryData?.summary?.win_rate || 0;
    const games = this.summaryData?.summary?.total_games || 0;
    const base = 50;
    const winRateBonus = (winRate - 45) * 0.5;
    const gamesBonus = Math.min(games / 10, 20);
    return Math.max(0, Math.min(100, base + winRateBonus + gamesBonus));
  }

  getTeamPlayerLevel(): number {
    const kda = this.summaryData?.summary?.key_metrics?.avg_kda || 0;
    const winRate = this.summaryData?.summary?.win_rate || 0;
    const base = 50;
    const kdaBonus = Math.min((kda - 1.0) * 15, 30);
    const winRateBonus = (winRate - 45) * 0.4;
    return Math.max(0, Math.min(100, base + kdaBonus + winRateBonus));
  }

  getGrowthJoke(): string {
    const growthAreas = this.summaryData?.growth_areas || [];
    if (growthAreas.length === 0) return "You're perfect! Just kidding, there's always room to grow! 🌱";
    if (growthAreas.length <= 2) return "You're on the right track! Keep working on those areas! 📈";
    return "You've identified areas to improve! That's the first step to greatness! 🚀";
  }

  getGamesPerMonth(): string {
    const games = this.summaryData?.summary?.total_games || 0;
    const perMonth = Math.round(games / 12);
    return perMonth.toLocaleString();
  }

  getMonthlyJoke(): string {
    const games = this.summaryData?.summary?.total_games || 0;
    const perMonth = games / 12;
    if (perMonth >= 50) return "That's a lot of games per month! You're dedicated! 🔥";
    if (perMonth >= 30) return "You're playing regularly! Keep it up! 💪";
    if (perMonth >= 15) return "Nice consistency! You're staying active! ⚡";
    return "Quality over quantity! Every game counts! 🎯";
  }

  getBestMonth(): string {
    // This would ideally come from the API, but for now we'll use a placeholder
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 
                    'July', 'August', 'September', 'October', 'November', 'December'];
    const games = this.summaryData?.summary?.total_games || 0;
    // Simple calculation - could be improved with actual monthly data
    const monthIndex = Math.floor((games % 12));
    return months[monthIndex] || 'Unknown';
  }

  getBestMonthJoke(): string {
    return "You were on fire that month! 🔥";
  }

  getPeakPerformance(): string {
    const winRate = this.summaryData?.summary?.win_rate || 0;
    const kda = this.summaryData?.summary?.key_metrics?.avg_kda || 0;
    if (winRate >= 60 && kda >= 2.5) return "Peak Performance Achieved!";
    if (winRate >= 55 || kda >= 2.0) return "Strong Performance!";
    return "Steady Improvement!";
  }

  getPeakJoke(): string {
    return "You were at your best! Keep chasing that peak! 🏔️";
  }

  getGlobalRanking(): string {
    const games = this.summaryData?.summary?.total_games || 0;
    const winRate = this.summaryData?.summary?.win_rate || 0;
    // Simple calculation - would ideally come from API
    if (games >= 500 && winRate >= 55) return "Top 10%";
    if (games >= 300 && winRate >= 52) return "Top 25%";
    if (games >= 200) return "Top 50%";
    return "Top 75%";
  }

  getRankingJoke(): string {
    const ranking = this.getGlobalRanking();
    if (ranking.includes("10%")) return "You're in the elite tier! 🏆";
    if (ranking.includes("25%")) return "You're above average! Keep climbing! 📈";
    if (ranking.includes("50%")) return "You're in the middle of the pack! Keep grinding! 💪";
    return "You're building your foundation! Every game matters! 🌱";
  }

  getPercentile(): string {
    const games = this.summaryData?.summary?.total_games || 0;
    const winRate = this.summaryData?.summary?.win_rate || 0;
    // Simple calculation
    if (games >= 500 && winRate >= 55) return "90th";
    if (games >= 300 && winRate >= 52) return "75th";
    if (games >= 200) return "50th";
    return "25th";
  }

  getPercentileJoke(): string {
    const percentile = this.getPercentile();
    if (percentile.includes("90")) return "You're better than 90% of players! That's amazing! 🎉";
    if (percentile.includes("75")) return "You're in the top quarter! Keep pushing! 🔥";
    if (percentile.includes("50")) return "You're right in the middle! Room to grow! 📊";
    return "You're building your skills! Keep improving! 🚀";
  }

  getAchievementLevel(): string {
    const games = this.summaryData?.summary?.total_games || 0;
    const winRate = this.summaryData?.summary?.win_rate || 0;
    if (games >= 1000 && winRate >= 55) return "LEGENDARY";
    if (games >= 500 && winRate >= 52) return "ELITE";
    if (games >= 200) return "VETERAN";
    if (games >= 100) return "EXPERIENCED";
    return "RISING";
  }

  getAchievementJoke(): string {
    const level = this.getAchievementLevel();
    if (level === "LEGENDARY") return "You're a legend in the making! 🏆";
    if (level === "ELITE") return "You're elite! Keep dominating! 💎";
    if (level === "VETERAN") return "You're a veteran! Experience shows! 🎖️";
    if (level === "EXPERIENCED") return "You're getting experienced! Keep playing! 📚";
    return "You're on the rise! The sky's the limit! 🚀";
  }

  nextCard() {
    if (this.currentCard < this.totalCards - 1) {
      this.currentCard++;
    }
  }

  previousCard() {
    if (this.currentCard > 0) {
      this.currentCard--;
    }
  }

  goToCard(index: number) {
    if (index >= 0 && index < this.totalCards) {
      this.currentCard = index;
    }
  }

  shareWrapped() {
    if (navigator.share && this.summaryData) {
      const shareText = this.summaryData.shareable_content?.share_text || 
        `Check out my 2024 League of Legends Wrapped! 🎮 ${this.summaryData.summary.total_games} games played with ${(this.summaryData.summary.win_rate || 0).toFixed(1)}% win rate! 🏆`;
      
      navigator.share({
        title: 'My 2024 League Wrapped',
        text: shareText,
        url: window.location.href
      }).catch(err => console.log('Error sharing:', err));
    } else {
      const shareText = this.summaryData?.shareable_content?.share_text || 
        `Check out my 2024 League of Legends Wrapped! 🎮`;
      navigator.clipboard.writeText(shareText).then(() => {
        alert('Copied to clipboard! 📋');
      });
    }
  }
}
