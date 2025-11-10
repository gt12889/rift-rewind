import { Component, ElementRef, OnInit, OnDestroy, ViewChild, AfterViewInit, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { trigger, state, style, transition, animate } from '@angular/animations';

@Component({
  selector: 'app-hero-video',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="container-scroll" #containerScroll>
      <div class="container-sticky" [style.background-image]="'url(' + hallBackgroundSrc + ')'">
        <div 
          class="container-animated"
          [@fadeIn]="isVisible"
          [style.transform]="'translateY(' + animatedY + 'px)'"
        >
          <h1 class="hero-title">
            RIFT<br>
            REWIND
          </h1>
          <p class="hero-description">
            Rewind your journey through the Rift. Analyze your matches, 
            uncover your strengths, and forge your path to greatness.
          </p>
        </div>

        <div 
          class="container-inset"
          [style.clip-path]="clipPath"
        >
          <img
            #heroImage
            class="hero-image"
            [src]="imageSrc"
            [alt]="'Garen - The Might of Demacia'"
            [style.transform]="'scale(' + imageScale + ')'"
            (error)="onImageError()"
          />
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
      padding: 60px 20px;
      overflow: hidden;
      background-size: cover;
      background-position: center center;
      background-repeat: no-repeat;
      background-attachment: fixed;
    }

    .container-sticky::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(
        180deg,
        rgba(10, 10, 20, 0.4) 0%,
        rgba(15, 15, 30, 0.3) 50%,
        rgba(10, 10, 20, 0.5) 100%
      );
      z-index: 1;
      pointer-events: none;
    }

    .container-animated {
      text-align: center;
      margin-bottom: 40px;
      z-index: 10;
      position: relative;
    }

    .hero-title {
      font-size: 3.5em;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: #ffffff;
      text-shadow: 
        0 2px 10px rgba(0, 0, 0, 0.8),
        0 4px 20px rgba(0, 0, 0, 0.6),
        0 0 30px rgba(255, 255, 255, 0.3),
        0 0 60px rgba(192, 192, 255, 0.2);
      margin-bottom: 20px;
      line-height: 1.2;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .hero-description {
      font-size: 1.25em;
      color: rgba(248, 248, 255, 0.96);
      max-width: 54ch;
      margin: 0 auto;
      line-height: 1.95;
      opacity: 1;
      text-shadow: 
        0 2px 14px rgba(0, 0, 0, 0.85),
        0 4px 28px rgba(0, 0, 0, 0.65),
        0 1px 3px rgba(212, 175, 55, 0.2),
        0 0 20px rgba(212, 175, 55, 0.1),
        0 0 40px rgba(212, 175, 55, 0.05);
      font-weight: 350;
      font-family: 'Cormorant Garamond', 'Georgia', 'Palatino', 'Times New Roman', serif;
      letter-spacing: 0.04em;
      font-style: normal;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    .hero-description::first-letter {
      color: rgba(212, 175, 55, 0.95);
      font-size: 1.5em;
      font-weight: 600;
      float: left;
      line-height: 0.8;
      margin-right: 6px;
      margin-top: 4px;
      text-shadow: 
        0 0 14px rgba(212, 175, 55, 0.6),
        0 0 28px rgba(212, 175, 55, 0.3),
        0 2px 6px rgba(0, 0, 0, 0.6);
      font-family: 'Cormorant Garamond', serif;
    }

    .container-inset {
      position: relative;
      pointer-events: none;
      overflow: hidden;
      max-height: 450px;
      width: auto;
      padding: 24px 0;
      margin: 20px 0;
      z-index: 5;
    }

    .hero-image {
      position: relative;
      z-index: 5;
      height: auto;
      max-height: 600px;
      max-width: 100%;
      width: auto;
      object-fit: contain;
      border-radius: 8px;
      box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.6),
        0 0 40px rgba(255, 255, 255, 0.1);
      filter: brightness(1.1) contrast(1.05);
    }

    .container-animated-button {
      margin-top: 20px;
      z-index: 10;
      position: relative;
    }

    .hero-button {
      background: rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(10px);
      border: 2px solid rgba(255, 255, 255, 0.4);
      color: #ffffff;
      padding: 14px 32px;
      font-size: 1em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      cursor: pointer;
      transition: all 0.3s ease;
      border-radius: 8px;
      box-shadow: 
        0 4px 12px rgba(0, 0, 0, 0.4),
        0 0 20px rgba(255, 255, 255, 0.1);
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }

    .hero-button:hover {
      background: rgba(255, 255, 255, 0.25);
      border-color: rgba(255, 255, 255, 0.6);
      box-shadow: 
        0 6px 20px rgba(0, 0, 0, 0.5),
        0 0 30px rgba(255, 255, 255, 0.2);
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
  @ViewChild('heroImage', { static: false }) heroImage!: ElementRef<HTMLImageElement>;
  @Output() navigateToInsights = new EventEmitter<void>();

  // Hall background image - majestic futuristic/fantasy architecture
  // The image should be in frontend/src/assets/ and will be copied to assets/ during build
  hallBackgroundSrc = 'assets/hall-background.jpg';
  
  // Garen - The Might of Demacia hero image
  // Using Skin_Splash_Classic_Garen.webp from assets folder
  imageSrc = 'assets/Skin_Splash_Classic_Garen.webp';
  
  // Fallback if image fails to load
  onImageError() {
    console.warn('Hero image failed to load. Please check:');
    console.warn('1. Image file exists at: frontend/src/assets/Skin_Splash_Classic_Garen.webp');
    console.warn('2. Filename matches imageSrc in component (currently: ' + this.imageSrc + ')');
    console.warn('3. File format is supported (.jpg, .jpeg, .png, .webp)');
    // Hide the image container on error
    const imageContainer = document.querySelector('.container-inset');
    if (imageContainer) {
      (imageContainer as HTMLElement).style.display = 'none';
    }
  }
  
  isVisible = false;
  animatedY = 80;
  buttonY = -120;
  imageScale = 0.7;
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
      
      // Animate image scale (0.7 to 1)
      this.imageScale = 0.7 + (scrollProgress * 0.3);
      
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

