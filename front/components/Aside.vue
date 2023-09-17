<template>
  <b-sidebar
    class="d-block"
    id="sidebar"
    backdrop
    no-header
    :backdrop="false"
    :no-close-on-route-change="true"
    :visible="visibleBar"
  >
    <div class="sidebar-inner">
      <div>
        <div v-b-toggle.sidebar class="sidebar-head d-flex align-items-center justify-content-between" >
          <nuxt-link to="/">
            Fanlar
          </nuxt-link>
          <button type="button" class="close" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="sidebar-body">
          <nav>
            <NuxtLink to="/courses">
              <i>
                <svg
                  width="20"
                  height="16"
                  viewBox="0 0 20 16"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M10 4.24988C10.625 1.78269 12.9856 0.522929 18.125 0.499882C18.2072 0.499573 18.2886 0.515527 18.3645 0.546827C18.4405 0.578126 18.5095 0.624151 18.5676 0.68225C18.6257 0.740348 18.6718 0.809371 18.7031 0.885339C18.7344 0.961307 18.7503 1.04272 18.75 1.12488V12.3749C18.75 12.5406 18.6842 12.6996 18.5669 12.8168C18.4497 12.934 18.2908 12.9999 18.125 12.9999C13.125 12.9999 11.1934 14.0081 10 15.4999M10 4.24988C9.375 1.78269 7.01446 0.522929 1.875 0.499882C1.79284 0.499573 1.71143 0.515527 1.63546 0.546827C1.55949 0.578126 1.49047 0.624151 1.43237 0.68225C1.37427 0.740348 1.32825 0.809371 1.29695 0.885339C1.26565 0.961307 1.24969 1.04272 1.25 1.12488V12.2995C1.25 12.6854 1.48907 12.9999 1.875 12.9999C6.875 12.9999 8.81368 14.0155 10 15.4999M10 4.24988V15.4999"
                    stroke="#334D6E"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </i>
              <span>Barcha Testlar</span>
            </NuxtLink>

            <NuxtLink to="/crud/tests" v-if="user && !user.is_student">
              <i>
                <svg
                  width="20"
                  height="16"
                  viewBox="0 0 20 16"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M10 4.24988C10.625 1.78269 12.9856 0.522929 18.125 0.499882C18.2072 0.499573 18.2886 0.515527 18.3645 0.546827C18.4405 0.578126 18.5095 0.624151 18.5676 0.68225C18.6257 0.740348 18.6718 0.809371 18.7031 0.885339C18.7344 0.961307 18.7503 1.04272 18.75 1.12488V12.3749C18.75 12.5406 18.6842 12.6996 18.5669 12.8168C18.4497 12.934 18.2908 12.9999 18.125 12.9999C13.125 12.9999 11.1934 14.0081 10 15.4999M10 4.24988C9.375 1.78269 7.01446 0.522929 1.875 0.499882C1.79284 0.499573 1.71143 0.515527 1.63546 0.546827C1.55949 0.578126 1.49047 0.624151 1.43237 0.68225C1.37427 0.740348 1.32825 0.809371 1.29695 0.885339C1.26565 0.961307 1.24969 1.04272 1.25 1.12488V12.2995C1.25 12.6854 1.48907 12.9999 1.875 12.9999C6.875 12.9999 8.81368 14.0155 10 15.4999M10 4.24988V15.4999"
                    stroke="#334D6E"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </i>
              <span>Саволлар қўшиш</span>
            </NuxtLink>
            <NuxtLink to="/crud/users" v-if="user && !user.is_student">
              <i>
                <svg
                  width="20"
                  height="16"
                  viewBox="0 0 20 16"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M10 4.24988C10.625 1.78269 12.9856 0.522929 18.125 0.499882C18.2072 0.499573 18.2886 0.515527 18.3645 0.546827C18.4405 0.578126 18.5095 0.624151 18.5676 0.68225C18.6257 0.740348 18.6718 0.809371 18.7031 0.885339C18.7344 0.961307 18.7503 1.04272 18.75 1.12488V12.3749C18.75 12.5406 18.6842 12.6996 18.5669 12.8168C18.4497 12.934 18.2908 12.9999 18.125 12.9999C13.125 12.9999 11.1934 14.0081 10 15.4999M10 4.24988C9.375 1.78269 7.01446 0.522929 1.875 0.499882C1.79284 0.499573 1.71143 0.515527 1.63546 0.546827C1.55949 0.578126 1.49047 0.624151 1.43237 0.68225C1.37427 0.740348 1.32825 0.809371 1.29695 0.885339C1.26565 0.961307 1.24969 1.04272 1.25 1.12488V12.2995C1.25 12.6854 1.48907 12.9999 1.875 12.9999C6.875 12.9999 8.81368 14.0155 10 15.4999M10 4.24988V15.4999"
                    stroke="#334D6E"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </i>
              <span>Фойдаланувчи қўшиш</span>
            </NuxtLink>
          </nav>
        </div>
      </div>
    </div>
  </b-sidebar>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "Aside",
  data() {
    return {
      value: 10,
      max: 100,
      visibleBar: false
    };
  },
  computed: {
    ...mapState({
      user: s => s.auth.user
    })
  },

  /*computed:{
    visible(){
      if(window.width > 1200){
        return true
      }
      else {
        return false
      }
    }
  }*/

  mounted() {
    // this.resize();

    window.addEventListener("resize", this.resize);
  },
  destroyed() {
    window.removeEventListener("resize", this.resize);
  },
  methods: {
    resize() {
      if (window.innerWidth > 992) {
        this.visibleBar = true;
      } else {
        this.visibleBar = false;
      }
    }
  }
};
</script>

<style scoped lang="scss">
.sidebar-head {
  a {
    font-size: 24px;
    font-weight: 500;
    text-decoration: none;
    color: #1a202c;
    transition: all 0.2s;
    display: block;

    &:hover {
      transform: scale(1.1) translateX(10px);
    }
  }
}
</style>
