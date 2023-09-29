export default function ({store, redirect}) {
  const user = store.state.auth.user
  if (!(user && user.can_view_results)) {
    redirect('/')
  }
}
