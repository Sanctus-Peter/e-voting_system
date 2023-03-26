import { Box } from '@mui/material'
import React from 'react'
import { Form, useForm } from '../../custome_hooks/useForm'
import { sampleUser } from '../../data_objects'
import Controls from '../controls'

function UserEditForm() {
  const [values, setValues, resetForm, errors, setErrors, changeFunction] =
    useForm({ ...sampleUser })

  return (
    <Form title='Update Bio' marginBottom='1rem'>
      <Box display={'flex'} flexDirection='column' gap={'1rem'}>
        <Controls.Input
          name={'mobile_no'}
          value={values.mobile_no}
          label={'Phone'}
          error={errors.mobile_no}
          changeFxn={changeFunction}
        />
        <Controls.Input
          name={'address'}
          value={values.address}
          label={'Address'}
          error={errors.address}
          changeFxn={changeFunction}
        />
        <Controls.Input
          name={'email'}
          value={values.email}
          label={'Email'}
          error={errors.email}
          changeFxn={changeFunction}
          required
        />
      </Box>
    </Form>
  )
}

export default UserEditForm
