import { createTheme } from '@mui/material'

const theme = createTheme({
  palette: {
    type: 'light',
    primary: {
      main: '#ff3d00',
      dark: '#504E67',
      light: '#171150',
    },
    secondary: {
      main: '#FD295A',
    },
    background: {
      default: '#F8F9FD',
      white: ' rgba(255, 255, 255, 0.961)',
    },
  },
  typography: {
    fontFamily: "'Poppins', Roboto, Helvetica, Arial, sans-serif",
  },

  overrides: {
    MuiPaper: {
      backgroundColor: '#171150',
    },
  },
})

export default theme
