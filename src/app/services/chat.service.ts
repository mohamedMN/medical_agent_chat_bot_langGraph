import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '../../environments/environment';
import { Message, ConversationHistory } from '../models/message.model';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private socket$: WebSocketSubject<any>;
  private messagesSubject = new BehaviorSubject<Message[]>([]);
  public messages$ = this.messagesSubject.asObservable();

  constructor(private http: HttpClient) {
    this.socket$ = webSocket(environment.wsUrl);
    this.socket$.subscribe(
      message => this.handleMessage(message),
      error => console.error('WebSocket error:', error)
    );
  }

  private handleMessage(message: any): void {
    const currentMessages = this.messagesSubject.value;
    this.messagesSubject.next([...currentMessages, message]);
  }

  sendMessage(content: string): Observable<Message> {
    const message: Partial<Message> = {
      content,
      sender: 'user',
      timestamp: new Date(),
      status: 'sending'
    };

    return this.http.post<Message>(`${environment.apiUrl}/chat/message`, message);
  }

  getConversationHistory(): Observable<ConversationHistory[]> {
    return this.http.get<ConversationHistory[]>(`${environment.apiUrl}/chat/history`);
  }
}