export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  wsUrl: 'ws://localhost:8000/ws/chat',
  oauth: {
    clientId: 'your-client-id',
    authUrl: 'https://auth-server/oauth2/authorize',
    tokenUrl: 'https://auth-server/oauth2/token',
    redirectUri: 'http://localhost:4200/auth/callback',
    scope: 'openid profile email'
  },
  prometheus: {
    apiUrl: 'http://localhost:9090/api/v1'
  }
};