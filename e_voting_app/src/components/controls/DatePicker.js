import React from 'react'
import TextField from '@mui/material/TextField'
import AdapterDateFns from '@mui/lab/AdapterDateFns'
import LocalizationProvider from '@mui/lab/LocalizationProvider'
import { DateTimePicker as MuiDateTime } from '@mui/lab/'
import { DatePicker as MuiDate } from '@mui/lab'
import { FormHelperText } from '@mui/material'

const changeMiddleware = (name, value) => ({
  target: {
    name,
    value,
  },
})

function DateTimePicker({
  name,
  label,
  value,
  error,
  changeFunction,
  ...others
}) {
  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <MuiDateTime
        renderInput={(props) => <TextField {...props} />}
        variant='inline'
        inputVariant='outlined'
        label={label}
        inputFormat={'MM/dd/yyyy hh:mm'}
        name={name}
        value={value}
        {...(error && { InputProps: { error: true, errorText: error } })}
        {...others}
        onChange={(date) => changeFunction(changeMiddleware(name, date))}
      />
      {error && (
        <FormHelperText
          style={{ color: 'red', marginLeft: '10px', fontWeight: '500' }}
        >
          {error}
        </FormHelperText>
      )}
    </LocalizationProvider>
  )
}

export function DatePicker({
  name,
  label,
  value,
  error,
  changeFunction,
  ...others
}) {
  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <MuiDate
        renderInput={(props) => <TextField {...props} />}
        variant='inline'
        inputVariant='outlined'
        label={label}
        inputFormat={'dd/MM/yyyy'}
        name={name}
        value={value}
        {...(error && { InputProps: { error: true, errorText: error } })}
        {...others}
        onChange={(date) => changeFunction(changeMiddleware(name, date))}
      />
      {error && (
        <FormHelperText
          style={{ color: 'red', marginLeft: '10px', fontWeight: '500' }}
        >
          {error}
        </FormHelperText>
      )}
    </LocalizationProvider>
  )
}

export default DateTimePicker
