import './App.css'
import { CssBaseline, ThemeProvider } from '@mui/material'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
// import ProtectedRoute from './components/ProtectedRoute'
import defaultTheme from './themes/default'
import Home from './pages/Home'

function App() {
  return (
    <ThemeProvider theme={defaultTheme}>
      <div className='app'>
        <Router>
          <Routes>
            <Route index element={<Home />} />
          </Routes>
        </Router>
        <CssBaseline />
      </div>
    </ThemeProvider>
  )
}

export default App

