import { Box, Typography } from '@mui/material'
import React from 'react'

import Control from '../controls'

function SignupForm() {
  return (
    <form>
      <Typography>Signup</Typography>
      <Box display={'flex'} flexDirection='column' gap={'1rem'}>
        <Control.Input />
        <Control.Input />
        <Control.Input />
        <Control.Input />
        <Control.Input />
      </Box>
    </form>
  )
}

export default SignupForm
