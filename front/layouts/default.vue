<template>
  <div class="site-wrapper">
    <header-site/>

    <div class="wrapper">
      <div class="container-fluid">
        <div class="row">
          <div class="col-md-12">
            <aside-site/>
            <div class="site-content">
              <Nuxt/>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>


<script>
  import HeaderSite from '~/components/Header.vue'
  import AsideSite from '~/components/Aside.vue'


  export default {
    middleware: ['auth'],
    components: {
      HeaderSite,
      AsideSite,
    },
  }
</script>
