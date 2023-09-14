export default function ({$axios, store, redirect}) {
  $axios.onError(async (error) => {
    if (error.response.status === 401) {
      store.commit('auth/SET_TOKEN', undefined)
      store.commit('auth/SET_USER', undefined)
      redirect('/auth')
    }
  })
}
