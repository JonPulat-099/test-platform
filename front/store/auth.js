export const state = () => ({
  user: undefined,
  token: undefined,
  error: "Логин ёки парол хато"
});

export const actions = {
  async LOAD_TOKEN({ commit }) {
    const token = await localStorage.getItem("token");
    await localStorage.setItem("token", token);
    this.$axios.defaults.headers.common.Authorization = "Token " + token;
    commit("SET_TOKEN", token);
  },

  LOGIN({ commit }, { username, password }) {
    return new Promise((resolve, reject) => {
      this.$axios
        .$post(
          "login/",
          {
            username,
            password
          },
          {
            headers: {
              Authorization: null
            }
          }
        )
        .then(response => {
          if (response.token) {
            const token = response.token;
            localStorage.setItem("token", token);
            this.$axios.defaults.headers.common.Authorization =
              "Token " + token;
            commit("SET_TOKEN", token);
            this.$router.push(`/courses`);
          }
          resolve(response);
        })
        .catch(error => {
          reject(error);
        });
    });
  },

  FETCH_USER({ commit }) {
    return new Promise((resolve, reject) => {
      this.$axios
        .$get("profile/")
        .then(response => {
          commit("SET_USER", response);
          resolve(response);
        })
        .catch(error => {
          reject(error);
        });
    });
  },

  LOGOUT({ commit }) {
    return new Promise(resolve => {
      this.$axios.get("logout/").finally(() => {
        localStorage.removeItem("token");
        delete this.$axios.defaults.headers.common.Authorization;
        commit("SET_TOKEN", undefined);
        location.reload();
        resolve();
      });
    });
  }
};

export const mutations = {
  SET_TOKEN(state, token) {
    state.token = token;
  },
  SET_ERROR(state) {
    state.error = true;
  },
  SET_USER(state, user) {
    state.user = user;
  }
};
