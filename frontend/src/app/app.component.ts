import { Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlayerInsightsComponent } from './player-insights/player-insights.component';
import { ZaahenComponent } from './zaahen/zaahen.component';
import { HeroVideoComponent } from './hero-video/hero-video.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, PlayerInsightsComponent, ZaahenComponent, HeroVideoComponent],
  template: `
    <nav class="navbar">
      <div class="navbar-logo">RIFT REWIND</div>
      <ul class="navbar-links">
        <li><a (click)="setActiveTab('insights'); $event.preventDefault()" [class.active]="activeTab === 'insights'" href="#insights">INSIGHTS</a></li>
        <li><a (click)="setActiveTab('year-summary'); $event.preventDefault()" [class.active]="activeTab === 'year-summary'" href="#year-summary">YEAR SUMMARY</a></li>
        <li><a (click)="setActiveTab('comparisons'); $event.preventDefault()" [class.active]="activeTab === 'comparisons'" href="#comparisons">COMPARISONS</a></li>
        <li><a (click)="setActiveTab('visualizations'); $event.preventDefault()" [class.active]="activeTab === 'visualizations'" href="#visualizations">VISUALIZATIONS</a></li>
        <li><a (click)="setActiveTab('zaahen'); $event.preventDefault()" [class.active]="activeTab === 'zaahen'" href="#zaahen">ZAAHEN</a></li>
      </ul>
      <div class="navbar-actions">
        <svg class="navbar-icon" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
        </svg>
        <svg class="navbar-icon" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM4.332 8.027a6.012 6.012 0 011.912-2.706C6.512 5.73 6.974 6 7.5 6A1.5 1.5 0 019 7.5V8a2 2 0 004 0 2 2 0 011.523-1.943A5.977 5.977 0 0116 10c0 .34-.028.675-.083 1H15a2 2 0 00-2 2v2.197A5.973 5.973 0 0110 16v-2a2 2 0 00-2-2 2 2 0 01-2-2 2 2 0 00-1.668-1.973z" clip-rule="evenodd"/>
        </svg>
      </div>
    </nav>
    
    <app-hero-video (navigateToInsights)="onNavigateToInsights()"></app-hero-video>
    
    <div class="tab-content" #tabContent>
      <app-player-insights *ngIf="activeTab === 'insights'"></app-player-insights>
      <app-zaahen *ngIf="activeTab === 'zaahen'"></app-zaahen>
      <div *ngIf="activeTab !== 'insights' && activeTab !== 'zaahen'" class="coming-soon">
        <h2>COMING SOON</h2>
        <p>This feature is under development.</p>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      min-height: 100vh;
    }
    
    .navbar-links a {
      cursor: pointer;
      transition: all 0.3s ease;
    }
    
    .navbar-links a.active {
      color: var(--metallic-gold);
      text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
    }
    
    .navbar-links a:hover {
      color: var(--metallic-silver);
    }
    
    .tab-content {
      min-height: calc(100vh - 200px);
      scroll-margin-top: 80px; /* Account for navbar + spacing */
    }
    
    .coming-soon {
      text-align: center;
      padding: 100px 20px;
      color: var(--text-secondary);
    }
    
    .coming-soon h2 {
      font-size: 2.5em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: var(--metallic-gold);
      margin-bottom: 20px;
    }
    
    .coming-soon p {
      font-size: 1.2em;
      color: var(--text-muted);
    }
  `]
})
export class AppComponent {
  @ViewChild('tabContent') tabContent!: any;
  
  title = 'Rift Rewind - Hall of Legends';
  activeTab = 'insights';
  
  setActiveTab(tab: string) {
    this.activeTab = tab;
  }
  
  onNavigateToInsights() {
    // Set active tab to insights
    this.activeTab = 'insights';
    
    // Wait for the DOM to update, then scroll to tab content
    setTimeout(() => {
      const heroSection = document.querySelector('app-hero-video');
      const tabContentElement = document.querySelector('.tab-content');
      const navbar = document.querySelector('.navbar');
      
      if (heroSection && tabContentElement) {
        const navbarHeight = navbar ? navbar.getBoundingClientRect().height : 60;
        
        // Get the hero container which has min-height: 350vh
        const heroContainer = heroSection.querySelector('.container-scroll');
        
        if (heroContainer) {
          // Get the bottom of the hero container in document coordinates
          const heroRect = heroContainer.getBoundingClientRect();
          const heroBottom = heroRect.bottom + window.pageYOffset;
          
          // Scroll to just past the hero container so tab content is visible
          // The hero container has min-height: 350vh, so scrolling past it reveals the content
          const scrollTarget = heroBottom - navbarHeight + 40; // Add some spacing
          
          window.scrollTo({ 
            top: Math.max(0, scrollTarget), 
            behavior: 'smooth' 
          });
        } else {
          // Fallback: scroll to tab content directly
          const tabRect = tabContentElement.getBoundingClientRect();
          const elementTop = tabRect.top + window.pageYOffset;
          const scrollTarget = elementTop - navbarHeight - 20;
          
          window.scrollTo({ 
            top: Math.max(0, scrollTarget), 
            behavior: 'smooth' 
          });
        }
      }
    }, 200);
  }
}

