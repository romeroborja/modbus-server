<template>
  <router-link
    :data-bs-toggle="collapse ? 'collapse' : ''"
    :to="collapseRef"
    :aria-controls="collapseRef"
    :aria-expanded="isExpanded"
    class="nav-link"
    v-bind="$attrs"
    @click="isExpanded = !isExpanded"
  >
    <span
      v-if="submenu"
      class="sidenav-mini-icon text-white"
    >
      {{ navText[0]}}
    </span>
    <div
      v-else
      class="text-center d-flex align-items-center justify-content-center"
      :class="isRTL ? ' ms-2' : 'me-2'"
    >
      <slot name="icon"></slot>
    </div>
    <span :class="submenu ? 'sidenav-normal me-3 ms-3 ps-1 text-white text-white' : 'nav-link-text'">
      {{ navText }}
    </span>
  </router-link>

  <div
    v-if="collapse"
    :id="collapseRef"
    :class="isExpanded ? 'collapse show' : 'collapse'"
  >
    <slot name="list"></slot>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "SidenavCollapse",
  props: {
    collapseRef: {
      type: String,
      required: true,
    },
    navText: {
      type: String,
      required: true,
    },
    collapse: {
      type: Boolean,
      default: true,
    },
    submenu: {
      type: Boolean,
      default: false
    },
  },
  data() {
    return {
      isExpanded: false,
    };
  },
  methods: {
    getRoute() {
      const routeArr = this.$route.path.split("/");
      return `/${routeArr[1]}`;
    },
  },
  computed: {
    ...mapState(["isRTL", "color"]),
  },
};
</script>
