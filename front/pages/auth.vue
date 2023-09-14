<template>
  <div class="auth-container w-65" style="rgba(166, 30, 77, .2) !important">
    <div class="center-block">
      <h1 class="university__title">TASHKENT INTERNATIONAL UNIVERSITY</h1>
      <img class="logo__university" src="/logo.png" alt="">
      <!-- <h1 class="text-center mb-4">TEST</h1> -->
      <div class="main-bock auth">
        <form @submit.prevent="submit">
          <div
            class="form-group"
            :class="{
              'form-group--error': $v.username.$error,
              'form-group--loading': $v.username.$pending
            }"
          >
            <label>Login</label>
            <div class="error top-rigth" v-if="error === true">
              Login yoki parol xato
            </div>
            <b-form-input
              v-model.trim="$v.username.$model"
              id="input-live"
              aria-describedby="input-live-help input-live-feedback"
              placeholder="Loginni kiriting"
            ></b-form-input>
            <div class="error" v-if="!$v.username.required">
              Login kiritishingiz shart
            </div>
          </div>
          <div
            class="form-group"
            :class="{ 'form-group--error': $v.password.$error }"
          >
            <label>Parol</label>
            <b-form-input
              v-model.trim="$v.password.$model"
              id="input-live-2"
              aria-describedby="input-live-help input-live-feedback"
              placeholder="Parolni kiriting"
              type="password"
            ></b-form-input>
            <div class="error" v-if="!$v.password.required">
              Parol kiritishingiz shart
            </div>
          </div>
          <div class="d-flex flex-column align-items-center mt-3">
            <button class="mb-3 auth-button" type="submit">KIRISH</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import Vuelidate from "vuelidate";
import { mapState } from "vuex";
Vue.use(Vuelidate);
import { required } from "vuelidate/lib/validators";

export default {
  middleware: ["no-auth"],
  name: "auth",
  layout: "auth",
  data() {
    return {
      username: "",
      password: ""
    };
  },
  computed: {
    ...mapState({
      error: state => state.auth.error
    })
  },
  methods: {
    async submit() {
      this.$v.$touch();

      if (!this.$v.$invalid) {
        await this.$store
          .dispatch("auth/LOGIN", {
            username: this.username,
            password: this.password
          })
          .then(async () => {
            await this.$store.dispatch("auth/FETCH_USER");
          })
          .catch(() => {
            alert("Login yoki parol no‘to‘g‘ri kiritilgan");
            this.$router.push("/");
          });
      }
    }
  },
  validations: {
    username: {
      required
    },
    password: {
      required
    }
  }
};
</script>
<style scoped lang="scss">

.auth-container {
  position: relative;
  z-index: 100;
}
.logo__university {
  width: 350px;
  height: 200px;
  display: block;
  margin: 0 auto 20px;
  position: relative;
  object-fit: cover;
}

.university__title {
  margin: 0 auto;
  font-size: 28px;
  line-height: 40px;
  text-align: center;
  font-weight: 600;
  text-transform: uppercase;
  position: relative;
  // z-index: 1;
}

.auth {
  background: rgba(255, 255, 255, .5) !important;
  filter: blur(.8);
}
.form-group {
  position: relative;
}

.form-group--error {
  label {
    color: #eb5757;
  }

  input {
    background: #ffffff;
    border: 1px solid #eb5757;
    box-sizing: border-box;
    border-radius: 4px;
  }
}

.auth-button {
  background: #4a5ad0;
  width: 100%;
  padding: 15px;
  box-shadow: 0px 4px 8px rgba(16, 156, 241, 0.24);
  border-radius: 4px;
  font-weight: 500;
  font-size: 23px;
  line-height: 18px;
  text-align: center;
  letter-spacing: -0.08px;
  color: #ffffff;
  border: none;
  border-radius: 10px;

  &:focus {
    outline: none;
  }
}

label {
  font-style: normal;
  font-weight: 600;
  font-size: 15px;
  line-height: 18px;
  /* identical to box height */

  letter-spacing: -0.24px;

  /* TextGreyC-0 */

  color: #90a0b7;
}

input {
  padding: 25px 18px;
  font-weight: normal;
  font-size: 15px;
  line-height: 18px;
  letter-spacing: 0.36px;
  background: #ffffff;
}

.error {
  color: #eb5757;
}

.top-rigth {
  position: absolute;
  right: 0;
  top: 0;
}
</style>
