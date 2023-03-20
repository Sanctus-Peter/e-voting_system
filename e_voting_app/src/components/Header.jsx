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
import { Link } from 'react-router-dom'
import LogoPlaceHolder from './LogoPlaceHolder'

const pages = [
  { text: 'Home', url: '/' },
  { text: 'Signup', url: '/signup' },
  { text: 'Signin', url: '/signin' },
  { text: 'Elections', url: '/elections' },
]
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
function Header() {
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
        <Toolbar disableGutters>
          <Box
            sx={{ gap: '15px', display: { xs: 'none', md: 'flex' } }}
            className='brand'
          >
            <BrandName>
              {' '}
              <LogoPlaceHolder white={false} size={5} /> E-VOTING MS
            </BrandName>
          </Box>

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
            <Menu
              id='menu-appbar'
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {pages.map((page, i) => (
                <MenuItem key={i + 1} onClick={handleCloseNavMenu}>
                  <NavItem page={page} />
                </MenuItem>
              ))}
            </Menu>
          </Box>
          <BrandName
            sx={{
              flexGrow: 1,
              display: { xs: 'flex', md: 'none' },
              justifyContent: 'center',
            }}
          >
            <LogoPlaceHolder white={false} size={5} />{' '}
            <span style={{ flex: 1 }}>E-VOTING MS</span>
          </BrandName>
          <Box
            gap={1}
            sx={{
              flexGrow: 1,
              display: { xs: 'none', md: 'flex' },
              justifyContent: 'center',
              flexWrap: 'wrap',
            }}
          >
            {pages.map((page, i) => (
              <Button
                key={i + 1}
                onClick={handleCloseNavMenu}
                sx={{ my: 2, color: 'white', display: 'block' }}
              >
                <NavItem page={page} />
              </Button>
            ))}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  )
}

const NavItem = ({ page }) => {
  return (
    <Link
      style={{
        textDecoration: 'none',
        color: 'inherit',
      }}
      to={page.url}
    >
      <Typography textAlign='center'>{page.text}</Typography>
    </Link>
  )
}

export default Header
