import {
  FormControl,
  FormControlLabel,
  Checkbox as MuiCheckBox,
} from '@mui/material'
import React from 'react'

const changeMiddleware = (e) => ({
  target: {
    name: e.target.name,
    value: e.target.checked,
  },
})

function CheckBox({ name, label, value, changeFunction }) {
  return (
    <FormControl>
      <FormControlLabel
        control={
          <MuiCheckBox
            name={name}
            checked={value}
            color='primary'
            onChange={(e) => changeFunction(changeMiddleware(e))}
          />
        }
        label={label}
      />
    </FormControl>
  )
}

export default CheckBox
