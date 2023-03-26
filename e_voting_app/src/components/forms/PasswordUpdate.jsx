import { Box } from '@mui/material'
import React from 'react'
import { Form, useForm } from '../../custome_hooks/useForm'
import Controls from '../controls'

function PasswordUpdate() {
  const [values, setValues, resetForm, errors, setErrors, changeFunction] =
    useForm({ oldpassword: '', password: '', confirmpass: '' })
  return (
    <Form title='Update Password'>
      <Box display={'flex'} flexDirection='column' gap={'1rem'}>
        <Controls.Input
          name={'oldpassword'}
          label={'Old Password'}
          type='password'
          changeFxn={changeFunction}
          error={errors.oldpassword}
          value={values.oldpassword}
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

        <Controls.Input
          name={'confirmpass'}
          label={'Confirm Password'}
          type='password'
          changeFxn={changeFunction}
          error={errors.confirmpass}
          value={values.confirmpass}
          required
        />

        <Controls.Button text={'Update'} />
      </Box>
    </Form>
  )
}

export default PasswordUpdate
