import styled from '@emotion/styled'
import {
  Table,
  TableCell,
  TableHead,
  TableRow,
  TablePagination,
  TableSortLabel,
} from '@mui/material'
import React, { useState } from 'react'

const MyTable = styled(Table)(({ theme }) => ({
  marginTop: theme.spacing(3),
  '& thead th': {
    fontWeight: '600',
    color: theme.palette.primary.main,
    backgroundColor: 'lightgray',
  },
  '& tbody td': {
    fontWeight: '300',
  },
  '& tbody tr :hover': {
    backgroundColor: '#fffbfz',
    cursor: 'pointer',
  },
}))

function useTable(records, headCols, filter) {
  const pages = [5, 10, 25]
  const [page, setPage] = useState(0)
  const [rowsPerPage, setRowsPerPage] = useState(pages[0])

  const [order, setOrder] = useState('asc')
  const [orderBy, setOrderBy] = useState()

  const handleSort = (cellID) => {
    const isAsc = orderBy === cellID && order === 'asc'
    setOrder(isAsc ? 'dsc' : 'asc')
    setOrderBy(cellID)
  }
  const handleChangePage = (event, newPage) => {
    setPage(newPage)
  }
  const handleRowsChange = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10))
    setPage(0)
  }

  const getComparator = () => {
    const comparator = (a, b) => {
      if (a[orderBy] < b[orderBy]) return -1
      else if (a[orderBy] > b[orderBy]) return 1
      else return 0
    }
    return order === 'asc'
      ? (a, b) => comparator(a, b)
      : (a, b) => -comparator(a, b)
  }

  const mySort = (array, cmpFxn) => {
    const temp = array.map((a, i) => [a, i])
    temp.sort((a, b) => {
      const order = cmpFxn(a[0], b[0])
      if (order !== 0) return order
      return a[1] - b[1]
    })
    return temp.map((a) => a[0])
  }

  const recordsAfterPagination = () => {
    return mySort(filter.fn(records), getComparator()).slice(
      page * rowsPerPage,
      (page + 1) * rowsPerPage
    )
  }
  const TableContainer = (props) => <MyTable>{props.children}</MyTable>

  const TblPagination = () => (
    <TablePagination
      rowsPerPageOptions={pages}
      component='div'
      count={records.length}
      page={page}
      rowsPerPage={rowsPerPage}
      onPageChange={handleChangePage}
      onRowsPerPageChange={handleRowsChange}
    />
  )

  const TblHead = (props) => (
    <TableHead>
      <TableRow>
        {headCols.map((hd, i) => (
          <TableCell
            key={hd.id}
            sortDirection={orderBy === hd.id ? order : false}
          >
            {hd.disableSort ? (
              hd.label
            ) : (
              <TableSortLabel
                active={orderBy === hd.id}
                direction={orderBy === hd.id ? order : 'asc'}
                onClick={() => handleSort(hd.id)}
              >
                {hd.label}
              </TableSortLabel>
            )}
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  )
  return { TableContainer, TblHead, TblPagination, recordsAfterPagination }
}

export default useTable
