import { Typography } from '@mui/material'
import { Box } from '@mui/system'
import React from 'react'
import { BiUser } from 'react-icons/bi'
import { NavLink } from 'react-router-dom'
import './css/Sidebar.css'

const userNavs = [
  {
    text: 'Profile',
    url: '/dashboard',
    icon: <BiUser fontSize={'2em'} />,
  },
]

function Sidebar() {
  return (
    <Box
      sx={{
        color: '#ffffff',
        flex: 0.3,
        height: 'calc(100vh - 100px)',
      }}
    >
      <SidebarContent />
    </Box>
  )
}

const SidebarContent = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        gap: '10px',
        width: '300px',
        minHeight: '100%',
        backgroundColor: '#ff3d00',
        color: '#ffffff',
        borderRadius: 8,
        overflowY: 'scroll',
        px: 2,
        py: 8,
      }}
    >
      {userNavs.map((nav, i) => (
        <SidebarItem {...nav} key={i + 1} />
      ))}
    </Box>
  )
}

const SidebarItem = ({ text, icon, url }) => {
  return (
    <NavLink
      to={url}
      className={({ isActive }) => `sidenav__navlink ${isActive && 'active'}`}
    >
      <Box display={'flex'} alignItems='center' gap='10px'>
        {icon}
        <Typography fontSize={'lg'}>{text}</Typography>
      </Box>
    </NavLink>
  )
}

export default Sidebar
