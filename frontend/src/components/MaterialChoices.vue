<template>
  <select id="select">
  </select>
</template>

<script>
import Choices from 'choices.js';

export default {
  name: 'material-choices',
  emits: ['selectedOption'],
  props: {
    options: {
      type: Object,
      default: () => {}
    },
    defaultOption: {
      type: Number,
      default: 0
    },
  },
  data() {
    return {
      choicesInstance: undefined
    }
  },
  methods: {
    resetSelect() {
      this.choicesInstance.setChoiceByValue(this.defaultOption.toString());
    }
  },
  mounted() {
    const options = Object.entries(this.options).map(([value, label]) => {
      if (value == this.defaultOption) {
        return {value, label, selected: true};
      }
      return {value, label};
    });

    const selectElement = document.querySelector('#select');
    this.choicesInstance = new Choices(selectElement, {
      noResultsText: 'No se han encontrado resultados',
      itemSelectText: '',
      choices: options,
    })

    const choices = this.choicesInstance
    this.choicesInstance.passedElement.element.addEventListener('showDropdown', function () {
      setTimeout(() => {
        const input = choices.input.element;
        if (input) {
          input.focus();
        }
      }, 50);
    });

    selectElement.addEventListener('change', (event) => {
      this.$emit('selectedOption', parseInt(event.detail.value))
    });
  },
}
</script>
