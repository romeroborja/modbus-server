<template>
  <div
    class="w-auto h-auto collapse navbar-collapse max-height-vh-100 h-100"
    id="sidenav-collapse-main"
  >
    <ul class="navbar-nav">
      <li class="nav-item">
        <sidenav-collapse
          url="#"
          :aria-controls="''"
          v-bind:collapse="false"
          collapseRef="/modbus"
          navText="Modbus addresses"
        >
          <template v-slot:icon>
            <i class="material-icons-round opacity-10 fs-5">table_view</i>
          </template>
        </sidenav-collapse>
      </li>
      <!-- <li class="nav-item">
        <sidenav-collapse
          url="#"
          :aria-controls="''"
          v-bind:collapse="false"
          collapseRef="/configuration"
          navText="Configuración"
        >
          <template v-slot:icon>
            <i class="material-icons-round opacity-10 fs-5">settings</i>
          </template>
        </sidenav-collapse>
      </li> -->
    </ul>
  </div>
</template>
<script>
import SidenavCollapse from "./SidenavCollapse.vue";
import router from "@/router";

export default {
  name: "SidenavList",
  components: {
    SidenavCollapse,
  },
  computed: {
    childRoutes() {
      let paramsRoute = router.resolve({name: "Params"})
      let childrens = paramsRoute.matched[0].children

      return childrens
    }
  }
};
</script>
