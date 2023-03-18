import styled from '@emotion/styled'
import { Button, Grid, Typography } from '@mui/material'
import { Box } from '@mui/system'
import React from 'react'
import Header from '../components/Header'

const CtaButton = styled(Button)`
  padding: 30px 45px;
  color: #ffffff;
  background: #ff3d00;
  border-radius: 60px;
`

function Home() {
  return (
    <div>
      <Header />
      <Grid
        display={'grid'}
        style={{}}
        sx={{ minHeight: { xs: '700px', md: '60vh' }, placeItems: 'center' }}
      >
        <Box
          display={'flex'}
          flexDirection='column'
          justifyContent={'center'}
          alignItems='center'
          gap={'1rem'}
          flex={1}
          p={2}
        >
          <Typography variant='h1'>E-Voting</Typography>
          <Typography maxWidth={'700px'} textAlign='center'>
            Welcome to Vote, the most convenient and secure way to vote. Our
            platform is designed to make the voting process simple, fast, and
            accessible to everyone. With just a few clicks, you can exercise
            your right to vote and make your voice heard.
          </Typography>
          <CtaButton>Vote Now</CtaButton>
        </Box>
      </Grid>
    </div>
  )
}

export default Home
