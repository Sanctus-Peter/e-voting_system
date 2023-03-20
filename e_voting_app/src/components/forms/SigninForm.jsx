import { Box, Typography } from '@mui/material'
import React from 'react'
import { Form, useForm } from '../../custome_hooks/useForm'
import { signInData } from '../../data_objects'
import Controls from '../controls'

function SigninForm() {
  const [values, setValues, resetForm, errors, setErrors, changeFunction] =
    useForm({ ...signInData })
  return (
    <Form title='Signin' withLogo={true}>
      <Box display={'flex'} flexDirection='column' gap={'1rem'}>
        <Controls.Input
          name={'username'}
          label={'Email'}
          changeFxn={changeFunction}
          error={errors.username}
          value={values.username}
          required
        />
        <Controls.Input
          name={'password'}
          label={'Password'}
          type='password'
          changeFxn={changeFunction}
          error={errors.password}
          value={values.password}
          required
        />

        <Controls.Button text={'Signin'} />
      </Box>
    </Form>
  )
}

export default SigninForm
