import React from 'react'
import Card from '@mui/material/Card'
import CardActions from '@mui/material/CardActions'
import CardContent from '@mui/material/CardContent'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'

function HowItWorksCard({ title, info, icon }) {
  return (
    <Card sx={{ width: 270, minHeight: 300 }}>
      <CardContent sx={{ gap: 1 }}>
        <Typography
          sx={{ fontSize: 14, fontWeight: '600' }}
          // color='text.secondary'
          variant='h5'
          textAlign={'center'}
          gutterBottom
        >
          {title}
        </Typography>
        <Typography variant='h5' component='div'></Typography>
        <Typography
          flex={1}
          sx={{ mb: 1.5 }}
          display='flex'
          justifyContent={'center'}
          alignItems='center'
          component='div'
          color='text.secondary'
        >
          {icon}
        </Typography>
        <Typography variant='body2'>{info}</Typography>
      </CardContent>
      <CardActions>
        <Button size='small'>Learn More</Button>
      </CardActions>
    </Card>
  )
}

export default HowItWorksCard
