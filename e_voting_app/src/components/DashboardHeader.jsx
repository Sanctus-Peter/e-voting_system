import React, { useState } from 'react'
// import './css/Header.css'
import {
  AppBar,
  Box,
  Toolbar,
  IconButton,
  Typography,
  Menu,
  MenuItem,
  Button,
  Container,
} from '@mui/material'
import { ImMenu } from 'react-icons/im'
// import darkLogo from '../assets/logo_dark.png'
import styled from '@emotion/styled'
import LogoPlaceHolder from './LogoPlaceHolder'

const BrandName = styled(Typography)`
  height: 44px;
  font-family: 'Irish Grover';
  font-style: normal;
  font-weight: 700;
  text-transform: small-caps;
  display: flex;
  gap: 10px;
  align-items: center;
  font-size: 28px;
  line-height: 44px;
`
function DashboardHeader() {
  const [anchorElNav, setAnchorElNav] = useState(null)

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget)
  }

  const handleCloseNavMenu = () => {
    setAnchorElNav(null)
  }

  return (
    <AppBar
      sx={{ background: '#ff3d00' }}
      position='sticky'
      className='header'
      elevation={0}
    >
      <Container maxWidth='xl'>
        <Toolbar disableGutters display='flex' justifyContent='space-between'>
          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size='large'
              aria-label='account of current user'
              aria-controls='menu-appbar'
              aria-haspopup='true'
              onClick={handleOpenNavMenu}
              color='inherit'
            >
              <ImMenu />
            </IconButton>
          </Box>
          <Box sx={{ gap: '15px' }} className='brand'>
            <BrandName>
              {' '}
              <LogoPlaceHolder white={false} size={5} /> E-VOTING MS
            </BrandName>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  )
}

export default DashboardHeader
