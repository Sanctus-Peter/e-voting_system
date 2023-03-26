import { Typography } from '@mui/material'
import { Box } from '@mui/system'
import React, { useState } from 'react'
import Controls from '../components/controls'

function useElectionFilter() {
  const [filters, setFilters] = useState({
    state: '',
    lga: '',
  })
  const changeFunction = (e) => {
    const { name, value } = e.target
    setFilters({ ...filters, [name]: value })
  }
  const FilterComponent = () => {
    return (
      <Box margin='1rem auto' width='90%' p='8px 16px'>
        <Typography
          sx={{
            fontSize: { xs: '0.6em', md: '0.8em' },
            textTransform: 'small-caps',
            mb: 1,
          }}
        >
          Filter Elections
        </Typography>
        <Box display={'flex'} gap={1}>
          <Controls.Input
            changeFxn={changeFunction}
            label='By State'
            name={'state'}
            value={filters.state}
            size='small'
          />
          <Controls.Input
            changeFxn={changeFunction}
            label='By L.G.A'
            name={'lga'}
            size='small'
            value={filters.lga}
          />
        </Box>
      </Box>
    )
  }

  return [filters, FilterComponent]
}

export default useElectionFilter
