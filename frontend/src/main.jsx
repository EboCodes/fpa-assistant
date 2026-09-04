// frontend/src/main.jsx
import { StrictMode, createElement } from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './App.css'
import './polish.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  createElement(StrictMode, null, createElement(App)),
)
