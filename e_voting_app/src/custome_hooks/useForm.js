import { makeStyles } from '@mui/styles'
import React, { useState } from 'react'
import Loading from './loading/Loading'

const useStyles = makeStyles((theme) => ({
  root: {
    position: 'relative',
    '& .MuiFormControl-root': {
      width: '85%',
      margin: theme.spacing(1),
    },
    '& .MuiSvgIcon-root': {
      marginRight: theme.spacing(1),
    },
  },
}))

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
  const classes = useStyles()
  const [submitting, setSubmitting] = useState(false)
  const { children, ref, onSubmit, ...others } = props

  const handleSubmit = (e) => {
    setSubmitting(true)
    onSubmit(e)
    setSubmitting(false)
  }
  return (
    <form
      action=''
      className={classes.root}
      autoComplete='off'
      onSubmit={handleSubmit}
      encType='multipart/form-data'
      {...others}
      ref={ref}
    >
      {submitting && <Loading />}
      {children}
    </form>
  )
}
