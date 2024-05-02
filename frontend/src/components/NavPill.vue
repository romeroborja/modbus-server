<template>
  <!-- navpill -->
  <div class="nav-wrapper position-relative end-0">
    <ul class="nav nav-pills nav-fill p-1" role="tablist">
      <li
        class="nav-item"
        v-for="(option, index) in options" :key="index"
      >
        <a
          class="nav-link mb-0 px-2 py-1"
          data-bs-toggle="tab"
          href="#"
          :class="{ active: selectedOption === index }"
          :aria-selected="selectedOption === index"
          @click="selectOption(index)"
        >
          {{ option }}
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
import setNavPills from "@/assets/js/nav-pills.js";

export default {
  name: "nav-pill",
  data() {
    return {
      selectedOption: 0,
    }
  },
  props: {
    options: {
      type: Object,
      required: true
    }
  },
  emits: ['selectedOption'],
  methods: {
    selectOption(index) {
      this.selectedOption = index
      this.$emit('selectedOption', this.options[this.selectedOption])
    }
  },
  mounted() {
    setNavPills()
    this.selectOption(this.selectedOption)
  },
};
</script>
