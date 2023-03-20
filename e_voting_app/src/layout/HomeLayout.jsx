import { Box } from '@mui/system'
import React from 'react'
import Footer from '../components/Footer'
import Header from '../components/Header'

function HomeLayout({ children, withHeader = true, withFooter = true }) {
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
      {withHeader && <Header />}
      <Box sx={{ flex: 1 }}>{children}</Box>
      {withFooter && <Footer />}
    </Box>
  )
}

export default HomeLayout
