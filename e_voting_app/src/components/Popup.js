import {
  Dialog,
  DialogContent,
  DialogTitle,
  Slide,
  Typography,
} from '@mui/material'
import { makeStyles } from '@mui/styles'
import React from 'react'
import Controls from './controls/Controls'
import CloseIcon from '@mui/icons-material/Close'

const useStyles = makeStyles((theme) => ({
  dialogWrapper: {
    padding: theme.spacing(2),
    position: 'absolute !important',
    top: theme.spacing(2),
  },
}))

function Popup(props) {
  const { title, children, open, setOpen } = props
  const classes = useStyles()
  return (
    <Dialog
      TransitionComponent={Transition}
      transitionDuration={700}
      open={open}
      onClose={() => setOpen(false)}
      maxWidth='md'
      classes={{ paper: classes.dialogWrapper }}
    >
      <DialogTitle>
        <div
          style={{
            minWidth: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <Typography variant='h6' component={'div'}>
            {title}
          </Typography>
          <Controls.ActionButton
            text={'X'}
            onClick={() => setOpen(false)}
            color='secondary'
            style={{ marginLeft: '16px' }}
          >
            <CloseIcon />
          </Controls.ActionButton>
        </div>
      </DialogTitle>
      <DialogContent dividers>{children}</DialogContent>
    </Dialog>
  )
}

const Transition = React.forwardRef(function Transition(props, ref) {
  return (
    <Slide direction='down' ref={ref} mountOnEnter unmountOnExit {...props} />
  )
})

export default Popup
