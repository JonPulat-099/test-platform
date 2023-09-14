export default function ({ store, redirect }) {
  let user = store.state.auth.user

  if (!!user) {
    redirect('/')
  }
}
