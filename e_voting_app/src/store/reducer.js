export const initialState = {
  elections: [],
  loadingData: false,
  user: null,
  userType: null,
  token: null,
}

const updateFunction = (collection, modified, isDelete = false) => {
  const index = collection.findIndex((ses) => ses.id === modified?.id)
  const updated = [...collection]
  if (isDelete) updated.splice(index, 1)
  else updated[index] = modified
  return updated
}

export const reducer = (state, action) => {
  switch (action.type) {
    case 'SET_LOADING':
      return {
        ...state,
        loadingData: action.data,
      }

    case 'SET_ELECTIONS':
      return {
        ...state,
        elections: action.data,
      }

    case 'UPDATE_ELECTION':
      return {
        ...state,
        elections: updateFunction(state.elections, action.data),
      }
    case 'DELETE_ELECTION':
      return {
        ...state,
        elections: updateFunction(state.elections, { id: action.data }, true),
      }
    case 'ADD_ELECTION':
      return {
        ...state,
        elections: [...state.elections, action.data],
      }

    case 'SET_USER':
      return {
        ...state,
        user: action.data,
      }
    case 'SET_USER_TYPE':
      return {
        ...state,
        userType: action.data,
      }
    case 'UPDATE_USER': {
      return {
        ...state,
        user: { ...state.user, [action.key]: action.value },
      }
    }
    case 'SET_TOKEN':
      return {
        ...state,
        token: action.token,
      }
    case 'LOGOUT':
      return {
        ...state,
        token: null,
        user: null,
      }
    default:
      console.error(`Action ${action.type} not Implemented`)
      return state
  }
}
