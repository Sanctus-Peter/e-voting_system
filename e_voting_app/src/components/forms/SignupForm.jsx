import { Box } from '@mui/material'
import React from 'react'
import { Form, useForm } from '../../custome_hooks/useForm'
import { signUpData } from '../../data_objects'
import Control from '../controls'

function SignupForm() {
  const [values, setValues, resetForm, errors, setErrors, changeFunction] =
    useForm({ ...signUpData })

  return (
    <Form title='Signup' withLogo={true}>
      <Box display={'flex'} flexDirection='column' gap={'1rem'}>
        <Control.Input
          changeFxn={changeFunction}
          label='Name'
          name={'name'}
          value={values.name}
          error={errors.name}
          required
        />
        <Control.Input
          type='date'
          name='dob'
          label={'D.O.B'}
          value={values.dob}
          changeFxn={changeFunction}
          error={errors.dob}
          required
        />
        <Control.Input
          name={'state'}
          value={values.state}
          label={'State'}
          error={errors.state}
          changeFxn={changeFunction}
          required
        />
        <Control.Input
          name={'lga'}
          value={values.lga}
          label={'L.G.A'}
          error={errors.lga}
          changeFxn={changeFunction}
          required
        />
        <Control.Input
          name={'mobile_no'}
          value={values.mobile_no}
          label={'Phone'}
          error={errors.mobile_no}
          changeFxn={changeFunction}
        />
        <Control.Input
          name={'address'}
          value={values.address}
          label={'Address'}
          error={errors.address}
          changeFxn={changeFunction}
        />
        <Control.Input
          name={'email'}
          value={values.email}
          label={'Email'}
          error={errors.email}
          changeFxn={changeFunction}
          required
        />
        <Control.Input
          name={'password'}
          value={values.password}
          label={'Password'}
          error={errors.password}
          changeFxn={changeFunction}
          required
        />
        <Control.Button text={'Signup'} />
      </Box>
    </Form>
  )
}

export default SignupForm
