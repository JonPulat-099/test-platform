<template>
  <header>
    <div class="container-fluid">
      <div class="row align-items-center navbar">
        <div
          class="col-12 col-lg-6 d-flex align-items-center justify-content-between"
        >
          <div style="text-align: center">
            <h2>Tashkent International University<br /></h2>
            <h4>
              {{ user.full_name }}
              <template v-if="user.u_group_name"
                >- {{ user.u_group_name }}</template
              >
            </h4>
          </div>
        </div>
        <div class="col-12 col-lg-6 pt-4">
          <nav class="d-flex  align-items-center justify-content-end">
            <button class="btn logout ml-2" @click.prevent="logout">
              <span> Chiqish </span>
              <svg
                width="20"
                height="20"
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M13 1H17C17.5304 1 18.0391 1.21071 18.4142 1.58579C18.7893 1.96086 19 2.46957 19 3V17C19 17.5304 18.7893 18.0391 18.4142 18.4142C18.0391 18.7893 17.5304 19 17 19H13M8 15L13 10M13 10L8 5M13 10H1"
                  stroke="#C2CFE0"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </button>

            <b-button v-b-toggle.sidebar class="toggle ml-4">
              <span></span>
              <span></span>
              <span></span>
            </b-button>
          </nav>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "Header",
  methods: {
    logout() {
      this.$store.dispatch("auth/LOGOUT").then(() => {
        this.$router.push("/auth");
      });
    }
  },
  computed: {
    ...mapState({
      user: s => s.auth.user || {}
    })
  }
};
</script>

<style scoped lang="scss">
.navbar {
  @media only screen and (max-width: 1024px) {
    h2 {
      font-size: 26px;
      line-height: 1.2;
      margin-bottom: 15px;
      text-transform: uppercase;
    }

    h4 {
      font-size: 20px;
      line-height: 1.2;
    }
  }

  @media only screen and (max-width: 576px) {
    h2 {
      font-size: 20px;
      margin-bottom: 15px;
      text-transform: uppercase;
    }

    h4 {
      font-size: 16px;
      line-height: 1.2;
    }
  }
}
</style>
