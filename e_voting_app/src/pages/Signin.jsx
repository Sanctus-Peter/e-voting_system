import React from 'react'
import HomeLayout from '../layout/HomeLayout'
import { Box } from '@mui/system'
import SigninForm from '../components/forms/SigninForm'

function Signin() {
  return (
    <HomeLayout>
      <Box sx={{ display: 'flex', height: '100%', width: '100%' }}>
        <Box sx={{ flex: 1 }}>Left side</Box>
        <Box sx={{ flex: 1, p: 2, justifyContent: 'center', display: 'flex' }}>
          <SigninForm />
        </Box>
      </Box>
    </HomeLayout>
  )
}

export default Signin
