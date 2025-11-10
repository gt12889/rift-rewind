import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiBase = window.location.origin;
  
  constructor(private http: HttpClient) {}
  
  getPlayerInsights(summonerName: string, region: string, matchCount: number = 50): Promise<any> {
    const url = `${this.apiBase}/api/player/${encodeURIComponent(summonerName)}/insights?region=${region}&match_count=${matchCount}`;
    return this.http.get(url).pipe(
      catchError(this.handleError)
    ).toPromise();
  }
  
  getYearSummary(summonerName: string, year: number, region: string): Promise<any> {
    const url = `${this.apiBase}/api/player/${encodeURIComponent(summonerName)}/year-summary?year=${year}&region=${region}`;
    return this.http.get(url).pipe(
      catchError(this.handleError)
    ).toPromise();
  }
  
  getSocialContent(summonerName: string, region: string): Promise<any> {
    const url = `${this.apiBase}/api/player/${encodeURIComponent(summonerName)}/social-content?content_type=year-end&region=${region}`;
    return this.http.get(url).pipe(
      catchError(this.handleError)
    ).toPromise();
  }
  
  chatWithAgent(message: string, context: string | null = null, conversationHistory: any[] = []): Promise<any> {
    const url = `${this.apiBase}/api/agent/chat`;
    console.log('[ApiService] chatWithAgent called');
    console.log('[ApiService] URL:', url);
    console.log('[ApiService] Message:', message);
    console.log('[ApiService] Context:', context);
    console.log('[ApiService] Conversation history length:', conversationHistory.length);
    
    const body = {
      message: message,
      context: context,
      conversation_history: conversationHistory.map(msg => ({
        role: msg.role,
        content: msg.content
      }))
    };
    
    console.log('[ApiService] Request body:', JSON.stringify(body, null, 2));
    
    try {
      return this.http.post(url, body).pipe(
        catchError((error) => {
          console.error('[ApiService] Error in chatWithAgent:', error);
          console.error('[ApiService] Error status:', error.status);
          console.error('[ApiService] Error message:', error.message);
          console.error('[ApiService] Error details:', error.error);
          return this.handleError(error);
        })
      ).toPromise() as Promise<any>;
    } catch (error) {
      console.error('[ApiService] Exception in chatWithAgent:', error);
      throw error;
    }
  }
  
  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An unknown error occurred';
    let errorType = 'unknown';
    
    if (error.error instanceof ErrorEvent) {
      // Client-side error (network, etc.)
      errorType = 'network';
      errorMessage = 'Unable to connect to the server. Please check your internet connection and try again.';
    } else {
      // Server-side error
      const status = error.status;
      
      if (status === 0) {
        // Network error or CORS issue
        errorType = 'network';
        errorMessage = 'Unable to connect to the server. The server may be down or unreachable.';
      } else if (status === 404) {
        errorType = 'not_found';
        if (error.error?.detail) {
          errorMessage = error.error.detail;
        } else {
          errorMessage = 'Summoner not found. Please check the summoner name and region, and make sure the format is correct (GameName#Tag).';
        }
      } else if (status === 400) {
        errorType = 'bad_request';
        errorMessage = error.error?.detail || 'Invalid request. Please check your input and try again.';
      } else if (status === 401 || status === 403) {
        errorType = 'unauthorized';
        errorMessage = 'Authentication failed. Please check your API credentials.';
      } else if (status === 429) {
        errorType = 'rate_limit';
        errorMessage = 'Too many requests. Please wait a moment and try again.';
      } else if (status >= 500) {
        errorType = 'server_error';
        errorMessage = error.error?.detail || 'Server error occurred. Please try again later.';
      } else {
        // Other errors
        errorMessage = error.error?.detail || `An error occurred (${status}). Please try again.`;
      }
    }
    
    return throwError(() => ({ 
      message: errorMessage, 
      type: errorType,
      status: error.status,
      originalError: error
    }));
  }
}

