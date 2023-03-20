import { Box, Typography } from '@mui/material'
import React from 'react'
import Controls from '../controls'

function SigninForm() {
  return (
    <form className='loginform signin'>
      <Typography>Signin</Typography>
      <Box display={'flex'} flexDirection='column' gap={'1rem'}>
        <Controls.Input />
        <Controls.Input />
        <Controls.Input />
        <Controls.Input />
        <Controls.Input />
      </Box>
    </form>
  )
}

export default SigninForm
