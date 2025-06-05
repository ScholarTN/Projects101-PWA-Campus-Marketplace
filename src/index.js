import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import * as serviceWorker from './registerServiceWorker';
import { AuthProvider } from './context/AuthContext';
import { MessageProvider } from './context/MessageContext';
import './styles/main.css';

ReactDOM.render(
  <React.StrictMode>
    <AuthProvider>
      <MessageProvider>
        <App />
      </MessageProvider>
    </AuthProvider>
  </React.StrictMode>,
  document.getElementById('root')
);

serviceWorker.register();