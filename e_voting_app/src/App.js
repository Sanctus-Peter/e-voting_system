import './App.css'
import { CssBaseline, ThemeProvider } from '@mui/material'
import {
  BrowserRouter as Router,
  Outlet,
  Route,
  Routes,
} from 'react-router-dom'
// import ProtectedRoute from './components/ProtectedRoute'
import defaultTheme from './themes/default'
import Home from './pages/Home'
import Signup from './pages/Signup'
import Signin from './pages/Signin'
import Dashboardlayout from './layout/Dashboardlayout'
import ProtectedRoute from './components/ProtectedRoute'
import UserHome from './pages/dashboard/user/UserHome'
import NotImplemented from './pages/NotImplemented'
import ActiveElections from './pages/dashboard/user/ActiveElections'
import Voters from './pages/dashboard/admin/Voters'

function App() {
  return (
    <ThemeProvider theme={defaultTheme}>
      <div className='app'>
        <Router>
          <Routes>
            <Route index element={<Home />} />
            <Route path='/signup' element={<Signup />} />
            <Route path='/signin' element={<Signin />} />

            {/* Protected Pages */}
            <Route path='/dashboard' element={<Dashboardlayout />}>
              {/* User/Voter Pages */}
              <Route index element={<UserHome />} />
              <Route path='me' element={<UserHome />} />
              <Route path='active-elections' element={<ActiveElections />} />

              {/* Admin Pages */}
              <Route path='admin' element={<Outlet />}>
                <Route path='voters' element={<Voters />} />
              </Route>
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

