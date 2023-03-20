import { Button } from '@mui/material'
import { makeStyles } from '@mui/styles'
import React from 'react'

const useStyles = makeStyles((theme) => ({
  root: {
    minWidth: 0,
    width: '40px',
    height: '40px',
    margin: theme.spacing(0.5),
    borderRadius: '50% !important',
    padding: '5px !important',
    color: '#fff',
  },
  secondary: {
    backgroundColor: 'red !important' || theme.palette.secondary.light,
    color: '#fff',
    '& .MuiButton-label': {
      color: '#fff' || theme.palette.secondary.main,
    },
  },
  primary: {
    backgroundColor: theme.palette.primary.light,
    '& .MuiButton-label': {
      color: theme.palette.primary.main,
    },
  },
}))

function ActionButton({ children, color, onClick, ...others }) {
  const classes = useStyles()
  return (
    <Button
      {...others}
      onClick={onClick}
      className={`${classes.root} ${classes[color]}`}
    >
      {children}
    </Button>
  )
}

export default ActionButton
