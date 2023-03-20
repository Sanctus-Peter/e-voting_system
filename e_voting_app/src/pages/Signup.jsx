import { Box } from '@mui/system'
import React from 'react'
import SignupForm from '../components/forms/SignupForm'
import HomeLayout from '../layout/HomeLayout'

function Signup() {
  return (
    <HomeLayout>
      <Box sx={{ display: 'flex', height: '100%', width: '100%' }}>
        <Box sx={{ flex: 1, display: { xs: 'none', md: 'flex' } }}>
          Left side
        </Box>
        <Box
          sx={{
            flex: 1,
            p: 2,
            justifyContent: 'center',
            display: 'flex',
            height: '80vh',
            overflowY: 'scroll',
          }}
        >
          <SignupForm />
        </Box>
      </Box>
    </HomeLayout>
  )
}

export default Signup
