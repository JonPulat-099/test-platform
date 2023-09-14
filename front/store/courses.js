export const state = () => ({
  courses: [],
  currentPage: 1,
  perPage: 10,
  totalItems: 1
});
export const mutations = {
  SET_COURSES(state, courses) {
    state.courses = courses;
  },
  SET_CURRENT_PAGE(state, payload) {
    state.currentPage = payload;
  },
  SET_TOTAL_ITEMS(state, payload) {
    state.totalItems = payload;
  }
};
export const actions = {
  FETCH_COURSES({ commit, state }) {
    return new Promise((resolve, reject) => {
      this.$axios
        .$get("education/courses/", {
          params: {
            page: state.currentPage,
          },
        })
        .then(res => {
          commit("SET_COURSES", res.results);
          commit("SET_CURRENT_PAGE", res.current_page);
          commit("SET_TOTAL_ITEMS", res.total);
          resolve();
        })
        .catch(reject);
    });
  },
};
