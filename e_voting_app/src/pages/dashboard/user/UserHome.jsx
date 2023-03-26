import { Avatar, Box, Typography } from '@mui/material'
import { Container } from '@mui/system'
import React from 'react'
import { sampleUser } from '../../../data_objects'
import {
  MdCalendarViewMonth,
  MdEmail,
  MdFemale,
  MdMale,
  MdOutlineVerifiedUser,
  MdPending,
  MdPhone,
  MdPinDrop,
} from 'react-icons/md'
import UserEditForm from '../../../components/forms/UserEditForm'
import PasswordUpdate from '../../../components/forms/PasswordUpdate'

function UserHome() {
  const user = sampleUser
  return (
    <Container
      maxWidth='xl'
      sx={{
        display: 'flex',
        flexDirection: { xs: 'column', md: 'row' },
        minHeight: '100%',
        gap: 2,
      }}
    >
      <Box
        flex={3}
        boxShadow={1}
        borderRadius={3}
        minHeight='90%'
        sx={{
          p: { xs: 2, md: 4 },
          // color: 'black',
        }}
      >
        {/* User Bio Header */}
        <Box display={'flex'} gap={2} mb={5}>
          <Avatar sx={{ width: '50px', height: '50px' }} />
          <Box>
            <Typography fontWeight={'bold'} variant='title'>
              {user.name}
            </Typography>
            <Box display='flex' gap='5px' alignItems='center'>
              {user.verified ? (
                <MdOutlineVerifiedUser fontSize={'1.2em'} />
              ) : (
                <MdPending color='#5555' fontSize={'1.2em'} />
              )}
              {user.verified ? 'Verified' : 'Pending'}
            </Box>
          </Box>
        </Box>

        {/* User Bio data */}

        <Box display={'flex'} flexDirection='column' gap='10px'>
          <UserBiodata
            title={'email'}
            icon={<MdEmail fontSize={'1.2em'} />}
            value={user.email}
          />

          <UserBiodata
            title={'Phone'}
            icon={<MdPhone fontSize={'1.2em'} />}
            value={user.mobile_no}
          />

          <UserBiodata
            title={'D.O.B'}
            icon={<MdCalendarViewMonth fontSize={'1.2em'} />}
            value={user?.dob}
          />

          <UserBiodata
            title={'Gender'}
            icon={
              user?.gender === 'male' ? (
                <MdMale fontSize='1.2em' />
              ) : (
                <MdFemale fontSize={'1.2em'} />
              )
            }
            value={user?.gender.toUpperCase()}
          />

          <UserBiodata
            title={'State'}
            icon={<MdPinDrop fontSize={'1.2em'} />}
            value={user?.state}
          />
          <UserBiodata
            title={'L.G.A'}
            icon={<MdPinDrop fontSize={'1.2em'} />}
            value={user?.lga}
          />
          <UserBiodata
            title={'Address'}
            icon={<MdPinDrop fontSize={'1.2em'} />}
            value={user?.address}
          />
        </Box>
      </Box>
      <Box
        flex={1.8}
        boxShadow={1}
        borderRadius={3}
        minHeight='90%'
        dislay='flex'
        sx={{
          p: { xs: 2, md: 4 },
        }}
      >
        <UserEditForm />
        <PasswordUpdate />
      </Box>
    </Container>
  )
}

const UserBiodata = ({ title, value, icon }) => {
  return (
    <Box
      sx={{ fontSize: { xs: '0.9em', md: '1.2em' } }}
      display={'flex'}
      gap={'10px'}
    >
      <Typography
        flex={0.5}
        textTransform={'uppercase'}
        fontWeight={'bold'}
        display='flex'
        variant='title'
        color='#555555'
        gap='5px'
        alignItems={'center'}
        sx={{ fontSize: { xs: '0.8em', md: '0.9em' } }}
      >
        {icon}

        {title}
      </Typography>
      <Typography flex={1} variant='subtitle'>
        {value}
      </Typography>
    </Box>
  )
}

export default UserHome
