import React from 'react'
import './css/logoplaceholder.css'

function LogoPlaceHolder({ white = true, size = 7 }) {
  size *= 10
  return (
    <span
      style={{
        width: `${size}px`,
        height: `${size}px`,
      }}
      className={`logoplaceholder ${white ? 'white' : 'dark'}`}
    >
      E
    </span>
  )
}

export default LogoPlaceHolder
