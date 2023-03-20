import { TextField } from '@mui/material'
import React from 'react'

function Input({ name, value, error = null, changeFxn, label, ...others }) {
  return (
    <TextField
      variant='outlined'
      label={label}
      value={value}
      onChange={changeFxn}
      name={name}
      {...others}
      {...(error && { error: true, helperText: error })}
    />
  )
}

export default Input
