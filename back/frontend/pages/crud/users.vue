<template>
  <div class="page">
    <div class="row">
      <div class="col-10">
        <div class="input-group">
          <div class="custom-file">
            <input
              :disabled="disable"
              type="file"
              id="file"
              accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
              @change="onUploadFile"
            />
            <label class="custom-file-label" for="file">{{
              file_name || "Файлни танланг"
            }}</label>
          </div>
        </div>
        <div class="col-12 mt-2 p-0">
          <button class="btn btn-blue" :disabled="disable" @click="addUsers">
            Юклаш
          </button>
        </div>
      </div>
      <div v-if="disable" class="col-10 d-flex justify-content-center">
        <div class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "AddUser",
  data() {
    return {
      file: null,
      file_name: "",
      disable: false
    };
  },
  methods: {
    onUploadFile(e) {
      this.disable = true;
      const file = e.target.files[0];
      if (file) {
        this.file_name = file?.name;
        this.file = file;
      }
      this.disable = false;
    },
    async addUsers() {
      this.disable = true;
      try {
        const formdata = new FormData();
        formdata.append("file", this.file); // apped file

        this.$toast.success(
          "Iltimos kuting foydalanuvchilar qo`shish ma`lum vaqt qoladi.",
          {
            hideProgressBar: true
          }
        );
        const resp = await this.$axios.$post("users/", formdata, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        });
        this.$toast.success(resp?.message || "Muvaffaqiyatli", {
          hideProgressBar: true
        });
      } catch (e) {
        const msg = e.response?.data?.error || "Xatolik yuz berdi.";
        this.$toast.error(msg, {
          hideProgressBar: true
        });
      }
      this.disable = false;
    }
  }
};
</script>
