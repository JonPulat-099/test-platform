<template>
  <div class="custom-input-file custom-input-file-dropzone" @dragover="dragover" @dragleave="dragleave" @drop="drop">
    <label class="custom-input-file__label">
      <div class="custom-input-file__title" v-if="!file">
        <img src="@/static/img/certificate-ico.png" alt="">
        Перетащите файлы сюда
        <br>
        или
      </div>
      <div class="custom-input-file__title" v-else>{{ file.name }}</div>
      <input type="file" ref="file" @change="onChange($event)">
      <div class="custom-input-file__button" type="button">Выберите файлы</div>
    </label>
  </div>
</template>

<script>
  export default {
    name: "CustomFileInput",
    data: () => ({
      file: null
    }),
    methods: {
      onChange: function () {
        this.file = this.$refs.file.files[0];
        this.$emit('input', this.file)
      },
      dragover(event) {
        event.preventDefault();
        // Add some visual fluff to show the user can drop its files
        if (!event.currentTarget.classList.contains('dropzone--active')) {
          event.currentTarget.classList.remove('dropzone--disabled');
          event.currentTarget.classList.add('dropzone--active');
        }
      },
      dragleave(event) {
        // Clean up
        event.currentTarget.classList.add('dropzone--disabled');
        event.currentTarget.classList.remove('dropzone--active');
      },
      drop(event) {
        event.preventDefault();
        this.$refs.file.files = event.dataTransfer.files;
        this.onChange(); // Trigger the onChange event manually
        // Clean up
        event.currentTarget.classList.add('dropzone--disabled');
        event.currentTarget.classList.remove('dropzone--active');
      },
    }
  }
</script>

<style lang="scss" scoped>
  .custom-input-file {
    transition: .2s all;
    border: 2px dashed #E0E7FF;
    padding: 5px 10px;
    padding-right: 5px;
    border-radius: 6px;

    &.dropzone--active {
      border-color: #41BD86;
    }

    &__label {
      display: flex !important;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0 !important;
    }

    &__title {
      color: rgba(46, 56, 77, 0.35);
      font-weight: 500;
      font-size: 14px;
      line-height: 1.2;
    }

    &__button {
      background: #109cf1;
      border-radius: 4px;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 4px 16px;
      color: #FFFFFF;
      font-size: 15px;
      line-height: 1.5;
      transition: .2s all;
      text-transform: none;
      font-weight: 400;

      &:hover,
      &:focus {
        cursor: pointer;
        background: darken(#8A939A, 10);
      }
    }

    input[type="file"] {
      position: absolute;
      overflow: hidden;
      clip: rect(0 0 0 0);
      height: 1px;
      width: 1px;
      margin: -1px;
      padding: 0;
      border: 0;
    }
  }
</style>
