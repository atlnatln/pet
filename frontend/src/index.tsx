import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import './stiller/global.css';
import App from './App';
import { store } from './magaza';
import { AuthProvider } from './baglamlar/AuthContext';
import { TemaBaglami } from './baglamlar/TemaBaglami';
import { BildirimProvider } from './baglamlar/BildirimBaglami';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <AuthProvider>
          <TemaBaglami>
            <BildirimProvider>
              <App />
            </BildirimProvider>
          </TemaBaglami>
        </AuthProvider>
      </BrowserRouter>
    </Provider>
  </React.StrictMode>
);
