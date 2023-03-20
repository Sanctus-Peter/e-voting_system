import styled from '@emotion/styled'
import { Button, Grid, Typography } from '@mui/material'
import { Box } from '@mui/system'
import React from 'react'
import HowItWorksCard from '../components/HowItWorksCard'
import { MdOutlineVerifiedUser } from 'react-icons/md'
import { BiSelectMultiple } from 'react-icons/bi'
import { SlCalculator } from 'react-icons/sl'
import HomeLayout from '../layout/HomeLayout'

const CtaButton = styled(Button)(({ theme }) => ({
  padding: `16px 48px`,
  color: '#ffffff',
  background: '#ff3d00',
  borderRadius: '60px',
  '&:hover': {
    transition: '0.3s',
    color: '#ff3d00',
    background: '#ffffff',
    border: '1.5px solid #ff3d00',
    transform: 'translateY(-3px)',
    fontWeight: '600',
  },
}))

const UnderLine = styled('span')`
  display: block;
  height: 10px;
  width: 100px;
  border-radius: 8px;
  background-color: #ff3d00;
`

function Home() {
  return (
    <HomeLayout>
      <HomeSection index={1}>
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
        <Box
          display={'flex'}
          flexWrap='wrap'
          justifyContent={'space-around'}
          gap={2}
          mt={2}
        >
          <HowItWorksCard
            title='Account Verification'
            icon={<MdOutlineVerifiedUser color='#ff3d00' fontSize={'5em'} />}
            info='Sign Up your Account with the necessary details and await verification from the admins'
          />
          <HowItWorksCard
            title='Select Candidate'
            icon={<BiSelectMultiple color='#ff3d00' fontSize={'5em'} />}
            info='Choose Your Prefereed Candidtae in aany of your eligible election and vote for them'
          />
          <HowItWorksCard
            icon={<SlCalculator color='#ff3d00' fontSize={'5em'} />}
            title='Voting Results'
            info={'View Live Update of result in all Elections '}
          />
        </Box>
      </HomeSection>
    </HomeLayout>
  )
}

const HomeSection = ({ children, index = 0 }) => {
  const background = index ? 'rgb(196,164,132)' : 'rgb(251,251,253)'
  const color = index ? '#ffffff' : '#000000'
  return (
    <Grid
      display={'grid'}
      p={3}
      sx={{
        minHeight: { xs: '55vh', md: '65vh' },
        placeItems: 'center',
        background,
        color,
      }}
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
