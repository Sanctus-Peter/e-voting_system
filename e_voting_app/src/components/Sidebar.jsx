import { Typography } from '@mui/material'
import { Box } from '@mui/system'
import React from 'react'
import { BiDice6, BiHistory, BiUser } from 'react-icons/bi'
import { MdPeople } from 'react-icons/md'
import { NavLink } from 'react-router-dom'
import './css/Sidebar.css'

const userNavs = [
  {
    text: 'Profile',
    url: '/dashboard/me',
    icon: <BiUser fontSize={'2em'} />,
  },
  {
    text: 'Active Elections',
    url: '/dashboard/active-elections',
    icon: <BiDice6 fontSize={'2em'} />,
  },
  {
    text: 'Vote History',
    url: '/dashboard/vote-history',
    icon: <BiHistory fontSize={'2em'} />,
  },
]

const adminNavs = [
  {
    text: 'Manage Voters',
    url: '/dashboard/admin/voters',
    icon: <MdPeople fontSize={'2em'} />,
  },
  {
    text: 'Manage Elections',
    url: '/dashboard/admin/elections',
    icon: <BiDice6 fontSize={'2em'} />,
  },
  {
    text: 'Manage Candidates',
    url: '/dashboard/admin/candidates',
    icon: <MdPeople fontSize={'2em'} />,
  },
  {
    text: 'Manage Parties',
    url: '/dashboard/admin/parties',
    icon: <BiHistory fontSize={'2em'} />,
  },
]

function Sidebar() {
  return (
    <Box
      sx={{
        color: '#ffffff',
        flex: 0.3,
        height: 'calc(100vh - 100px)',
        display: { xs: 'none', md: 'flex' },
        overflowY: 'scroll',
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

      <Typography
        sx={{
          fontSize: '1.5em',
          textAlign: 'center',
          my: 3,
          textDecoration: 'underline',
        }}
      >
        Admin
      </Typography>
      {adminNavs.map((nav, i) => (
        <SidebarItem {...nav} key={i + 100} />
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
