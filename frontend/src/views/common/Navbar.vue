<template>
  <nav
    class="shadow-none navbar navbar-main navbar-expand-lg border-radius-xl"
    v-bind="$attrs"
    id="navbarBlur"
    data-scroll="true"
    :class="isAbsolute ? 'mt-4' : 'mt-0'"
  >
    <div class="px-3 py-1 container-fluid">
      <breadcrumbs :currentPage="currentRouteName" :color="color" />
      <div
        class="mt-2 collapse navbar-collapse mt-sm-0 me-md-0 me-sm-4"
        id="navbar"
      >
        <ul class="navbar-nav justify-content-end ms-md-auto">
          <li class="nav-item d-xl-none ps-3 d-flex align-items-center">
            <a
              href="#"
              @click="toggleSidebar"
              class="p-0 nav-link text-body lh-1"
              id="iconNavbarSidenav"
            >
              <div class="sidenav-toggler-inner">
                <i class="sidenav-toggler-line"></i>
                <i class="sidenav-toggler-line"></i>
                <i class="sidenav-toggler-line"></i>
              </div>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
// import MaterialInput from "@/components/MaterialInput.vue";
import Breadcrumbs from "@/views/common/Breadcrumbs.vue";
import { mapMutations, mapState } from "vuex";

export default {
  name: "navbar",
  data() {
    return {
      showMenu: false,
      showUserMenu: false
    };
  },
  props: ["minNav", "color"],
  created() {
    this.minNav;
  },
  methods: {
    logout() {
      this.$store.dispatch('logout');
      this.$router.push({name: 'Login'});
    },
    ...mapMutations(["navbarMinimize", "toggleConfigurator"]),

    toggleSidebar() {
      this.navbarMinimize();
    },
  },
  components: {
    Breadcrumbs,
    // MaterialInput,
  },
  computed: {
    ...mapState(["isAbsolute"]),
    ...mapState({isAuthenticated: state => state.auth.isAuthenticated}),
    ...mapState({userName: state => state.auth.userName}),

    currentRouteName() {
      return this.$route.name;
    },
  },
};
</script>
