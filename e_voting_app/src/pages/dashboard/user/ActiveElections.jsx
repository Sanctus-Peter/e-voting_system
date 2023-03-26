import { Container } from '@mui/material'
import { Box } from '@mui/system'
import React from 'react'
import useElectionFilter from '../../../custome_hooks/useElectionFilter'
import ActiveElection from '../../../components/ActiveElection'

function ActiveElections() {
  const [filters, FilterComponent] = useElectionFilter()
  return (
    <Container
      maxWidth='xl'
      sx={{
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100%',
        alignItems: 'center',
        gap: 2,
      }}
    >
      <FilterComponent />
      <Box
        display='flex'
        justifyContent={'space-around'}
        gap={2}
        flexWrap='wrap'
      >
        <ActiveElection
          election={{
            name: 'Governorship Election',
            startDate: new Date(),
            stopDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
          }}
        />
        <ActiveElection
          election={{
            name: 'House of Reps Election',
            startDate: new Date(),
            stopDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
          }}
        />
        <ActiveElection
          election={{
            name: 'Presidential Election',
            startDate: new Date(),
            stopDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
          }}
        />
        <ActiveElection
          election={{
            name: 'Senate Election',
            startDate: new Date(),
            stopDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
          }}
        />
      </Box>
    </Container>
  )
}

export default ActiveElections
