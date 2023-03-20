import React from 'react'

import { Button as MuiButton } from '@mui/material'
import { makeStyles } from '@mui/styles'

const useStyles = makeStyles((theme) => ({
  root: {
    margin: theme.spacing(0.5) + ' !important',
  },
  label: {
    textTransform: 'none',
  },
}))

function Button({ text, size, color, variant, onClick, ...others }) {
  const classes = useStyles()
  return (
    <MuiButton
      variant={variant || 'contained'}
      size={size || 'large'}
      color={color || 'primary'}
      onClick={onClick}
      {...others}
      classes={{ root: classes.root, label: classes.label }}
    >
      {text}
    </MuiButton>
  )
}

export default Button
