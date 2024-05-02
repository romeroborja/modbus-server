<template>
  <!-- navcard -->
  <div class="card position-sticky top-1 mt-4">
    <ul class="nav flex-column bg-white border-radius-lg p-3">
      <li
        class="nav-item p-1"
        v-for="(option, index) in options" :key="index"
      >
        <a
          class="nav-link text-dark d-flex"
          data-bs-toggle="tab"
          href="#"
          :class="{ active: selectedOption === index }"
          :aria-selected="selectedOption === index"
          @click="selectOption(index)"
        >
          <i class="material-icons text-lg me-2">table_rows</i>
          <span class="text-sm">
            {{ option }}
          </span>
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "nav-card",
  props: {
    options: {
      type: Array,
      required: true
    },
    selectedNavPill:{
      type: String,
      required: false
    }
  },
  data() {
    return {
      selectedOption: 0,
    }
  },
  emits: ['selectedOption'],
  methods: {
    selectOption(index) {
      this.selectedOption = index
      this.$emit('selectedOption', this.options[this.selectedOption])
    }
  },
  watch: {
    selectedNavPill() {
      this.selectOption(0)
    }
  },
  mounted() {
    this.selectOption(this.selectedOption)
  }
}
</script>

<style>

</style>