import React from 'react'
import {
  FormControl,
  FormControlLabel,
  FormLabel,
  Radio,
  RadioGroup,
} from '@mui/material'

function MyRadio({
  value,
  changeFunction,
  name,
  items,
  label,
  showLetters = false,
  row = true,
  allowDisselect = false,
}) {
  const letters = ['A. ', 'B. ', 'C. ', 'D. ', 'E. ', 'F. ']
  return (
    <FormControl>
      <FormLabel>{label}</FormLabel>
      <RadioGroup row={row} value={value} name={name} onChange={changeFunction}>
        {items?.map((item, i) => (
          <FormControlLabel
            key={i + 12}
            value={item.value || item}
            control={<Radio />}
            label={(showLetters ? letters[i] : '') + (item.title || item)}
            {...(allowDisselect && { onClick: changeFunction })}
          />
        ))}
      </RadioGroup>
    </FormControl>
  )
}

export default MyRadio
