import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../api.service';

interface PlayerInsights {
  strengths: string[];
  weaknesses: string[];
  trends: string;
  unexpected_insights: string[];
  recommendations: string[];
  key_metrics: {
    avg_kda?: number;
    avg_damage?: number;
    avg_gold?: number;
    avg_vision_score?: number;
    avg_cs?: number;
  };
  rank_info?: {
    solo_queue?: {
      tier: string;
      rank: string;
      league_points: number;
      win_rate: number;
      wins: number;
      losses: number;
      hot_streak?: boolean;
    };
  };
  visualizations?: {
    phase_heatmap?: string;
    win_rate_trend?: string;
    champion_radar?: string;
    win_rate_chart?: string;
    kda_trend?: string;
    champion_performance?: string;
    role_performance?: string;
  };
}

interface YearSummary {
  year: number;
  summary: {
    total_games?: number;
    win_rate?: number;
    best_champion?: string;
  };
  highlights: Array<{ type: string; description: string }>;
  strengths: string[];
  weaknesses: string[];
  growth_areas: string[];
  ai_generated_summary: string;
}

@Component({
  selector: 'app-player-insights',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="content-section">
      <div class="input-card">
        <div class="form-group">
          <label for="summonerName">Riot ID (GameName#Tag)</label>
          <input 
            type="text" 
            id="summonerName" 
            [(ngModel)]="summonerName"
            placeholder="e.g., Faker#KR1 or YourName#NA1"
            (keyup.enter)="fetchInsights()"
          />
          <p class="help-text">Enter your Riot ID in format: GameName#TagLine</p>
        </div>
        
        <div class="form-group">
          <label for="region">Region</label>
          <select id="region" [(ngModel)]="region">
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
        
        <div class="form-group">
          <label for="actionType">Action</label>
          <select id="actionType" [(ngModel)]="actionType">
            <option value="insights">Get Player Insights</option>
            <option value="year-summary">Year-End Summary</option>
            <option value="social-content">Social Content</option>
          </select>
        </div>
        
        <div class="form-group" *ngIf="actionType === 'insights'">
          <label for="matchCount">Match Count (1-100)</label>
          <input 
            type="number" 
            id="matchCount" 
            [(ngModel)]="matchCount"
            min="1"
            max="100"
            placeholder="50"
          />
        </div>
        
        <button 
          class="btn-primary" 
          (click)="fetchInsights()"
          [disabled]="loading || !summonerName.trim()"
        >
          {{ loading ? 'Analyzing...' : 'Get Insights' }}
        </button>
      </div>
      
      <div *ngIf="loading" class="loading">
        <div class="spinner"></div>
        <p>Analyzing your matches... This may take a moment.</p>
      </div>
      
      <div *ngIf="error" class="error-container" [class.error-network]="errorType === 'network'" [class.error-not-found]="errorType === 'not_found'" [class.error-server]="errorType === 'server_error'">
        <div class="error-icon">
          <span *ngIf="errorType === 'network'">📡</span>
          <span *ngIf="errorType === 'not_found'">🔍</span>
          <span *ngIf="errorType === 'server_error'">⚠️</span>
          <span *ngIf="!errorType || errorType === 'unknown'">❌</span>
        </div>
        <div class="error-content">
          <h3 class="error-title">{{ getErrorTitle() }}</h3>
          <p class="error-message">{{ error }}</p>
          <div class="error-actions" *ngIf="errorType === 'network' || errorType === 'server_error'">
            <button class="btn-retry" (click)="retryFetch()" [disabled]="loading">
              {{ loading ? 'Retrying...' : 'Retry' }}
            </button>
          </div>
          <div class="error-help" *ngIf="errorType === 'not_found'">
            <p class="help-text">Tips:</p>
            <ul>
              <li>Make sure the summoner name format is correct: <strong>GameName#Tag</strong></li>
              <li>Check that you've selected the correct region</li>
              <li>The summoner must have played at least one match recently</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div *ngIf="results && !loading" class="results-section">
        <div class="tabs">
          <button 
            *ngFor="let tab of tabs"
            class="tab"
            [class.active]="activeTab === tab.id"
            (click)="activeTab = tab.id"
          >
            {{ tab.label }}
          </button>
        </div>
        
        <div *ngIf="activeTab === 'overview'" class="tab-content active">
          <div class="result-card">
            <h3>Key Metrics</h3>
            <div [innerHTML]="getMetricsHtml()"></div>
          </div>
          <div class="result-card">
            <h3>Trends</h3>
            <p>{{ getTrendsText() }}</p>
          </div>
        </div>
        
        <div *ngIf="activeTab === 'strengths'" class="tab-content active">
          <div class="result-card">
            <h3>Your Strengths</h3>
            <div *ngFor="let strength of getStrengths()" class="strength">
              {{ strength }}
            </div>
          </div>
        </div>
        
        <div *ngIf="activeTab === 'weaknesses'" class="tab-content active">
          <div class="result-card">
            <h3>Areas for Improvement</h3>
            <div *ngFor="let weakness of getWeaknesses()" class="weakness">
              {{ weakness }}
            </div>
          </div>
        </div>
        
        <div *ngIf="activeTab === 'insights'" class="tab-content active">
          <div class="result-card">
            <h3>Unexpected Insights</h3>
            <div *ngFor="let insight of getUnexpectedInsights()" class="insight-item">
              {{ insight }}
            </div>
          </div>
        </div>
        
        <div *ngIf="activeTab === 'recommendations'" class="tab-content active">
          <div class="result-card">
            <h3>Recommendations</h3>
            <div *ngFor="let rec of getRecommendations()" class="insight-item">
              {{ rec }}
            </div>
          </div>
        </div>
        
        <div *ngIf="activeTab === 'visualizations'" class="tab-content active">
          <div class="result-card" *ngIf="actionType === 'insights'">
            <h3>Performance Visualizations</h3>
            
            <div *ngIf="getVisualization('phase_heatmap')" class="chart-container">
              <h4>Performance by Game Phase</h4>
              <img [src]="'data:image/png;base64,' + getVisualization('phase_heatmap')" 
                   alt="Performance by Game Phase Heatmap" 
                   class="chart-image" />
            </div>
            
            <div *ngIf="getVisualization('win_rate_trend')" class="chart-container">
              <h4>Win Rate Trend Over Time</h4>
              <img [src]="'data:image/png;base64,' + getVisualization('win_rate_trend')" 
                   alt="Win Rate Trend" 
                   class="chart-image" />
            </div>
            
            <div *ngIf="getVisualization('champion_radar')" class="chart-container">
              <h4>Champion Performance Radar Chart</h4>
              <img [src]="'data:image/png;base64,' + getVisualization('champion_radar')" 
                   alt="Champion Performance Radar" 
                   class="chart-image" />
            </div>
            
            <div *ngIf="getVisualization('win_rate_chart')" class="chart-container">
              <h4>Win Rate Chart</h4>
              <img [src]="'data:image/png;base64,' + getVisualization('win_rate_chart')" 
                   alt="Win Rate Chart" 
                   class="chart-image" />
            </div>
            
            <div *ngIf="getVisualization('kda_trend')" class="chart-container">
              <h4>KDA Trend</h4>
              <img [src]="'data:image/png;base64,' + getVisualization('kda_trend')" 
                   alt="KDA Trend" 
                   class="chart-image" />
            </div>
            
            <div *ngIf="getVisualization('champion_performance')" class="chart-container">
              <h4>Champion Performance</h4>
              <img [src]="'data:image/png;base64,' + getVisualization('champion_performance')" 
                   alt="Champion Performance" 
                   class="chart-image" />
            </div>
            
            <div *ngIf="getVisualization('role_performance')" class="chart-container">
              <h4>Role Performance</h4>
              <img [src]="'data:image/png;base64,' + getVisualization('role_performance')" 
                   alt="Role Performance" 
                   class="chart-image" />
            </div>
            
            <div *ngIf="!hasAnyVisualizations()" class="no-charts">
              <p>No visualizations available. Please fetch insights first.</p>
            </div>
          </div>
          
          <div *ngIf="actionType !== 'insights'" class="result-card">
            <p>Visualizations are only available for player insights.</p>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
    }
    
    .chart-container {
      margin-bottom: 2rem;
      padding: 1.5rem;
      background: rgba(15, 15, 20, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      transition: all 0.3s ease;
    }
    
    .chart-container:hover {
      background: rgba(20, 20, 28, 0.8);
      border-color: rgba(212, 175, 55, 0.3);
    }
    
    .chart-container h4 {
      margin-bottom: 1rem;
      color: var(--metallic-gold, #d4af37);
      font-size: 1.2em;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    
    .chart-image {
      width: 100%;
      max-width: 100%;
      height: auto;
      border-radius: 4px;
      display: block;
      margin: 0 auto;
    }
    
    .no-charts {
      text-align: center;
      padding: 3rem 2rem;
      color: var(--text-muted, rgba(255, 255, 255, 0.5));
    }
    
    .no-charts p {
      font-size: 1.1em;
    }
  `]
})
export class PlayerInsightsComponent {
  summonerName = '';
  region = 'na1';
  actionType = 'insights';
  matchCount = 50;
  loading = false;
  error = '';
  errorType: 'network' | 'not_found' | 'bad_request' | 'server_error' | 'rate_limit' | 'unknown' | null = null;
  results: PlayerInsights | YearSummary | null = null;
  activeTab = 'overview';
  retryCount = 0;
  maxRetries = 2;
  
  tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'strengths', label: 'Strengths' },
    { id: 'weaknesses', label: 'Weaknesses' },
    { id: 'insights', label: 'Unexpected Insights' },
    { id: 'recommendations', label: 'Recommendations' },
    { id: 'visualizations', label: 'Visualizations' }
  ];
  
  constructor(private apiService: ApiService) {}
  
  async fetchInsights() {
    // Normalize summoner name: trim and remove spaces around #
    let summonerName = this.summonerName.trim().replace(/\s*#\s*/g, '#');
    
    if (!summonerName) {
      this.error = 'Please enter a summoner name in format: GameName#Tag';
      return;
    }
    
    // Validate match count
    if (this.matchCount < 1 || this.matchCount > 100) {
      this.error = 'Match count must be between 1 and 100';
      return;
    }
    
    // Reset retry count if this is a new fetch (not a retry)
    // If there's no error, it means this is a new fetch from user action
    if (!this.error) {
      this.retryCount = 0;
    }
    
    this.loading = true;
    this.error = '';
    this.errorType = null;
    this.results = null;
    
    try {
      if (this.actionType === 'insights') {
        this.results = await this.apiService.getPlayerInsights(summonerName, this.region, this.matchCount);
      } else if (this.actionType === 'year-summary') {
        this.results = await this.apiService.getYearSummary(summonerName, 2024, this.region);
      } else if (this.actionType === 'social-content') {
        this.results = await this.apiService.getSocialContent(summonerName, this.region);
      }
      this.activeTab = 'overview';
      this.error = '';
      this.errorType = null;
      this.retryCount = 0; // Reset retry count on success
    } catch (error: any) {
      this.handleError(error);
    } finally {
      this.loading = false;
    }
  }
  
  handleError(error: any) {
    console.error('Error:', error);
    
    // Extract error message and type from the error object
    if (error && typeof error === 'object') {
      this.error = error.message || 'An error occurred while fetching insights';
      this.errorType = error.type || 'unknown';
    } else if (error && typeof error === 'string') {
      this.error = error;
      this.errorType = 'unknown';
    } else {
      this.error = 'An unexpected error occurred. Please try again.';
      this.errorType = 'unknown';
    }
  }
  
  retryFetch() {
    if (this.retryCount < this.maxRetries) {
      this.error = '';
      this.errorType = null;
      this.retryCount++;
      this.fetchInsights();
    } else {
      this.error = 'Maximum retry attempts reached. Please check your connection and try again later.';
      this.errorType = 'network';
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
  
  getMetricsHtml(): string {
    if (!this.results) return '';
    
    if (this.actionType === 'insights') {
      const data = this.results as PlayerInsights;
      let html = '';
      
      if (data.rank_info) {
        html += this.formatRankInfo(data.rank_info);
        html += '<hr style="margin: 15px 0; border-color: rgba(255,255,255,0.1);">';
      }
      
      if (data.key_metrics) {
        html += '<div class="metric-grid">';
        const metrics = [
          { label: 'Average KDA', value: data.key_metrics.avg_kda?.toFixed(2) || 'N/A' },
          { label: 'Average Damage', value: data.key_metrics.avg_damage?.toLocaleString() || 'N/A' },
          { label: 'Average Gold', value: data.key_metrics.avg_gold?.toLocaleString() || 'N/A' },
          { label: 'Vision Score', value: data.key_metrics.avg_vision_score?.toFixed(1) || 'N/A' },
          { label: 'Average CS', value: data.key_metrics.avg_cs?.toFixed(1) || 'N/A' }
        ];
        metrics.forEach(metric => {
          html += `
            <div class="metric-item">
              <div class="metric-label">${metric.label}</div>
              <div class="metric-value">${metric.value}</div>
            </div>
          `;
        });
        html += '</div>';
      }
      
      return html;
    } else if (this.actionType === 'year-summary') {
      const data = this.results as YearSummary;
      if (data.summary) {
        let html = '<div class="metric-grid">';
        const metrics = [
          { label: 'Total Games', value: data.summary.total_games || 0 },
          { label: 'Win Rate', value: data.summary.win_rate ? data.summary.win_rate.toFixed(1) + '%' : '0%' },
          { label: 'Most Played', value: data.summary.best_champion || 'N/A' }
        ];
        metrics.forEach(metric => {
          html += `
            <div class="metric-item">
              <div class="metric-label">${metric.label}</div>
              <div class="metric-value">${metric.value}</div>
            </div>
          `;
        });
        html += '</div>';
        return html;
      }
    }
    
    return '<p style="color: rgba(255,255,255,0.5);">No metrics available</p>';
  }
  
  formatRankInfo(rankInfo: any): string {
    if (!rankInfo.solo_queue) {
      return '<div class="rank-badge"><p>Unranked</p></div>';
    }
    
    const sq = rankInfo.solo_queue;
    let html = '<div class="rank-badge">';
    html += `<h4>🏆 ${sq.tier} ${sq.rank}</h4>`;
    html += `<p><strong>${sq.league_points} LP</strong> • Win Rate: ${sq.win_rate.toFixed(1)}% (${sq.wins}W / ${sq.losses}L)</p>`;
    if (sq.hot_streak) {
      html += '<p style="color: #f4d03f; margin-top: 8px;">🔥 Hot Streak Active!</p>';
    }
    html += '</div>';
    return html;
  }
  
  getTrendsText(): string {
    if (!this.results) return 'No trend data available';
    
    if (this.actionType === 'insights') {
      return (this.results as PlayerInsights).trends || 'No trend data available';
    } else if (this.actionType === 'year-summary') {
      return (this.results as YearSummary).ai_generated_summary || 'No summary available';
    } else if (this.actionType === 'social-content') {
      return (this.results as any).share_text || 'No content available';
    }
    
    return 'No data available';
  }
  
  getStrengths(): string[] {
    if (!this.results) return [];
    
    if (this.actionType === 'insights') {
      return (this.results as PlayerInsights).strengths || [];
    } else if (this.actionType === 'year-summary') {
      return (this.results as YearSummary).strengths || [];
    }
    
    return [];
  }
  
  getWeaknesses(): string[] {
    if (!this.results) return [];
    
    if (this.actionType === 'insights') {
      return (this.results as PlayerInsights).weaknesses || [];
    } else if (this.actionType === 'year-summary') {
      return (this.results as YearSummary).weaknesses || [];
    }
    
    return [];
  }
  
  getUnexpectedInsights(): string[] {
    if (!this.results) return [];
    
    if (this.actionType === 'insights') {
      return (this.results as PlayerInsights).unexpected_insights || [];
    } else if (this.actionType === 'year-summary') {
      return (this.results as YearSummary).highlights?.map(h => `${h.type}: ${h.description}`) || [];
    }
    
    return [];
  }
  
  getRecommendations(): string[] {
    if (!this.results) return [];
    
    if (this.actionType === 'insights') {
      return (this.results as PlayerInsights).recommendations || [];
    } else if (this.actionType === 'year-summary') {
      return (this.results as YearSummary).growth_areas || [];
    }
    
    return [];
  }
  
  getVisualization(key: string): string | null {
    if (!this.results || this.actionType !== 'insights') {
      return null;
    }
    
    const insights = this.results as PlayerInsights;
    return insights.visualizations?.[key as keyof typeof insights.visualizations] || null;
  }
  
  hasAnyVisualizations(): boolean {
    if (!this.results || this.actionType !== 'insights') {
      return false;
    }
    
    const insights = this.results as PlayerInsights;
    const viz = insights.visualizations;
    if (!viz) {
      return false;
    }
    
    return !!(viz.phase_heatmap || viz.win_rate_trend || viz.champion_radar || 
              viz.win_rate_chart || viz.kda_trend || viz.champion_performance || 
              viz.role_performance);
  }
}

