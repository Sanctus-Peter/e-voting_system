import React from 'react'
import { Box } from '@mui/system'
import DashboardHeader from '../components/DashboardHeader'
import Sidebar from '../components/Sidebar'
import { Outlet } from 'react-router-dom'

function Dashboardlayout({ children }) {
  return (
    <Box
      sx={{
        w: '100vw',
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
      }}
    >
      <DashboardHeader />
      <Box
        sx={{
          w: '100vw',
          height: '100%',
          flex: 1,
          display: 'flex',
          gap: '1rem',
          p: 2,
        }}
      >
        <Sidebar />

        <Box
          sx={{
            flex: 1,
            height: 'calc(100vh - 100px)',
            overflowY: 'scroll',
          }}
        >
          <Outlet />
        </Box>
      </Box>
    </Box>
  )
}

export default Dashboardlayout
