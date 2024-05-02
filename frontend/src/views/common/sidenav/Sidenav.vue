<template>
  <aside
    id="sidenav-main"
    class="sidenav navbar navbar-vertical navbar-expand-xs"
    :class="`${isRTL ? 'me-3 rotate-caret fixed-end' : 'fixed-start'} ${sidebarType}`"
  >
    <div class="sidenav-header">
      <i
        class="top-0 p-3 cursor-pointer fas fa-times text-secondary opacity-5 position-absolute end-0 d-none d-xl-none"
        aria-hidden="true"
        id="iconSidenav"
      ></i>
      <a class="m-0 navbar-brand" href="/">
        <img
          :src="sidebarType === 'bg-white' || (sidebarType === 'bg-transparent' && !isDarkMode) ? logoModbus : logoModbus"
          class="navbar-brand-img h-100"
          alt="main_logo"
        />
        <span class="ms-2 font-weight-bold text-white">Modbus Server</span>
      </a>
    </div>
    <hr class="horizontal light mt-0 mb-2" />
    <sidenav-list />
  </aside>
</template>

<script>
import SidenavList from "./SidenavList.vue";
import logoModbus from "@/assets/img/modbus-server.png";
import { mapState } from "vuex";

export default {
  name: "sidenav",
  components: {
    SidenavList,
  },
  data() {
    return {
      logoModbus
    };
  },
  computed: {
    ...mapState(["isRTL", "sidebarType", "isDarkMode"]),
  },
};
</script>
