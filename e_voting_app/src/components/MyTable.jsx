import React from 'react'
// import { useStateValue } from '../StateProvider'
import { Button, IconButton, Tooltip } from '@mui/material'
import { DataGrid, GridToolbar } from '@mui/x-data-grid'
import { Link } from 'react-router-dom'
import { MdAdd, MdDelete, MdDetails, MdSearch } from 'react-icons/md'
import { Box } from '@mui/system'
import Controls from './controls'

function MyTable({ columns, data, label, actions = true }) {
  // const [{ setNotify, setConfirmDialog, showForm }, dispatch] = useStateValue()

  const handleDelete = (id) => {
    // const deleteCallback = () =>
    //   dispatch({ type: `DELETE_${label.toUpperCase()}`, data: id })
    // setConfirmDialog({
    //   title: `Are you sure you want to Delete this ${label}?`,
    //   subtitle: "You can't undo this action!",
    //   open: true,
    //   callback: () => {
    //     deleteData(`/${label.toLowerCase()}s/${id}`, setNotify, deleteCallback)
    //     setNotify({ message: label + ' Deleted successfully', type: 'error' })
    //   },
    // })
  }

  const handleSearch = (e) => {}
  const displayNewForm = (e) => {
    // const { show, title } = showForm
    // title(`Add New ${label}`)
    // show(true)
  }

  if (actions && columns[columns.length - 1]?.field !== 'actions')
    columns.push({
      field: 'actions',
      headerName: 'Actions',
      sortable: false,
      disableExport: true,
      filterable: false,
      width: 160,
      renderCell: (params) => (
        <Box display={'flex'} gap={2}>
          <Link to={`${params.row.id}`} className='link'>
            <Button
              variant='contained'
              size='small'
              onClick={() => {}}
              startIcon={<MdDetails fontSize={'small'} />}
            >
              Details
            </Button>
          </Link>
          <Tooltip title={'Delete ' + label}>
            <IconButton onClick={() => handleDelete(params.row.id)}>
              <MdDelete color='red' />
            </IconButton>
          </Tooltip>
        </Box>
      ),
    })
  return (
    <>
      {actions && (
        <div
          style={{
            minWidth: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
          // className={classes.searchContainer}
        >
          <Controls.Input
            style={{
              width: '75%',
            }}
            // className={classes.serchInput}
            label={`Search ${label}s`}
            name={'query'}
            size='small'
            InputProps={{ startAdornment: <MdSearch fontSize='small' /> }}
            onChange={handleSearch}
          />
          <Controls.Button
            text={'Add New'}
            variant='outlined'
            size={'small'}
            sx={{ fontSize: { xs: '0.6', md: '1em' } }}
            onClick={displayNewForm}
            startIcon={<MdAdd />}
          />
        </div>
      )}
      <DataGrid
        sx={{
          padding: 1,
          minHeight: 'height: calc(100vh-320px);',
          width: '100%',
        }}
        // className={classes.studentList}
        components={{ Toolbar: GridToolbar }}
        autoHeight
        rows={data || []}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[10, 15, 25]}
        checkboxSelection
        disableSelectionOnClick
      />
    </>
  )
}

export default MyTable
