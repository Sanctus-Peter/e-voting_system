import { Typography } from '@mui/material'
import React, { useState } from 'react'
import LogoPlaceHolder from '../components/LogoPlaceHolder'

export function useForm(
  initialValues,
  validateOnChange = false,
  validateFunction
) {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState({})

  const changeFunction = (e) => {
    const { name, value } = e.target
    if (name.includes('.')) {
      const [object, property] = name.split('.')
      setValues({
        ...values,
        [object]: { ...values[object], [property]: value },
      })
    } else setValues({ ...values, [name]: value })
    if (validateOnChange) validateFunction({ [name]: value })
  }

  const resetForm = () => {
    setValues(initialValues)
    setErrors({})
  }
  return [values, setValues, resetForm, errors, setErrors, changeFunction]
}

export const Form = (props) => {
  const [submitting, setSubmitting] = useState(false)
  const { children, ref, onSubmit, title, withLogo = false, ...others } = props

  const handleSubmit = (e) => {
    if (submitting) return
    setSubmitting(true)
    onSubmit(e)
    setSubmitting(false)
  }
  return (
    <form
      className='loginform'
      action=''
      autoComplete='off'
      onSubmit={handleSubmit}
      encType='multipart/form-data'
      {...others}
      ref={ref}
    >
      {withLogo && <LogoPlaceHolder />}
      <Typography
        sx={{
          my: 1,
          textAlign: 'center',
          fontWeight: '600',
          fontSize: '22px',
        }}
        color='primary'
      >
        {title}
      </Typography>
      {children}
    </form>
  )
}
