export interface Message {
  id: string;
  content: string;
  timestamp: Date;
  sender: 'user' | 'bot';
  status: 'sending' | 'sent' | 'error';
}

export interface ConversationHistory {
  id: string;
  messages: Message[];
  startTime: Date;
  endTime?: Date;
  metadata?: Record<string, any>;
}