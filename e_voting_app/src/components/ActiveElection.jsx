import React from 'react'
import {
  Button,
  Card,
  CardActions,
  CardContent,
  Typography,
} from '@mui/material'
import { MdTimer, MdTimerOff } from 'react-icons/md'
import LogoPlaceHolder from '../components/LogoPlaceHolder'

function ActiveElection({ election }) {
  return (
    <Card
      sx={{
        width: 260,
        minHeight: 300,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
      }}
    >
      <CardContent sx={{ gap: 1 }}>
        <LogoPlaceHolder character={election?.name.charAt(0)} size={10} />

        <Typography
          sx={{ fontSize: 14, fontWeight: '600', mt: 2 }}
          // color='text.secondary'
          variant='h5'
          textAlign={'center'}
          gutterBottom
        >
          {election?.name}
        </Typography>
        <Typography
          flex={1}
          sx={{ mb: 1.5 }}
          display='flex'
          gap={2}
          flexDirection={'column'}
          justifyContent={'center'}
          alignItems='center'
          component='div'
          color='text.secondary'
        >
          <div>
            <MdTimer /> Start: {election?.startDate.toLocaleString()}
          </div>
          <div>
            <MdTimerOff /> Stop: {election?.stopDate.toLocaleString()}
          </div>
        </Typography>
        <Typography variant='body2'></Typography>
      </CardContent>
      <CardActions>
        <Button size='small' variant='contained'>
          Vote
        </Button>
        <Button size='small' variant='contained'>
          View Results
        </Button>
      </CardActions>
    </Card>
  )
}

export default ActiveElection
