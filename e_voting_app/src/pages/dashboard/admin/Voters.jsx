import { Avatar, Box, Container } from '@mui/material'
import React from 'react'
import MyTable from '../../../components/MyTable'
import { sampleVoters } from '../../../data_objects'

function Voters() {
  const columns = [
    {
      field: 'name',
      headerName: 'Voter Name',
      width: 250,
      valueGetter: (params) => params.row.name,
      renderCell: (params) => {
        return (
          <Box display='flex' gap={1} alignItems='center'>
            <Avatar />
            {/* <img src={params.row.passport} alt='' className='user__image' /> */}
            {params.row.name}
          </Box>
        )
      },
    },
    { field: 'gender', headerName: 'Gender', width: 150 },
    { field: 'nin', headerName: 'NIN', width: 150 },
    { field: 'state', headerName: 'State', width: 150 },
    { field: 'lga', headerName: 'L.G.A', width: 150 },
  ]

  return (
    <Container
      maxWidth='xl'
      sx={{
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100%',
        p: 2,
        gap: 2,
      }}
    >
      <MyTable data={sampleVoters} columns={columns} label='Voter' />
    </Container>
  )
}

export default Voters
