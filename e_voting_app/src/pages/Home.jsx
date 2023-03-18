import styled from '@emotion/styled'
import { Button, Container, Grid, Typography } from '@mui/material'
import { Box } from '@mui/system'
import React from 'react'
import Header from '../components/Header'

const CtaButton = styled(Button)`
  padding: 25px 45px;
  color: #ffffff;
  background: #ff3d00;
  border-radius: 60px;
`

const UnderLine = styled('span')`
  display: block;
  height: 10px;
  width: 100px;
  border-radius: 8px;
  background-color: #ff3d00;
`

function Home() {
  return (
    <div>
      <Header />
      <HomeSection>
        <Typography variant='h1'>E-Voting</Typography>
        <Typography maxWidth={'700px'} textAlign='center'>
          Welcome to Vote, the most convenient and secure way to vote. Our
          platform is designed to make the voting process simple, fast, and
          accessible to everyone. With just a few clicks, you can exercise your
          right to vote and make your voice heard.
        </Typography>
        <CtaButton>Vote Now</CtaButton>
      </HomeSection>
      <HomeSection>
        <Typography variant='h4'>How It Works</Typography>
        <UnderLine />
      </HomeSection>
    </div>
  )
}

const HomeSection = ({ children }) => {
  return (
    <Grid
      display={'grid'}
      p={3}
      sx={{ minHeight: { xs: '55vh', md: '50vh' }, placeItems: 'center' }}
    >
      <Box
        display={'flex'}
        flexDirection='column'
        justifyContent={'center'}
        alignItems='center'
        gap={'1rem'}
      >
        {children}
      </Box>
    </Grid>
  )
}

export default Home
