import { Component, ElementRef, OnInit, OnDestroy, ViewChild, AfterViewInit, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { trigger, state, style, transition, animate } from '@angular/animations';

@Component({
  selector: 'app-hero-video',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="container-scroll" #containerScroll>
      <div class="container-sticky" [style.background]="backgroundGradient">
        <div 
          class="container-animated"
          [@fadeIn]="isVisible"
          [style.transform]="'translateY(' + animatedY + 'px)'"
        >
          <h1 class="hero-title">
            HALL<br>
            <span class="title-small">of</span><br>
            LEGENDS
          </h1>
          <p class="hero-description">
            Enter the Hall of Legends and discover your legacy. Analyze your matches, 
            uncover your strengths, and forge your path to greatness in the Rift.
          </p>
        </div>

        <div 
          class="container-inset"
          [style.clip-path]="clipPath"
        >
          <video
            #heroVideo
            class="hero-video"
            [style.transform]="'scale(' + videoScale + ')'"
            autoplay
            muted
            loop
            playsinline
          >
            <source [src]="videoSrc" type="video/mp4">
            Your browser does not support the video tag.
          </video>
        </div>

        <div 
          class="container-animated-button"
          [@fadeIn]="isVisible"
          [style.transform]="'translateY(' + buttonY + 'px)'"
        >
          <button 
            class="hero-button"
            (click)="scrollToInsights()"
            [@buttonHover]="buttonHoverState"
            (mouseenter)="buttonHoverState = 'hover'"
            (mouseleave)="buttonHoverState = 'idle'"
          >
            GET STARTED
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .container-scroll {
      position: relative;
      min-height: 350vh;
      width: 100%;
    }

    .container-sticky {
      position: sticky;
      left: 0;
      top: 0;
      min-height: 100vh;
      width: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 40px 20px;
      overflow: hidden;
    }

    .container-animated {
      text-align: center;
      margin-bottom: 40px;
      z-index: 10;
    }

    .hero-title {
      font-size: 3.5em;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: var(--metallic-gold);
      text-shadow: 
        0 0 10px rgba(212, 175, 55, 0.5),
        0 0 20px rgba(212, 175, 55, 0.3),
        0 0 30px rgba(212, 175, 55, 0.2);
      margin-bottom: 20px;
      line-height: 1.2;
    }

    .title-small {
      font-size: 0.6em;
      font-weight: 400;
      letter-spacing: 0.3em;
      color: rgba(100, 100, 120, 0.9);
    }

    .hero-description {
      font-size: 1.2em;
      color: rgba(80, 80, 100, 0.9);
      max-width: 42ch;
      margin: 0 auto;
      line-height: 1.6;
      opacity: 0.85;
    }

    .container-inset {
      position: relative;
      pointer-events: none;
      overflow: hidden;
      max-height: 450px;
      width: auto;
      padding: 24px 0;
      margin: 20px 0;
    }

    .hero-video {
      position: relative;
      z-index: 10;
      height: auto;
      max-height: 100%;
      max-width: 100%;
      border-radius: 16px;
      box-shadow: 0 0 40px rgba(212, 175, 55, 0.4), 0 0 60px rgba(59, 130, 246, 0.2);
    }

    .container-animated-button {
      margin-top: 20px;
      z-index: 10;
    }

    .hero-button {
      background: rgba(5, 5, 8, 0.2);
      border: 2px solid rgba(212, 175, 55, 0.5);
      color: var(--metallic-gold);
      padding: 14px 32px;
      font-size: 1em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      cursor: pointer;
      transition: all 0.3s ease;
      border-radius: 0;
      box-shadow: 0 4px 24px rgba(212, 175, 55, 0.3);
    }

    .hero-button:hover {
      background: rgba(5, 5, 8, 0.5);
      border-color: rgba(212, 175, 55, 0.8);
      box-shadow: 0 4px 30px rgba(212, 175, 55, 0.5);
      transform: translateY(-2px);
    }

    .hero-button:active {
      transform: translateY(0);
    }

    @media (max-width: 768px) {
      .hero-title {
        font-size: 2.5em;
      }

      .hero-description {
        font-size: 1em;
      }

      .container-inset {
        max-height: 300px;
      }
    }
  `],
  animations: [
    trigger('fadeIn', [
      state('hidden', style({
        filter: 'blur(10px)',
        opacity: 0
      })),
      state('visible', style({
        filter: 'blur(0px)',
        opacity: 1
      })),
      transition('hidden => visible', [
        animate('0.6s cubic-bezier(0.4, 0, 0.2, 1)')
      ])
    ]),
    trigger('buttonHover', [
      state('idle', style({
        transform: 'scale(1)'
      })),
      state('hover', style({
        transform: 'scale(1.015)'
      })),
      transition('idle <=> hover', [
        animate('0.2s ease')
      ])
    ])
  ]
})
export class HeroVideoComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChild('containerScroll', { static: false }) containerScroll!: ElementRef;
  @ViewChild('heroVideo', { static: false }) heroVideo!: ElementRef<HTMLVideoElement>;
  @Output() navigateToInsights = new EventEmitter<void>();

  videoSrc = 'https://videos.pexels.com/video-files/8566672/8566672-uhd_2560_1440_30fps.mp4';
  // Majestic hall theme: whites, silvers, light grays with blue and gold accents
  backgroundGradient = 'radial-gradient(40% 40% at 50% 20%, rgba(255, 255, 255, 0.95) 0%, rgba(240, 240, 245, 0.9) 15%, rgba(220, 220, 230, 0.85) 30%, rgba(200, 200, 210, 0.8) 50%, rgba(180, 180, 190, 0.75) 70%, rgba(160, 160, 170, 0.7) 88.54%), linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(212, 175, 55, 0.1) 50%, rgba(59, 130, 246, 0.15) 100%)';
  
  isVisible = false;
  animatedY = 80;
  buttonY = -120;
  videoScale = 0.7;
  clipPath = 'inset(45% 45% 45% 45% round 1000px)';
  buttonHoverState = 'idle';

  private scrollListener?: () => void;

  ngOnInit() {
    // Initial visibility check
    setTimeout(() => {
      this.isVisible = true;
    }, 100);
  }

  ngAfterViewInit() {
    this.setupScrollAnimation();
  }

  ngOnDestroy() {
    if (this.scrollListener) {
      window.removeEventListener('scroll', this.scrollListener);
    }
  }

  private setupScrollAnimation() {
    this.scrollListener = () => {
      if (!this.containerScroll?.nativeElement) return;

      const container = this.containerScroll.nativeElement;
      const rect = container.getBoundingClientRect();
      const windowHeight = window.innerHeight;
      
      // Calculate scroll progress (0 to 1)
      // Start when container enters center of viewport, end when it exits
      const startOffset = windowHeight * 0.5; // center
      const endOffset = -windowHeight * 0.5; // bottom
      
      let scrollProgress = 0;
      
      if (rect.top <= startOffset && rect.bottom >= endOffset) {
        // Container is in view
        const scrollRange = startOffset - endOffset;
        const scrolled = startOffset - rect.top;
        scrollProgress = Math.max(0, Math.min(1, scrolled / scrollRange));
      } else if (rect.top > startOffset) {
        // Before start
        scrollProgress = 0;
      } else {
        // After end
        scrollProgress = 1;
      }

      // Animate Y position (80px to 0)
      this.animatedY = 80 - (scrollProgress * 80);
      
      // Animate button Y position (-120px to 0)
      this.buttonY = -120 + (scrollProgress * 120);
      
      // Animate video scale (0.7 to 1)
      this.videoScale = 0.7 + (scrollProgress * 0.3);
      
      // Animate clip path inset (45% to 0%)
      const inset = 45 - (scrollProgress * 45);
      const roundedness = 1000 - (scrollProgress * 984); // 1000px to 16px
      this.clipPath = `inset(${inset}% ${inset}% ${inset}% ${inset}% round ${roundedness}px)`;
    };

    window.addEventListener('scroll', this.scrollListener, { passive: true });
    // Initial call
    this.scrollListener();
  }

  scrollToInsights() {
    // Emit event to parent component to handle navigation
    this.navigateToInsights.emit();
  }
}

