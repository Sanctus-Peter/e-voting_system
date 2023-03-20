import {
  FormControl,
  FormHelperText,
  InputLabel,
  MenuItem,
  Select as MuiSelect,
} from '@mui/material'
import React from 'react'

function Select({ name, label, value, changeFunction, options, error = null }) {
  return (
    <FormControl variant='outlined' error={error}>
      <InputLabel style={{ backgroundColor: '#fff', padding: '0 4px' }}>
        {label}
      </InputLabel>
      <MuiSelect name={name} value={value} onChange={changeFunction}>
        <MenuItem value=''>None</MenuItem>
        {options.map((op, i) => (
          <MenuItem value={op._id || op} key={op._id || i + 1}>
            {op.title || op}
          </MenuItem>
        ))}
      </MuiSelect>
      {error && <FormHelperText>{error}</FormHelperText>}
    </FormControl>
  )
}

export default Select
