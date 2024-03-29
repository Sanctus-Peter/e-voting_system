import React from 'react'
import { useEffect } from 'react'
import { Navigate } from 'react-router-dom'
import { useStateValue } from '../store/StateProvider'

function ProtectedRoute({ children, restrictedTo = [], redirect = '/' }) {
  const [{ user }, dispatch] = useStateValue()
  const loggedInUser = JSON.parse(localStorage.getItem('user'))

  useEffect(() => {
    if (!user && loggedInUser) {
      dispatch({ type: 'SET_USER', data: loggedInUser })
    }
  }, [user, loggedInUser])

  if (!loggedInUser) {
    return <Navigate to='/' replace={true} />
  }

  if (restrictedTo.length && !restrictedTo.includes(loggedInUser?.role)) {
    return <Navigate to={redirect} replace={true} />
  }

  return <>{children}</>
}

export default ProtectedRoute
