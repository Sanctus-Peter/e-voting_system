import './App.css'
import { CssBaseline, ThemeProvider } from '@mui/material'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
// import ProtectedRoute from './components/ProtectedRoute'
import defaultTheme from './themes/default'
import Home from './pages/Home'
import Signup from './pages/Signup'
import Signin from './pages/Signin'
import Dashboardlayout from './layout/Dashboardlayout'
import ProtectedRoute from './components/ProtectedRoute'
import UserHome from './pages/UserHome'
import NotImplemented from './pages/NotImplemented'

function App() {
  return (
    <ThemeProvider theme={defaultTheme}>
      <div className='app'>
        <Router>
          <Routes>
            <Route index element={<Home />} />
            <Route path='/signup' element={<Signup />} />
            <Route path='/signin' element={<Signin />} />
            <Route path='/dashboard' element={<Dashboardlayout />}>
              <Route index element={<UserHome />} />

              <Route path='*' element={<NotImplemented />} />
            </Route>
          </Routes>
        </Router>
        <CssBaseline />
      </div>
    </ThemeProvider>
  )
}

export default App

