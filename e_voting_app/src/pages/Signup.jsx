import { Box } from '@mui/system'
import React from 'react'
import SignupForm from '../components/forms/SignupForm'
import HomeLayout from '../layout/HomeLayout'

function Signup() {
  return (
    <HomeLayout>
      <Box sx={{ display: 'flex', height: '100%', width: '100%' }}>
        <Box sx={{ flex: 1 }}>Left side</Box>
        <Box sx={{ flex: 1, p: 2, justifyContent: 'center', display: 'flex' }}>
          <SignupForm />
        </Box>
      </Box>
    </HomeLayout>
  )
}

export default Signup
